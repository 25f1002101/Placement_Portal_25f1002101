<template>
  <div class="page">
    <div class="box">
      <h2>Student Profile</h2>

      <input v-model="profile.department" placeholder="Department" />
      <input v-model="profile.year" placeholder="Year" />
      <input v-model="profile.cgpa" placeholder="CGPA" />
      <input v-model="profile.skills" placeholder="Skills" />
      <input type="file" accept="application/pdf" @change="handleFile" />
      <button @click="saveProfile">Save</button>
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
      profile: {},
      resume: null
    };
  },

  mounted() {
    api.get("/student/profile").then(res => {
      this.profile = res.data.exists ? res.data : {};
    });
  },

  methods: {
    handleFile(e) {
      this.resume = e.target.files[0];
    },

    saveProfile() {
      const formData = new FormData();

      formData.append("department", this.profile.department);
      formData.append("year", this.profile.year);
      formData.append("cgpa", this.profile.cgpa);
      formData.append("skills", this.profile.skills);

      if (this.resume) {
        formData.append("resume", this.resume);
      }

      api.post("/student/profile", formData).then(() => {
        this.$router.push("/student-dashboard");
      });
    }
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
  width:380px;
  background:#fff;
  padding:20px;
  border-radius:8px;
}
input{
  width:100%;
  margin-top:10px;
  padding:8px;
  border:1px solid #d6b8ae;
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
.back-btn{
  background:#a45a5a;
}
</style>