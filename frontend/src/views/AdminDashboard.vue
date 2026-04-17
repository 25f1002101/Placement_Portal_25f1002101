<template>
  <div class="page">
    <div class="nav">
      <h2>Admin Dashboard</h2>
      <div class="nav-btns">
        <button @click="$router.push('/admin/companies')">Companies</button>
        <button @click="$router.push('/admin/drives')">Drives</button>
        <button @click="$router.push('/admin/applications')">Applications</button>
        <button class="logout" @click="logout">Logout</button>
      </div>
    </div>
    <div class="box">
      <input
        v-model="query"
        @input="handleSearch"
        placeholder="Search students or companies..."
        class="search-box"
      />
      <div v-if="loading" class="center">Searching...</div>
      <div v-else-if="query.length > 0" class="results">
        <h3>Students</h3>
        <div v-if="results.students.length === 0" class="empty">
          No students found
        </div>
        <div class="grid">
          <div v-for="s in results.students" :key="s.id" class="card">
            {{ s.name }}
          </div>
        </div>
        <h3>Companies</h3>
        <div v-if="results.companies.length === 0" class="empty">
          No companies found
        </div>
        <div class="grid">
          <div v-for="c in results.companies" :key="c.id" class="card">
            {{ c.name }}
          </div>
        </div>
      </div>
      <div v-else class="grid stats">
        <div class="card big"> Students <br /> {{ data.total_students || 0 }}</div>
        <div class="card big"> Companies <br /> {{ data.total_companies || 0 }}</div>
        <div class="card big"> Drives <br /> {{ data.total_drives || 0 }}</div>
      </div>
    </div>
  </div>
</template>
<script>
import api from "../services/api";
export default {
  data() {
    return {
      data: {},
      query: "",
      loading: false,
      // simple debounce timer
      timer: null,
      results: {
        students: [],
        companies: []
      }
    };
  },
  mounted() {
    // load dashboard numbers
    api.get("/admin/dashboard").then(res => {
      this.data = res.data;
    });
  },

  methods: {
    handleSearch() {
      clearTimeout(this.timer);

      // debounce so api not hit every key
      this.timer = setTimeout(() => {
        this.search();
      }, 400);
    },

    search() {
      if (!this.query.trim()) {
        this.results = { students: [], companies: [] };
        return;
      }

      this.loading = true;

      api
        .get(`/admin/search?q=${this.query}`)
        .then(res => {
          this.results = res.data;
        })
        .catch(() => {
          this.results = { students: [], companies: [] };
        })
        .finally(() => {
          this.loading = false;
        });
    },

    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.page{
  min-height:100vh;
  background:#f3e2dc;
  padding:20px;
}
.nav{
  display:flex;
  justify-content:space-between;
  margin-bottom:20px;
  color:#5a3a3a;
}
.nav-btns{
  display:flex;
  gap:8px;
}
.box{
  background:#fff;
  padding:15px;
  border-radius:8px;
  max-width:900px;
  margin:auto;
}
button{
  padding:6px 10px;
  background:#c08478;
  color:#fff;
  border:none;
  border-radius:5px;
}
.logout{
  background:#a45a5a;
}
.search-box{
  width:100%;
  padding:8px;
  margin-bottom:10px;
  border:1px solid #d6b8ae;
}
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
  gap:8px;
}
.card{
  background:#f0d8d1;
  padding:8px;
}
.big{
  text-align:center;
}
.results h3{
  margin-top:10px;
}
.empty{
  font-size:13px;
}
.center{
  text-align:center;
}
</style>