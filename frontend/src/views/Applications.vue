<template>
  <!--company side -->
  <div class="page">
    <div class="box">
      <h2>Applicants</h2>

      <button class="back-btn" @click="$router.push('/company_dashboard')">
        Back to Dashboard
      </button>
      <div v-for="a in apps" :key="a.application_id" class="card">
        <p><b>{{ a.student_name }}</b></p>
        <p>{{ a.department }}</p>
        <p>CGPA: {{ a.cgpa }}</p>
        <p>Status: {{ a.status }}</p>

        <a
        v-if="a.resume_url"
        :href="a.resume_url"
        target="_blank"
        >
        View Resume
        </a>

        <div class="button-row">
          <button @click="viewApplicant(a)">View More</button>

          <button @click="shortlist(a)">Shortlist</button>

          <button @click="reject(a)">Reject</button>

          <button @click="accept(a)">Accept</button>
        </div>
      </div>


      <div v-if="selectedApplicant" class="modal">
        <div class="modal-box">
          <h3>{{ selectedApplicant.student_name }}</h3>
          <p>Department: {{ selectedApplicant.department }}</p>
          <p>CGPA: {{ selectedApplicant.cgpa }}</p>
          <p>Status: {{ selectedApplicant.status }}</p>

          <a
            v-if="selectedApplicant.resume"
            :href="`http://localhost:5000/uploads/${selectedApplicant.resume}`"
            target="_blank"
          >
            View Resume
          </a>

          <button @click="selectedApplicant = null">Close</button>
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
      apps: [],
      selectedApplicant: null
    };
  },

  mounted() {
    const id = this.$route.params.id;

    api.get(`/company/drive/${id}/applications`)
      .then(res => {
        this.apps = res.data;
      });
  },

  methods: {
    update(id, payload) {
      api.post(`/company/application/${id}/update`, payload)
        .then(() => {
          location.reload();
        });
    },

    shortlist(a) {
      const datetime = prompt("Enter Interview Date & Time (YYYY-MM-DD HH:MM)");
      const mode = prompt("Enter Mode (Online/Offline)");
      const link = prompt("Enter Meeting Link (if online)");

      this.update(a.application_id, {
        status: "Shortlisted",
        interview_datetime: datetime,
        interview_mode: mode,
        interview_link: link
      });
    },

    reject(a) {
      const feedback = prompt("Enter reason for rejection");

      this.update(a.application_id, {
        status: "Rejected",
        feedback: feedback
      });
    },

    accept(a) {
      this.update(a.application_id, {
        status: "Selected"
      });
    },

    viewApplicant(a) {
      this.selectedApplicant = a;
    }
  }
};
</script>

<style scoped>
.page{
  min-height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
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
.button-row{
  display:flex;
  gap:6px;
  margin-top:8px;
  flex-wrap:wrap;
}
button{
  flex:1;
  padding:8px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:5px;
  font-size:13px;
}
.back-btn{
  width:100%;
  margin-bottom:10px;
  padding:8px;
  background:#a45a5a;
  color:#fff;
  border:none;
  border-radius:5px;
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
  background:#fff;
  padding:15px;
  border-radius:8px;
  width:280px;
}
</style>