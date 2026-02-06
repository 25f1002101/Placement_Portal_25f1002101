<template>
  <div class="login-container">
    <form @submit.prevent="loginUser">
      <h2>Login</h2>
      
      <input
        type="email"
        placeholder="Email"
        v-model="email"
        required
      />
      <input
        type="password"
        placeholder="Password"
        v-model="password"
        required
      />
      
      <button type="submit">Login</button>
      
      <p class="message">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",

  data() {
    return {
      email: "",
      password: "",
      message: "",
    };
  },

  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://localhost:5000/login", {
          email: this.email,
          password: this.password,
        });

        this.message = response.data.message;
      } catch (error) {
        this.message = "Login failed. Check your email or password.";
      }
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #1e40af 100%);
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

form {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 48px 40px;
  border-radius: 20px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h2 {
  text-align: center;
  color: #1e3a8a;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

input {
  padding: 16px 20px;
  border: 1px solid rgba(59, 130, 246, 0.4);
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.8);
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: white;
}

button {
  padding: 16px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
}

.message {
  text-align: center;
  font-size: 14px;
  color: #dc2626;
  margin-top: 4px;
}

@media (max-width: 480px) {
  form {
    padding: 32px 24px;
    margin: 16px;
  }
}
</style>
