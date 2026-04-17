from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager, create_access_token, get_jwt
from celery import Celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import os

def company_only():
    claims = get_jwt()
    return claims.get("role") == "company"

def admin_only():
    claims = get_jwt()
    return claims.get("role") == "admin"


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CORS(app, supports_credentials=True)

app.config["SECRET_KEY"] = "placement-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)

from flask_caching import Cache

# redis config
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1" 

cache = Cache(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

celery.conf.beat_schedule = {
    "send-company-report": {
        "task": "app.send_company_reports_task",
        "schedule": 60.0
    },
    "interview-reminder": {
        "task": "app.interview_reminder_job",
        "schedule": 60.0
    }
}

EMAIL_USER = ""
EMAIL_PASS = ""

@celery.task(name="app.interview_reminder_job")
def interview_reminder_job():
    print("running interview reminder job")

    applications = Application.query.filter_by(status="Shortlisted").all()
    print("applications found:", len(applications))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
    except Exception as e:
        print("smtp error:", e)
        return

    for app_obj in applications:
        if not app_obj.student or not app_obj.student.user:
            continue

        email = app_obj.student.user.email
        name = app_obj.student.user.name

        try:
            msg = MIMEMultipart()
            msg["Subject"] = "Interview Scheduled"
            msg["From"] = EMAIL_USER
            msg["To"] = email

            body = f"""
Hello {name},

Your interview has been scheduled.

Company: {app_obj.job.company.company_name if app_obj.job and app_obj.job.company else "N/A"}
Date & Time: {app_obj.interview_datetime}
Mode: {app_obj.interview_mode}

All the best!
"""
            msg.attach(MIMEText(body, "plain"))

            server.sendmail(EMAIL_USER, email, msg.as_string())
            print("mail sent to", email)

        except Exception as e:
            print("mail failed:", e)

    server.quit()


@celery.task(name="app.send_company_reports_task")
def send_company_reports_task():
    companies = CompanyProfile.query.all()

    if not companies:
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
    except Exception as e:
        print("SMTP error:", e)
        return

    report_file = generate_placement_report()

    for company in companies:
        if not company.user:
            continue

        try:
            msg = MIMEMultipart()
            msg["Subject"] = "Placement Report"
            msg["From"] = EMAIL_USER
            msg["To"] = company.user.email

            body = f"Hello {company.company_name},\n\nReport generated: {report_file}"
            msg.attach(MIMEText(body, "plain"))

            server.sendmail(EMAIL_USER, company.user.email, msg.as_string())
            print("sent to:", company.user.email)

        except Exception as e:
            print("send failed:", e)

    server.quit()


# user model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # admin / student / company
    role = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # one to one relationship one User has one StudentProfile
    student_profile = db.relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False
    )

    # one to one relationship one User has one CompanyProfile
    company_profile = db.relationship(
        "CompanyProfile",
        back_populates="user",
        uselist=False
    )
# StudentProfile model
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    # foriegn key one to one each StudentProfile belongs to one User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    department = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    skills = db.Column(db.String(200))  # comma-separated
    resume = db.Column(db.String(200))
    placement_status = db.Column(
        db.String(50), default="Not Placed"
    )
    # one to one each StudentProfile belongs to one User
    user = db.relationship("User", back_populates="student_profile")
    # one to many relationship one Student can apply to many jobs
    applications = db.relationship(
        "Application",
        back_populates="student"
    )
# CompanyProfile model
class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    # foriegn key one to one each CompanyProfile belongs to one User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    company_name = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    website = db.Column(db.String(150))
    location = db.Column(db.String(100))
    company_size = db.Column(db.String(50))
    # one to one each CompanyProfile belongs to one User
    user = db.relationship("User", back_populates="company_profile")
    # one to many relationship one company can post many jobs
    jobs = db.relationship(
        "Job",
        back_populates="company"
    )
# job model
class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    # foriegn key many to one many jobs posted by 1 company
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id")
    )
    experience = db.Column(db.String(50))
    job_type = db.Column(db.String(50))
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    skills = db.Column(db.String(200))
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean, default=False)
    is_close = db.Column(db.Boolean, default=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    # many jobs posted by 1 company
    company = db.relationship("CompanyProfile", back_populates="jobs")
    # one to many one Job can have many Applications
    applications = db.relationship(
        "Application",
        back_populates="job"
    )
# application model
class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"))
    status = db.Column(db.String(50), default="Applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    remarks = db.Column(db.String(200))
    interview_datetime = db.Column(db.String(100))
    interview_mode = db.Column(db.String(50))
    interview_link = db.Column(db.String(200))
    interview_location = db.Column(db.String(200))
    feedback = db.Column(db.String(200))
    offer_letter = db.Column(db.String(200))
    # many to one many applications sent for one job
    job = db.relationship("Job", back_populates="applications")
    # many to one many applications sent by one student
    student = db.relationship("StudentProfile", back_populates="applications")

# Routing
# registeration
@app.route("/register", methods=["POST"])
def register():
    data = request.json  # stores in dictionary format
    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]                  # admin / student / company
    phone = data.get("phone")            # optional
    # check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already registered"})
    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role=role,
        phone=phone,
        is_active=True,
        # is_approved=False
        is_approved=False if role == "company" else True
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    })
# login


@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()

    if not data:
        return jsonify({"msg": "no data found bro"}), 400

    email = data.get("email")
    password = data.get("password")

    # find user
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "user not found"}), 404

    # check password
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "wrong password"}), 401

    # block company login if not approved
    if user.role == "company" and not user.is_approved:
        return jsonify({
            "msg": "wait for admin approval, you can't login yet"
        }), 403

    # generate token if everything ok
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role,
            "email": user.email
        }
    )

    return jsonify({
        "msg": "login success",
        "token": access_token,
        "role": user.role
    }), 200
from flask import send_from_directory
#for uploading resumee
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
#company routes
# for creating company ka profile

@app.route("/company/update_profile", methods=["PUT"])
@jwt_required()
def update_company_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Profile not found"}), 404

    # simple updates 
    company.company_name = data.get("company_name", company.company_name)
    company.description = data.get("description", company.description)
    company.location = data.get("location", company.location)
    company.website = data.get("website", company.website)

    db.session.commit()

    return jsonify({"msg": "Profile updated successfully"})

@app.route('/company/create_profile', methods=['POST'])
@jwt_required()
def create_company_profile():
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    existing = CompanyProfile.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({"message": "Profile already exists"})
    data = request.get_json()
    profile = CompanyProfile(
        user_id=user_id,
        company_name=data.get("company_name"),
        industry=data.get("industry"),
        website=data.get("website"),
        location=data.get("location"),
        company_size=data.get("company_size")
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({"message": "Company profile created"})
# get company ka profile
@app.route('/company/get_profile', methods=['GET'])
@cache.cached(timeout=300)
@jwt_required()
def get_company_profile():
    print("get_profile called")

    # check role
    if not company_only():
        print(" not a company user")
        return jsonify({"message": "Unauthorized"}), 403

    user_id = get_jwt_identity()

    profile = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        print(" profile not found for user:", user_id)
        return jsonify({"message": "Profile not found"}), 404


    print(" profile found:", profile.company_name, "|", profile.industry)

    return jsonify({
        "company_name": profile.company_name or "",
        "industry": profile.industry ,
        "website": profile.website ,
        "location": profile.location ,
        "company_size": profile.company_size 
    }), 200
    # creating job posting
@app.route("/company/create_drive", methods=["POST"])
@jwt_required()
def create_drive():
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # approval check
    if not user.is_approved:
        return jsonify({"message": "Wait for admin approval"})
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message": "Create profile first"})
    data = request.get_json()
    drive = Job(
    company_id=company.id,
    title=data.get("title"),
    description=data.get("description"),
    skills=data.get("skills"),
    salary=data.get("salary"),
    location=data.get("location"),
    eligibility=data.get("eligibility"),
    deadline=datetime.strptime(data.get("deadline"), "%Y-%m-%d"),
    is_approved=True )
    db.session.add(drive)
    db.session.commit()
    return jsonify({"message": "Drive created"})
# company dashboard display
@app.route("/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():
    if not company_only():
        return jsonify({"message": "Unauthorized"}), 403

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drives = Job.query.filter_by(company_id=company.id).all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "title": d.title,
            "is_approved": d.is_approved,
            "is_close": d.is_close,
            "applicants_count": len(d.applications),
            "posted_at": d.posted_at
        })

    return jsonify({
        "company_name": company.company_name,  
        "industry": company.industry,           
        "website": company.website,             
        "drives": result                        
    }), 200
# seeing company postings of jobs
@app.route("/company/my_drives", methods=["GET"])
@jwt_required()
def get_my_drives():
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message": "Company not found"})
    drives = Job.query.filter_by(company_id=company.id).all()
    data = []
    for d in drives:
        data.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "skills": d.skills,
            "salary": d.salary,
            "location": d.location,
            "eligibility": d.eligibility,
            "deadline": d.deadline,
            "is_close": d.is_close,
            "is_approved": d.is_approved
        })
    return jsonify(data)
# to reopen a drive that was previously closed
@app.route("/company/open_drive/<int:drive_id>", methods=["POST"])
@jwt_required()
def open_drive(drive_id):
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    drive = Job.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({"message": "Drive not found"})
    if not drive.is_close:
        return jsonify({"message": "Already open"})
    drive.is_close = False
    db.session.commit()
    return jsonify({"message": "Drive opened"})
# close the drive
@app.route("/company/close_drive/<int:drive_id>", methods=["POST"])
@jwt_required()
def close_drive(drive_id):
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    drive = Job.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({"message": "Drive not found"})
    if drive.is_close:
        return jsonify({"message": "Already closed"})
    drive.is_close = True
    db.session.commit()
    return jsonify({"message": "Drive closed"})
# to view applications
@app.route("/company/drive/<int:drive_id>/applications", methods=["GET"])
@jwt_required()
def view_applications(drive_id):
    if not company_only():
        return jsonify({"message": "Unauthorized"}), 403

    user_id = get_jwt_identity()

    company = CompanyProfile.query.filter_by(user_id=user_id).first()

    drive = Job.query.filter_by(id=drive_id, company_id=company.id).first()

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    apps = Application.query.filter_by(job_id=drive_id).all()

    result = []
    for a in apps:
        result.append({
            "application_id": a.id,
            "student_name": a.student.user.name,
            "department": a.student.department,
            "cgpa": a.student.cgpa,
            "status": a.status,
            "skills": a.student.skills,
            "year": a.student.year,

          "resume_url": f"http://127.0.0.1:5000/uploads/{a.student.resume}" if a.student.resume else ""
        })

    return jsonify(result), 200 
# to change application status
@app.route("/company/application/<int:app_id>/update", methods=["POST"])
@jwt_required()
def update_application(app_id):
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    data = request.get_json()
    status = data.get("status")
    app_obj = Application.query.get(app_id)
    if not app_obj:
        return jsonify({"message": "Application not found"})
    app_obj.status = status
    app_obj.updated_at = datetime.utcnow()
    if status == "Rejected":
        app_obj.feedback = data.get("feedback")
    if status == "Shortlisted":
        app_obj.interview_datetime = data.get("interview_datetime")
        app_obj.interview_mode = data.get("interview_mode")
        app_obj.interview_link = data.get("interview_link")
    if status == "Selected":
        app_obj.remarks = "You are selected"
    db.session.commit()
    return jsonify({"message": "Updated"})
#edit manage drives
@app.route("/company/update_drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def update_drive(drive_id):
    if not company_only():
        return jsonify({"message": "Unauthorized"})
    user_id = get_jwt_identity()
    company = CompanyProfile.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({"message": "Company not found"})
    drive = Job.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({"message": "Drive not found"})
    data = request.get_json()
    if "title" in data:
        drive.title = data["title"]
    if "description" in data:
        drive.description = data["description"]
    if "skills" in data:
        drive.skills = data["skills"]
    if "salary" in data:
        drive.salary = data["salary"]
    if "location" in data:
        drive.location = data["location"]
    if "eligibility" in data:
        drive.eligibility = data["eligibility"]
    if "deadline" in data and data["deadline"]:
        drive.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
    db.session.commit()
    return jsonify({"message": "Drive updated"})

#student routes
#get student profile
@app.route("/student/profile", methods=["GET"])
@jwt_required()
def get_student_profile():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)
    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({
            "exists": False,
            "id": user.id,
            "name": user.name
        })
    resume_url = ""
    if profile.resume:
        resume_url = f"http://127.0.0.1:5000/uploads/{profile.resume}"

    return jsonify({
        "exists": True,
        "id": profile.id,
        "name": user.name,
        "department": profile.department,
        "year": profile.year,
        "cgpa": profile.cgpa,
        "skills": profile.skills,
        "resume_url": resume_url,
        "placement_status": profile.placement_status
    })#create or update studnet profile
@app.route("/student/profile", methods=["POST"])
@jwt_required()
def create_or_update_student_profile():
    user_id = int(get_jwt_identity())
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = StudentProfile(user_id=user_id)
    profile.department = request.form.get("department")
    profile.year = request.form.get("year")
    profile.cgpa = request.form.get("cgpa")
    profile.skills = request.form.get("skills")
    file = request.files.get("resume")
    if file:
        filename = f"{user_id}_resume.pdf"
        filepath = os.path.join("uploads", filename)
        file.save(filepath)
        profile.resume = filename
    db.session.add(profile)
    db.session.commit()
    return jsonify({"message": "Profile saved"})
#get all available jobs 
@app.route("/student/jobs", methods=["GET"])
@cache.cached(timeout=60, query_string=True)  
@jwt_required()

def get_jobs():
    print(" DB HIT - fetching jobs from database")
    search = request.args.get("search")
    query = Job.query.filter_by(is_approved=True, is_close=False)
    if search:
        query = query.filter(Job.title.ilike(f"%{search}%"))
    jobs = query.all()
    result = []
    for j in jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "company": j.company.company_name,
            "company_id": j.company.id,
            "location": j.location,
            "salary": j.salary,
            "skills": j.skills,
            "deadline": j.deadline
        })
    return jsonify(result)
#student applying to job
@app.route("/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):
    user_id = int(get_jwt_identity())
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "Create profile first"})
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"message": "Job not found"})
    if job.is_close:
        return jsonify({"message": "Job is closed"})
    if not job.is_approved:
        return jsonify({"message": "Job not approved"})
    existing = Application.query.filter_by(
        job_id=job_id,
        student_id=profile.id
    ).first()
    if existing:
        return jsonify({"message": "Already applied"})
    application = Application(
        job_id=job_id,
        student_id=profile.id,
        status="Applied"
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Applied successfully"})
#application statuses 
@app.route("/student/applications", methods=["GET"])
@jwt_required()
def get_student_applications():
    user_id = int(get_jwt_identity())
    # get student profile
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        print('not profie')
        return jsonify([])
    # get all applications of this student
    applications = Application.query.filter_by(student_id=profile.id).all()

    data = []

    for app in applications:
        job = Job.query.get(app.job_id)

        data.append({
            "job_id": app.job_id,
            "job_title": job.title if job else "N/A",
            "status": app.status
        })

    print("Applications sending:", data)  
    return jsonify(data)



#company details for student to see
@app.route("/student/company/<int:id>", methods=["GET"])
@jwt_required()
def company_details(id):
    company = CompanyProfile.query.get(id)
    if not company:
        return jsonify({"message": "Company not found"})
    jobs = Job.query.filter_by(
        company_id=id,
        is_approved=True,
        is_close=False
    ).all()
    return jsonify({
        "company": {
            "id": company.id,
            "name": company.company_name,
            "industry": company.industry,
            "location": company.location
        },
        "jobs": [{
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "salary": j.salary,
            "location": j.location
        } for j in jobs]
    })

#admin routes
#admin getting total counts 
@app.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    total_students = User.query.filter_by(role="student").count()
    total_companies = User.query.filter_by(role="company").count()
    total_drives = Job.query.count()
    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives
    })
#takes all users who are companies and returns their details.
@app.route("/admin/companies", methods=["GET"])
@jwt_required()
def get_companies():
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    companies = User.query.filter_by(role="company").all()
    result = []
    for c in companies:
        result.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "is_approved": c.is_approved,
            "is_active": c.is_active
        })
    return jsonify(result)
#admin approving company 
@app.route("/admin/company/<int:id>/approve", methods=["POST"])
@jwt_required()
def approve_company(id):
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"})
    if user.role != "company":
        return jsonify({"message": "Not a company"})
    if user.is_approved:
        return jsonify({"message": "Already approved"})
    user.is_approved = True
    user.is_active = True
    db.session.commit()
    return jsonify({"message": "Company approved"})
#admin rejecting comapny
@app.route("/admin/company/<int:id>/reject", methods=["POST"])
@jwt_required()
def reject_company(id):
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"})
    if user.role != "company":
        return jsonify({"message": "Not a company"})
    if not user.is_approved:
        return jsonify({"message": "Already rejected"})
    user.is_approved = False
    user.is_active = False
    db.session.commit()
    return jsonify({"message": "Company rejected"})
#shows all drives to admin
@app.route("/admin/drives", methods=["GET"])
@jwt_required()
def get_all_drives():
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    drives = Job.query.all()
    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "title": d.title,
            "company": d.company.company_name if d.company else "N/A",
            "is_approved": d.is_approved
        })
    return jsonify(result)
#admin approving drives 
@app.route("/admin/drive/<int:id>/approve", methods=["POST"])
@jwt_required()
def approve_drive(id):
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    drive = Job.query.get(id)
    if not drive:
        return jsonify({"message": "Drive not found"})
    if drive.is_approved:
        return jsonify({"message": "Drive already approved"})
    drive.is_approved = True
    db.session.commit()
    return jsonify({"message": "Drive approved"})
#admin rejectingg drives 
@app.route("/admin/drive/<int:id>/reject", methods=["POST"])
@jwt_required()
def reject_drive(id):
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    drive = Job.query.get(id)
    if not drive:
        return jsonify({"message": "Drive not found"})
    drive.is_approved = False
    db.session.commit()
    return jsonify({"message": "Drive rejected"})
#view all applicatins
@app.route("/admin/applications", methods=["GET"])
@jwt_required()
def all_applications():
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    apps = Application.query.all()
    return jsonify([{
        "student": a.student.user.name,
        "company": a.job.company.company_name,
        "job": a.job.title,
        "status": a.status
    } for a in apps])
#searching 
@app.route("/admin/search", methods=["GET"])
@jwt_required()
def search():
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    q = request.args.get("q")
    students = User.query.filter(
        User.role == "student",
        User.name.ilike(f"%{q}%")
    ).all()
    companies = User.query.filter(
        User.role == "company",
        User.name.ilike(f"%{q}%")
    ).all()
    return jsonify({
        "students": [{"id": s.id, "name": s.name} for s in students],
        "companies": [{"id": c.id, "name": c.name} for c in companies]
    })
#blacklisting
@app.route("/admin/user/<int:id>/toggle", methods=["POST"])
@jwt_required()
def toggle_user(id):
    if not admin_only():
        return jsonify({"message": "Unauthorized"})
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"})
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({"message": "User status updated"})


def init_db():
    db.create_all()
    if not User.query.filter_by(role="admin").first():
        admin = User(
            name="Admin",
            email="admin@college.com",
            password=generate_password_hash("admin123"),
            role="admin",
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")

def generate_company_report(company_id):

    company = CompanyProfile.query.get(company_id)
    if not company:
        return None

    jobs = Job.query.filter_by(company_id=company_id).all()

    applications = Application.query.join(Job).filter(
        Job.company_id == company_id
    ).all()

    total_jobs = len(jobs)
    total_applications = len(applications)

    shortlisted = len([a for a in applications if a.status == "Shortlisted"])
    selected = len([a for a in applications if a.status == "Selected"])
    rejected = len([a for a in applications if a.status == "Rejected"])

    report_text = f"""
COMPANY REPORT

Company: {company.company_name}

Total Jobs: {total_jobs}
Total Applications: {total_applications}

Shortlisted: {shortlisted}
Selected: {selected}
Rejected: {rejected}

"""

    for app_obj in applications:
        student = app_obj.student
        job = app_obj.job

        if not student or not job:
            continue

        report_text += f"""
Student Name: {student.user.name}
Email: {student.user.email}
Department: {student.department}
CGPA: {student.cgpa}

Applied For: {job.title}
Status: {app_obj.status}
"""

    return report_text
def send_company_report(company):

    report = generate_company_report(company.id)
    if not report:
        return

    from email.message import EmailMessage
    import smtplib

    msg = EmailMessage()
    msg["Subject"] = "Company Placement Report"
    msg["From"] = EMAIL_USER
    msg["To"] = company.user.email

    msg.set_content(report)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print("Report sent to:", company.user.email)



@app.route("/company/download-report")
def download_report():

    files = os.listdir("reports")

    if not files:
        return {"error": "No reports found"}, 404

    latest_file = sorted(files)[-1]

    return send_from_directory(
        "reports",
        latest_file,
        as_attachment=True
    )

@app.route("/admin/generate-report", methods=["GET"])
@jwt_required()
def generate_report():
   

    os.makedirs("reports", exist_ok=True)  # ensure folder exists

    task = generate_placement_report.delay()  # fire celery task

    return jsonify({
        "message": "Report generation started",
        "task_id": task.id
    }), 202

@app.route("/admin/report-status/<task_id>", methods=["GET"])
@jwt_required()
def report_status(task_id):


    from celery.result import AsyncResult
    result = AsyncResult(task_id, app=celery)

    if result.state == "PENDING":
        return jsonify({"status": "pending"}), 202

    elif result.state == "SUCCESS":
        filename = result.result  # task returns filename
        return jsonify({
            "status": "done",
            "download_url": f"/admin/download-report/{filename}"
        }), 200

    elif result.state == "FAILURE":
        return jsonify({"status": "failed", "error": str(result.result)}), 500

    return jsonify({"status": result.state}), 202


@app.route("/admin/download-report/<filename>", methods=["GET"])

def download_report_file(filename):
   

    return send_from_directory(
        os.path.abspath("reports"),
        filename,
        as_attachment=True
    )

@celery.task(name="app.generate_placement_report")
def generate_placement_report():

    import os
    os.makedirs("reports", exist_ok=True)

    filename = f"company_report_{datetime.now().date()}.csv"
    filepath = os.path.join("reports", filename)

    applications = Application.query.all()
    jobs = Job.query.all()

    total_jobs = len(jobs)
    total_applications = len(applications)

    shortlisted = len([a for a in applications if a.status == "Shortlisted"])
    selected = len([a for a in applications if a.status == "Selected"])
    rejected = len([a for a in applications if a.status == "Rejected"])

    placement_rate = round((selected / total_applications) * 100, 2) if total_applications else 0

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Company Placement Report"])
        writer.writerow(["Generated On", datetime.now()])
        writer.writerow([])

        writer.writerow(["Total Jobs", total_jobs])
        writer.writerow(["Total Applications", total_applications])
        writer.writerow(["Shortlisted", shortlisted])
        writer.writerow(["Selected", selected])
        writer.writerow(["Rejected", rejected])
        writer.writerow(["Placement Rate (%)", placement_rate])
        writer.writerow([])

        writer.writerow(["Job Title", "Applications", "Selected"])

        for job in jobs:
            job_apps = [a for a in applications if a.job_id == job.id]
            job_selected = [a for a in job_apps if a.status == "Selected"]

            writer.writerow([
                job.title,
                len(job_apps),
                len(job_selected)
            ])

        writer.writerow([])
        writer.writerow([
            "Application ID",
            "Student Name",
            "Email",
            "Department",
            "CGPA",
            "Job Title",
            "Status",
            "Interview DateTime"
        ])

        for app_obj in applications:
            student = app_obj.student
            job = app_obj.job

            writer.writerow([
                app_obj.id,
                student.user.name if student else "",
                student.user.email if student else "",
                student.department if student else "",
                student.cgpa if student else "",
                job.title if job else "",
                app_obj.status,
                app_obj.interview_datetime or ""  
            ])

    print("report generated:", filename)
    return filename

@app.route("/company/monthly-report")
@jwt_required()
def company_monthly_report():

    current_user = get_jwt_identity()

    user = User.query.get(int(current_user))
    company = user.company_profile  

    if not company:
        return jsonify({"error": "Company not found"}), 404

    jobs = Job.query.filter_by(company_id=company.id).all()

    applications = Application.query.join(Job).filter(
        Job.company_id == company.id
    ).all()

    total_jobs = len(jobs)
    total_applications = len(applications)

    shortlisted = len([a for a in applications if a.status == "Shortlisted"])
    selected = len([a for a in applications if a.status == "Selected"])

    selection_rate = round((selected / total_applications) * 100, 2) if total_applications else 0

    cgpas = [a.student.cgpa for a in applications if a.student and a.student.cgpa]
    avg_cgpa = round(sum(cgpas)/len(cgpas), 2) if cgpas else 0

    dept_stats = {}
    for app in applications:
        if not app.student:
            continue

        dept = app.student.department
        if dept not in dept_stats:
            dept_stats[dept] = 0

        if app.status == "Selected":
            dept_stats[dept] += 1

    placements = []
    for app in applications:
        if not app.student:
            continue

        placements.append({
            "id": app.id,
            "name": app.student.user.name,
            "email": app.student.user.email,
            "department": app.student.department,
            "cgpa": app.student.cgpa,
            "job": app.job.title if app.job else "",
            "status": app.status,
            "interview_datetime": app.interview_datetime or "-", 
            "feedback": app.feedback or ""
        })

    return jsonify({
        "stats": {
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "selected": selected,
            "selection_rate": selection_rate,
            "avg_cgpa": avg_cgpa
        },
        "department_stats": [{"department": d, "count": c} for d, c in dept_stats.items()],
        "placements": placements
    })

@app.route("/company/reports")
def company_reports():

    applications = Application.query.all()
    jobs = Job.query.all()

    shortlisted = len([a for a in applications if a.status=="Shortlisted"])
    selected = len([a for a in applications if a.status=="Selected"])
    rejected = len([a for a in applications if a.status=="Rejected"])

    return {
        "total_jobs": len(jobs),
        "total_applications": len(applications),
        "shortlisted": shortlisted,
        "selected": selected,
        "rejected": rejected
    }



@celery.task(name="udyog_tasks.export_student_applications")
def export_student_applications(student_id):

    from app import app, Application

    with app.app_context():

        applications = Application.query.filter_by(
            student_id=student_id
        ).all()

        filepath = f"exports/student_{student_id}_applications.csv"

        with open(filepath, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Drive",
                "Company",
                "Status"
            ])

            for app_obj in applications:

                writer.writerow([
                    app_obj.job.title,
                    app_obj.job.company.company_name,
                    app_obj.status
                ])

        return filepath
    



if __name__ == "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)
