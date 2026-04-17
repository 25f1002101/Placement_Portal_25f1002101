<template>
  <div class="page">
    <div class="box">
      <h2>Register</h2>

      <form @submit.prevent="registerUser">
        <label>Name</label>
        <input v-model="name" required />

        <label>Email</label>
        <input type="email" v-model="email" required />

        <label>Password</label>
        <input type="password" v-model="password" required />

        <label>Role</label>
        <select v-model="role" required>
          <option value="">Select</option>
          <option value="student">Student</option>
          <option value="company">Company</option>
        </select>

        <button>Register</button>
      </form>

      <p class="link">
        Already have an account?
        <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>


<script>
import api from "../services/api";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      role: ""
    };
  },
  methods: {
    registerUser() {
      api.post("/register", {
        name: this.name,
        email: this.email,
        password: this.password,
        role: this.role
      })
      .then(() => {
        alert("Registration successful. Please login.");
        this.$router.push("/login");
      })
      .catch(err => {
        alert(err.response.data.msg);
      });
    }
  }
};
</script>
<style scoped>
.page{
  min-height:100vh;
  width:100%;
  background:#f3e2dc;
  display:flex;
  align-items:center;
  justify-content:center;
}
.box{
  width:380px;
  background:#fff;
  padding:25px;
  border-radius:10px;
  font-family:Arial,Helvetica,sans-serif;
}
h2{
  text-align:center;
  margin-bottom:20px;
  color:#5a3a3a;
}
label{
  display:block;
  margin-top:12px;
  font-size:14px;
  color:#5a3a3a;
}
input,select{
  width:100%;
  padding:10px;
  margin-top:5px;
  border-radius:6px;
  border:1px solid #d6b8ae;
  font-size:14px;
}
button{
  width:100%;
  margin-top:20px;
  padding:10px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:6px;
  font-size:14px;
}
.link{
  margin-top:15px;
  text-align:center;
  font-size:14px;
  color:#7a5a5a;
}
.link a{
  color:#c08478;
  text-decoration:none;
}
</style>