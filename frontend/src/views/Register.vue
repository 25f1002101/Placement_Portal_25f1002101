<template>
    <div class="register-container">
      <h2>Create Account</h2>
      <form @submit.prevent="registerUser">
        <input type="text" placeholder="Name" v-model="name" required />
        <input type="email" placeholder="Email" v-model="email" required />
        <input type="password" placeholder="Password" v-model="password" required />
        <select v-model="role" required>
          <option disabled value="">Select role</option>
          <option value="student">Student</option>
          <option value="company">Company</option>
          <option value="admin">Admin</option>
        </select>
        <input type="text" placeholder="Phone (optional)" v-model="phone" />
  
        <button type="submit">Register</button>
      </form>
      <p class="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "Register",
  
    data() {
      return {
        name: "",
        email: "",
        password: "",
        role: "",
        phone: "",
        message: "",
      };
    },
  
    methods: {
      async registerUser() {
        try {
          const response = await axios.post("http://localhost:5000/register", {
            name: this.name,
            email: this.email,
            password: this.password,
            role: this.role,
            phone: this.phone,
          });
  
          this.message = response.data.message;
        } catch (error) {
          this.message = "Something went wrong. Please try again.";
        }
      },
    },
  };
  </script>
  <style>
.register-container {
  max-width: 420px;
  margin: 80px auto;
  padding: 32px;
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  font-family: Arial, Helvetica, sans-serif;
}
.register-container h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #1e3a8a;
  font-size: 24px;
}
.register-container form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.register-container input,
.register-container select {
  padding: 10px 12px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  outline: none;
}
.register-container input:focus,
.register-container select:focus {
  border-color: #2563eb;
}
.register-container button {
  margin-top: 10px;
  padding: 10px;
  background-color: #2563eb;
  color: #ffffff;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.register-container button:hover {
  background-color: #1e40af;
}
.message {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: #374151;
}
  </style>
  