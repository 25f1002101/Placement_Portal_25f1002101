<template>
    <!--shows company + jobs to students (student dashboard ka part hai )-->
    <div class="page">
      <div class="box">
        <h2>{{ data.company?.name }}</h2>
        <p>{{ data.company?.industry }}</p>
        <p>{{ data.company?.location }}</p>
  
        <h3>Jobs</h3>
  
        <div v-for="j in data.jobs" :key="j.id" class="card">
          <p><b>{{ j.title }}</b></p>
          <p>{{ j.description }}</p>
          <p>{{ j.salary }}</p>
  
          <button @click="apply(j.id)">Apply</button>
        </div>
  
        <button @click="$router.back()">Go Back</button>
      </div>
    </div>
  </template>
  
  <script>
  import api from "../services/api";
  
  export default {
    data() {
      return {
        data: { jobs: [] }
      };
    },
    mounted() {
      const id = this.$route.params.id;
  
      api.get(`/student/company/${id}`)
        .then(res => this.data = res.data);
    },
    methods: {
      apply(id) {
        api.post(`/student/apply/${id}`)
          .then(() => alert("Applied"));
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