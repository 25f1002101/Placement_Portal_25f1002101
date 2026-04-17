<template>
    <div class="page">
      <div class="box">
        <h2>Drives</h2>
        <div v-for="d in drives" :key="d.id" class="card">
          <p><b>{{ d.title }}</b></p>
          <p>{{ d.company }}</p>
          <p>Status: {{ d.is_approved ? "Approved" : "Rejected" }}</p>
          <div class="button-row">
            <button @click="approve(d.id)">Approve</button>
            <button @click="reject(d.id)">Reject</button>
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
      return { drives: [] };
    },
  
    mounted() {
      api.get("/admin/drives").then(res => {
        this.drives = res.data;
      });
    },
  
    methods: {
      approve(id) {
        api.post(`/admin/drive/${id}/approve`).then(() => location.reload());
      },
      reject(id) {
        api.post(`/admin/drive/${id}/reject`).then(() => location.reload());
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