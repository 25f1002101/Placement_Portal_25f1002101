<template>
  <div class="page">
  <div class="box">
  <h2>Manage Drives</h2>
  <div v-for="d in drives" :key="d.id" class="card">
  <p><b>{{ d.title }}</b></p>
  <p>{{ d.location }}</p>
  <p>Status: {{ d.is_close ? "Closed" : "Open" }}</p>
  <div class="button-row">
  <button v-if="!d.is_close" @click="closeDrive(d.id)" class="danger">Close</button>
  <button v-else @click="openDrive(d.id)">Reopen</button>
  <button @click="openEdit(d)">Edit</button>
  </div>
  </div>
  <div v-if="editMode" class="modal">
  <div class="modal-box">
  <h3>Edit Drive</h3>
  <input v-model="form.title" placeholder="Title" />
  <input v-model="form.location" placeholder="Location" />
  <input v-model="form.salary" placeholder="Salary" />
  <textarea v-model="form.description" placeholder="Description"></textarea>
  <input v-model="form.skills" placeholder="Skills" />
  <input v-model="form.eligibility" placeholder="Eligibility" />
  <input v-model="form.deadline" type="date" />
  <div class="button-row">
  <button @click="updateDrive">Save</button>
  <button class="danger" @click="editMode=false">Cancel</button>
  </div>
  </div>
  </div>
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
  drives: [],
  editMode: false,
  form: {
  id: null,
  title: "",
  location: "",
  salary: "",
  description: "",
  skills: "",
  eligibility: "",
  deadline: ""
  }
  };
  },
  mounted() {
  this.fetchDrives();
  },
  methods: {
  fetchDrives() {
  api.get("/company/my_drives").then(res => {
  this.drives = res.data;
  });
  },
  closeDrive(id) {
  api.post(`/company/close_drive/${id}`).then(() => {
  this.fetchDrives();
  });
  },
  openDrive(id) {
  api.post(`/company/open_drive/${id}`).then(() => {
  this.fetchDrives();
  });
  },
  openEdit(d) {
  this.form = { ...d };
  this.editMode = true;
  },
  updateDrive() {
  api.put(`/company/update_drive/${this.form.id}`, this.form).then(() => {
  this.editMode = false;
  this.fetchDrives();
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
    background:#f3e2dc;
  }
  .box{
    width:420px;
    background:#fff;
    padding:20px;
    border-radius:8px;
  }
  .card{
    background:#f0d8d1;
    padding:8px;
    margin-top:10px;
  }
  .button-row{
    display:flex;
    gap:6px;
    margin-top:8px;
  }
  button{
    flex:1;
    padding:7px;
    border:none;
    border-radius:5px;
    background:#c08478;
    color:#fff;
  }
  .danger{
    background:#a45a5a;
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
    width:300px;
  }
  input,textarea{
    width:100%;
    margin:5px 0;
    padding:6px;
    border:1px solid #d6b8ae;
  }
  .back-btn{
    width:100%;
    margin-top:10px;
    padding:8px;
    background:#a45a5a;
    color:#fff;
    border:none;
    border-radius:5px;
  }
  </style>