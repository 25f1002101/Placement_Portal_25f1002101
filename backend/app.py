from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "placement-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# user model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(20), nullable=False)  # admin / student / company
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
    #one to many relationship one Student can apply to many jobs
    applications = db.relationship(
        "Application",
        back_populates="student"
    )
#CompanyProfile model
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
    #one to many relationship one company can post many jobs
    jobs = db.relationship(
        "Job",
        back_populates="company"
    )
#job model
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    # foriegn key many to one many jobs posted by 1 company
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company_profiles.id")
    )
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    skills = db.Column(db.String(200))
    salary = db.Column(db.String(50))
    job_type = db.Column(db.String(50), default="Full-time")
    is_approved = db.Column(db.Boolean, default=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    # many jobs posted by 1 company
    company = db.relationship("CompanyProfile", back_populates="jobs")
    #one to many one Job can have many Applications
    applications = db.relationship(
        "Application",
        back_populates="job"
    )
#application model
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    # many to one many applications sent for one job
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id")
    )
    # many to one many applications sent by one student
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student_profiles.id")
    )
    status = db.Column(db.String(50), default="Applied")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    remarks = db.Column(db.String(200))
    # many to one many applications sent for one job
    job = db.relationship("Job", back_populates="applications")
    # many to one many applications sent by one student
    student = db.relationship("StudentProfile", back_populates="applications")
    
    #Routing
    #landing page
'''@app.route('/')
def landing():
    return render_template('landing.html') '''

#registeration
@app.route("/register", methods=["POST"])
def register():
    data = request.json                  #stores in dictionary format
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
        is_approved=False if role == "company" else True
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id,
        "role": user.role
    })

#login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "No user found"})
    # correct password check
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Wrong password"})
    # company approval check
    if user.role == "company" and not user.is_approved:
        return jsonify({"error": "Company not approved yet"})
    # set session
    session["user_id"] = user.id
    session["role"] = user.role
    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    })


def init_db():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()
    if not admin:
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


if __name__== "__main__":
    with app.app_context():
        init_db()

    app.run(debug=True)