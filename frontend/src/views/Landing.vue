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
.landing{
  min-height:100vh;
  width:100%;
  background:#f3e2dc;
  color:#5a3a3a;
  font-family:Arial,Helvetica,sans-serif;
  display:flex;
  flex-direction:column;
}
.header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:20px 60px;
  background:#ead2ca;
  border-bottom:1px solid #d6b8ae;
}
.logo{
  font-size:22px;
  font-weight:600;
}
.nav a{
  margin-left:20px;
  text-decoration:none;
  font-size:14px;
  color:#5a3a3a;
}
.btn-primary{
  background:#c08478;
  color:#fff!important;
  padding:10px 20px;
  border-radius:6px;
  text-decoration:none;
  font-size:14px;
}
.hero{
  background:#f0d8d1;
  border-radius:10px;
  text-align:center;
  padding:70px 20px;
  max-width:800px;
  margin:40px auto;
}
.hero h2{
  font-size:34px;
  margin-bottom:15px;
}
.hero p{
  font-size:15px;
  color:#7a5a5a;
  margin-bottom:30px;
}
.hero-buttons{
  display:flex;
  justify-content:center;
  gap:15px;
}
.btn-secondary{
  padding:10px 20px;
  border-radius:6px;
  text-decoration:none;
  font-size:14px;
  border:1px solid #d6b8ae;
  color:#7a5a5a;
  background:#fff;
}
.features{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:20px;
  padding:40px 60px;
}
.feature-card{
  background:#fff;
  padding:25px;
  border-radius:8px;
  border:1px solid #e6ccc5;
  border-top:3px solid #c08478;
}
.feature-card h3{
  margin-bottom:8px;
  font-size:17px;
}
.feature-card p{
  font-size:14px;
  color:#7a5a5a;
}
.footer{
  margin-top:auto;
  text-align:center;
  padding:15px;
  font-size:13px;
  color:#7a5a5a;
  border-top:1px solid #e6ccc5;
}
</style>

