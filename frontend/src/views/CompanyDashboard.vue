<template>
  <div class="page">
    <div class="box">
      <h2>Company Dashboard</h2>

      <div class="card">
        <p><b>{{ data.company_name || "No Name" }}</b></p>
        <p>{{ data.industry || "No Industry" }}</p>
        <p>{{ data.website || "No Website" }}</p>
      </div>


      <div class="button-row">
        <button @click="$router.push('/company/profile')">Company Profile</button>
        <button @click="$router.push('/company/drives')">Manage Drives</button>
      </div>


      <h3>Analytics</h3>
      <div class="stats">
        <div class="stat-card">
          <p>Total Jobs</p>
          <h4>{{ stats.total_jobs || 0 }}</h4>
        </div>
        <div class="stat-card">
          <p>Applications</p>
          <h4>{{ stats.total_applications || 0 }}</h4>
        </div>
        <div class="stat-card">
          <p>Shortlisted</p>
          <h4>{{ stats.shortlisted || 0 }}</h4>
        </div>
        <div class="stat-card">
          <p>Selected</p>
          <h4>{{ stats.selected || 0 }}</h4>
        </div>
        <div class="stat-card">
          <p>Rejected</p>
          <h4>{{ stats.rejected || 0 }}</h4>
        </div>
      </div>


      <button @click="downloadReport" :disabled="reportLoading">
        {{ reportLoading ? reportStatusMsg : "Download Report" }}
      </button>

      <h3>Your Drives</h3>
      <div v-for="d in data.drives" :key="d.id" class="card">
        <p><b>{{ d.title }}</b></p>
        <p>Applicants: {{ d.applicants_count }}</p>
        <p>Status: {{ d.is_close ? "Closed" : "Open" }}</p>
        <div class="button-row">
          <button @click="goToApplicants(d.id)">Applicants</button>
        </div>
      </div>

      <button @click="$router.push('/company/create-drive')">Create Drive</button>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      data: { drives: [] },
      stats: {},

      // report stuff
      reportLoading: false,
      reportStatusMsg: "Generating...",
      pollInterval: null,
    };
  },

  mounted() {
    api
      .get("/company/get_profile")
      .then(() => {
        this.fetchDashboard();
      })
      .catch(() => {
        this.$router.push("/company/profile");
      });
  },

  beforeUnmount() {

    if (this.pollInterval) {
      clearInterval(this.pollInterval);
      this.pollInterval = null;
    }
  },

  methods: {


    fetchDashboard() {
      api.get("/company/dashboard")
        .then((res) => {
          this.data = res.data;
        })
        .catch(() => {
          alert("Error loading dashboard");
        });

      api.get("/company/reports")
        .then((res) => {
          this.stats = res.data;
        })
        .catch(() => {
          console.log("stats error");
        });
    },

    goToApplicants(id) {
      this.$router.push(`/company/applications/${id}`);
    },
    async downloadReport() {

      // prevent double click
      if (this.reportLoading) return;

      this.reportLoading = true;
      this.reportStatusMsg = "Generating...";

      try {

        const res = await api.get("/admin/generate-report");

        const taskId = res.data.task_id;

        if (!taskId) {
          alert("Task not created properly");
          this.reportLoading = false;
          return;
        }

        if (this.pollInterval) {
          clearInterval(this.pollInterval);
          this.pollInterval = null;
        }


        this.startPolling(taskId);

      } catch (err) {
        console.log(err);
        alert("Failed to start report");
        this.reportLoading = false;
      }
    },


    startPolling(taskId) {

      this.pollInterval = setInterval(async () => {

        try {

          const res = await api.get(`/admin/report-status/${taskId}`);

          const status = res.data.status;
          const downloadUrl = res.data.download_url;


          if (status === "done") {

            clearInterval(this.pollInterval);
            this.pollInterval = null;

            this.reportLoading = false;
            this.reportStatusMsg = "Download Report";


            window.open(`http://127.0.0.1:5000${downloadUrl}`, "_blank");
          }


          else if (status === "failed") {

            clearInterval(this.pollInterval);
            this.pollInterval = null;

            this.reportLoading = false;
            alert("Report failed. Check backend logs.");
          }


          else {
            this.reportStatusMsg = "Please wait...";
          }

        } catch (err) {

          clearInterval(this.pollInterval);
          this.pollInterval = null;

          this.reportLoading = false;
          alert("Error while checking report status");
        }

      }, 2000); // every 2 sec
    },

    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.page{
  display:flex;
  justify-content:center;
  align-items:center;
  min-height:100vh;
  background:#f3e2dc;
}
.box{
  width:400px;
  background:#fff;
  padding:20px;
  border-radius:8px;
}
.card{
  background:#f0d8d1;
  padding:10px;
  margin-top:10px;
}
button{
  width:100%;
  margin-top:10px;
  padding:8px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:5px;
}
</style>