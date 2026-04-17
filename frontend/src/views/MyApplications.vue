<template>
  <div class="page">
    <div class="box">
      <h2>My Applications</h2>

      <div v-for="a in apps" :key="a.id" class="card">
        <p><b>{{ a.job_title }}</b></p>
        <p>{{ a.company }}</p>

        <p>Status: {{ a.status }}</p>

        <p v-if="a.status === 'Rejected' && a.feedback" class="reject">
          Rejected: {{ a.feedback }}
        </p>

        <div v-if="a.status === 'Shortlisted'" class="shortlist">
          <p>Interview: {{ a.interview_datetime }}</p>
          <p>Mode: {{ a.interview_mode }}</p>

          <a
            v-if="a.interview_link"
            :href="a.interview_link"
            target="_blank"
          >
            Join Interview
          </a>
        </div>

        <p v-if="a.status === 'Selected'" class="selected">
          You are Selected
        </p>

        <p v-if="a.remarks && a.status !== 'Selected'">
          {{ a.remarks }}
        </p>
      </div>

      <button class="back-btn" @click="$router.push('/student-dashboard')">
        Back to Dashboard
      </button>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      apps: []
    };
  },

  mounted() {
    api.get("/student/applications")
      .then(res => {
        this.apps = res.data;
      });
  }
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
.reject{
  color:#a45a5a;
}
.shortlist{
  background:#ead2ca;
  padding:6px;
  margin-top:5px;
}
.selected{
  color:#5a3a3a;
}
.back-btn{
  width:100%;
  margin-top:10px;
  padding:8px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:5px;
}
</style>