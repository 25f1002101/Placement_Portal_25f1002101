import { createRouter, createWebHistory } from "vue-router";
const routes = [
  { path: "/", component: () => import("./views/Landing.vue") },
  { path: "/login", component: () => import("./views/Login.vue") },
  { path: "/register", component: () => import("./views/Register.vue") },
  { path: "/company_dashboard", component: () => import("./views/CompanyDashboard.vue") },
  { path: "/company/profile", component: () => import("./views/CompanyProfile.vue") },
  { path: "/company/create-drive", component: () => import("./views/CreateDrive.vue") },
  { path: "/company/drives", component: () => import("./views/ManageDrives.vue") },
  { path: "/company/applications/:id", component: () => import("./views/Applications.vue") },
  { path: "/student-dashboard", component: () => import("./views/StudentDashboard.vue") },
  { path: "/student/profile", component: () => import("./views/StudentProfile.vue") },
  { path: "/student/applications", component: () => import("./views/MyApplications.vue") },
  { path: "/student/company/:id", component: () => import("./views/CompanyDetail.vue") },
  { path: "/admin", component: () => import("./views/AdminDashboard.vue") },
  { path: "/admin/companies", component: () => import("./views/AdminCompanies.vue") },
  { path: "/admin/drives", component: () => import("./views/AdminDrives.vue") },
  { path: "/admin/applications", component: () => import("./views/AdminApplications.vue") },
];
const router = createRouter({
  history: createWebHistory(),
  routes
});
export default router;