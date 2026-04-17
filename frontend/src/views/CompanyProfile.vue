<template>
    <div class="page">
      <div class="box">
        <h2>Create Company Profile</h2>
  
        <form @submit.prevent="createProfile">
          <input v-model="company_name" placeholder="Company Name" required />
          <input v-model="industry" placeholder="Industry" />
          <input v-model="website" placeholder="Website" />
          <input v-model="location" placeholder="Location" />
          <input v-model="company_size" placeholder="Company Size" />
  
          <button>Create Profile</button>
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
        company_name: "",
        industry: "",
        website: "",
        location: "",
        company_size: ""
      };
    },
    methods: {
      createProfile() {
        api.post("/company/create_profile", this.$data)
          .then(() => {
            alert("Profile created");
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