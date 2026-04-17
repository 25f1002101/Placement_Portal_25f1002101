<template>
    <div class="page">
      <div class="box">
        <h2>Companies</h2>
        <div v-for="c in companies" :key="c.id" class="card">
          <p><b>{{ c.name }}</b></p>
          <p>{{ c.email }}</p>
          <p>Status: {{ c.is_approved ? "Approved" : "Rejected" }}</p>
  
          <div class="button-row">
            <button @click="approve(c.id)">Approve</button>
            <button @click="reject(c.id)">Reject</button>
          </div>
        </div>
        <button class="back-btn" @click="$router.push('/admin')">
          Go Back to Dashboard
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../services/api";
  
  export default {
    data() {
      return { companies: [] };
    },
  
    mounted() {
      api.get("/admin/companies").then(res => {
        this.companies = res.data;
      });
    },
  
    methods: {
      approve(id) {
        api.post(`/admin/company/${id}/approve`).then(() => location.reload());
      },
      reject(id) {
        api.post(`/admin/company/${id}/reject`).then(() => location.reload());
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
  .back-btn{
    width:100%;
    margin-bottom:10px;
    padding:8px;
    background:#a45a5a;
    color:#fff;
    border:none;
    border-radius:5px;
  }
  .card{
    background:#f0d8d1;
    padding:8px;
    margin-top:10px;
  }
  .button-row{
    display:flex;
    gap:8px;
  }
  button{
    flex:1;
    padding:8px;
    background:#c08478;
    color:#fff;
    border:none;
    border-radius:5px;
  }
  </style>