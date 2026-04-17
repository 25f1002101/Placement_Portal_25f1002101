<template>
  <div class="page">
    <div class="box">
      <h2>Student Dashboard</h2>

      <p v-if="profile">
        {{ profile.name }} | {{ profile.department }}
      </p>

     <button 
  v-if="profile && profile.resume_url" 
  @click="viewResume(profile.resume_url)"
>
  View Resume
</button>

      <div class="buttons">
        <button @click="$router.push('/student/profile')">Profile</button>
        <button @click="$router.push('/student/applications')">Applications</button>
        <button @click="logout">Logout</button>
      </div>

      <input v-model="search" placeholder="Search jobs" class="search" />

      <div v-for="job in filteredJobs" :key="job.id" class="card">
        <h3>{{ job.title }}</h3>
        <p>{{ job.company }}</p>
        <p>{{ job.location }}</p>

        <button @click="viewJob(job)">View More</button>


        <button v-if="!job.applied" @click="apply(job.id)">
          Apply
        </button>

        <button v-else disabled>Applied</button>
      </div>

      <div v-if="selectedJob" class="modal">
        <div class="modal-box">
          <h3>{{ selectedJob.title }}</h3>
          <p>{{ selectedJob.description }}</p>
          <p>{{ selectedJob.skills }}</p>
          <p>{{ selectedJob.salary }}</p>

          <button @click="selectedJob = null">Close</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      jobs: [],
      profile: null,
      search: "",
      selectedJob: null
    };
  },

  computed: {
    filteredJobs() {
      return this.jobs.filter(j =>
        j.title.toLowerCase().includes(this.search.toLowerCase())
      );
    }
  },

  mounted() {
    console.log("Component mounted");
    this.loadData();
  },

  methods: {
    async loadData() {
      console.log("Loading all data...");
      await this.getProfile();
      await this.getJobs();
      await this.getApplications();
      console.log("Final jobs after mapping:", this.jobs);
    },

    logout() {
      console.log("Logging out...");
      localStorage.removeItem("token");
      this.$router.push("/login");
    },

    // profile
    getProfile() {
      return api.get("/student/profile").then(r => {
        console.log("Profile response:", r.data);
        this.profile = r.data;
      });
    },

    // jobs
    getJobs() {
      return api.get("/student/jobs").then(r => {
        console.log("Jobs response:", r.data);

        this.jobs = r.data;

        this.jobs.forEach(j => {
          j.applied = false;
        });

        console.log("Jobs after adding applied flag:", this.jobs);
      });
    },

    // applications
    getApplications() {
      return api.get("/student/applications").then(r => {
        console.log("Applications response:", r.data);

        const appliedIds = r.data.map(a => {
          console.log("Mapping application:", a);
          return a.job_id; 
        });

        console.log("Applied job IDs:", appliedIds);

        this.jobs.forEach(j => {
          if (appliedIds.includes(j.id)) {
            console.log("Marking as applied:", j.id);
            j.applied = true;
          }
        });

        console.log("Jobs after applying mapping:", this.jobs);
      });
    },

    // apply
    apply(id) {
      console.log("Applying for job ID:", id);

      api.post(`/student/apply/${id}`)
        .then(res => {
          console.log("Apply response:", res.data);

          const job = this.jobs.find(j => j.id === id);

          if (job) {
            console.log("Updating UI for job:", job);
            job.applied = true;
          } else {
            console.log("Job not found in list!");
          }

       
          this.getApplications();
        })
        .catch(err => {
          console.error("Apply error:", err);
          alert("Error applying job");
        });
    },

    viewJob(job) {
      console.log("Viewing job:", job);
      this.selectedJob = job;     
    },

  viewResume(url) {
    console.log(url)
  if (!url) {
    alert("No resume found");
    return;
  }

  window.open(url, "_blank");
}
  }
};
</script>

<style scoped>
.page{
  min-height:100vh;
  width:100%;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  background:#f3e2dc;
  padding:20px;
}
.box{
  width:100%;
  max-width:1100px;
  background:#fff;
  padding:20px;
  border-radius:8px;
}
.buttons{
  display:flex;
  gap:8px;
  margin:10px 0;
}
button{
  padding:7px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:5px;
}
.search{
  width:100%;
  padding:8px;
  margin:10px 0;
  border:1px solid #d6b8ae;
}
.card{
  background:#f0d8d1;
  padding:10px;
  margin-top:10px;
}
.modal{
  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background:rgba(0,0,0,0.4);
  display:flex;
  justify-content:center;
  align-items:center;
}
.modal-box{
  width:50%;
  min-height:50vh;
  background:#fff;
  padding:15px;
}
</style>