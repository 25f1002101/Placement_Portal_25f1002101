<template>
    <div class="page">
      <div class="box">
        <h2>Applications</h2>
        <div v-for="a in apps" :key="a.id" class="card">
          <p><b>{{ a.student }}</b></p>
          <p>{{ a.company }}</p>
          <p>{{ a.job }}</p>
          <p>Status: {{ a.status }}</p>
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
      return { apps: [] };
    },
  
    mounted() {
      api.get("/admin/applications").then(res => {
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
  </style>