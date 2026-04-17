<template>
  <div class="page">
    <div class="box">
      <h2>Login</h2>

      <form @submit.prevent="loginUser">
        <label>Email</label>
        <input type="email" v-model="email" required />

        <label>Password</label>
        <input type="password" v-model="password" required />

        <button>Login</button>
      </form>

      <p class="link">
        New user?
        <router-link to="/register">Register</router-link>
      </p>
      <button class="back-btn" @click="$router.push('/')">
        Back to Home
      </button>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {

      email: "",      // user email input
      password: ""    // user password input

    };
  },

  methods: {
    loginUser() {
      // basic check
      if (!this.email || !this.password) {
        alert("Please enter email and password");
        return;
      }
      // send login request to backend
      api.post("/login", {
        email: this.email,
        password: this.password
      })
      .then(response => {
        console.log("login success", response.data);
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("role", response.data.role);

        if (response.data.role === "company") {
          this.$router.push("/company_dashboard");
        } else if (response.data.role === "student") {
          this.$router.push("/student-dashboard");
        } else if (response.data.role === "admin") {
          this.$router.push("/admin");
        }
      })
      .catch(error => {
        console.log("login error", error);

        // backend sent an error message
        if (error.response && error.response.data) {
          alert(error.response.data.msg);
        } 
        else {
          // server not running / network issue
          alert("Server not reachable. Is Flask running?");
        }
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
  width:360px;
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
input{
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