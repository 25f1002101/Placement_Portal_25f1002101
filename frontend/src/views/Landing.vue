<template>
  <div class="landing">
    <header class="header">
      <h1 class="logo">Placement Portal</h1>
      <nav class="nav">
        <router-link to="/login" class="btn-primary">Login</router-link>
        <router-link to="/register" class="btn-primary">Register</router-link>
      </nav>
    </header>
    <section class="hero">
      <h2>Your Gateway to Career Opportunities</h2>
      <p>
        Manage placements, track applications, and connect students with top
        recruiters — all in one place.
      </p>
      <div class="hero-buttons">
        <router-link to="/register" class="btn-primary">
          Get Started
        </router-link>
        <router-link to="/login" class="btn-secondary">
          Already have an account?
        </router-link>
      </div>
    </section>
    <section class="features">
      <div class="feature-card">
        <h3>For Students</h3>
        <p>Apply for jobs, track status, and get notified instantly.</p>
      </div>
      <div class="feature-card">
        <h3>For Recruiters</h3>
        <p>Post openings and shortlist candidates efficiently.</p>
      </div>
      <div class="feature-card">
        <h3>For Admins</h3>
        <p>Manage drives, users, and reports from a single dashboard.</p>
      </div>
    </section>
    <footer class="footer">
      <p> 2026 Placement Portal. All rights reserved.</p>
    </footer>
  </div>
</template>
<script>
export default {
  name: "Landing",
};
</script>
<style scoped>
.landing {
  min-height: 100vh;
  width: 100%;
  background-color: #f8fafc;
  color: #1f2933;
  font-family: Arial, Helvetica, sans-serif;
  display: flex;
  flex-direction: column;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
  background-color: #eaf1ff;
  border-bottom: 1px solid #c7d2fe;
}
.logo {
  font-size: 22px;
  font-weight: 600;
  color: #1e3a8a;
}
.nav a {
  margin-left: 20px;
  text-decoration: none;
  font-size: 14px;
  color: #1e3a8a;
}
.btn-primary {
  background-color: #2563eb;
  color: #ffffff !important;
  padding: 10px 22px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
}
.hero {
  background-color: #eef2ff;
  border-radius: 12px;
  text-align: center;
  padding: 80px 20px;
  max-width: 800px;
  margin: 40px auto;
}
.hero h2 {
  font-size: 36px;
  margin-bottom: 16px;
  color: #4338ca;
}
.hero p {
  font-size: 16px;
  color: #6b7280;
  margin-bottom: 32px;
}
.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}
.btn-secondary {
  padding: 10px 22px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
  border: 1px solid #c7d2fe;
  color: #4338ca;
  background-color: #ffffff;
}
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  padding: 40px 60px;
}
.feature-card {
  background-color: #ffffff;
  padding: 28px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  border-top: 3px solid #2563eb;
}
.feature-card h3 {
  margin-bottom: 8px;
  font-size: 18px;
}
.feature-card p {
  font-size: 14px;
  color: #6b7280;
}
.footer {
  margin-top: auto;
  text-align: center;
  padding: 16px;
  font-size: 13px;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
}
</style>

