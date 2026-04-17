<template>
  <div class="page">
    <div class="box">
      <h2>Create Drive</h2>
      <form @submit.prevent="createDrive">
        <input v-model="title" placeholder="Title" required />
        <input v-model="skills" placeholder="Skills" />
        <input v-model="salary" placeholder="Salary" />
        <input v-model="location" placeholder="Location" />
        <input v-model="eligibility" placeholder="Eligibility" />
        <input type="date" v-model="deadline" />
        <textarea v-model="description" placeholder="Description"></textarea>
        <button>Create</button>
      </form>
      <button class="back-btn" @click="$router.push('/company_dashboard')">
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
      title: "",
      description: "",
      skills: "",
      salary: "",
      location: "",
      eligibility: "",
      deadline: ""
    };
  },
  methods: {
    createDrive() {
      api.post("/company/create_drive", this.$data)
        .then(() => {
          alert("Drive created");
          this.$router.push("/company_dashboard");
        });
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
  width:380px;
  background:#fff;
  padding:20px;
  border-radius:8px;
}
input,textarea{
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