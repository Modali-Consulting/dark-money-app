import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import ResourcesView from "../views/ResourcesView.vue";
import ResourceDetailView from "../views/ResourceDetailView.vue";
import CasesView from "../views/CasesView.vue";
import CaseDetailView from "../views/CaseDetailView.vue";
import EntitiesView from "../views/EntitiesView.vue";
import EntityDetailView from "../views/EntityDetailView.vue";
import PowerMapView from "../views/PowerMapView.vue";
import PipelinesView from "../views/PipelinesView.vue";
import ObservabilityView from "../views/ObservabilityView.vue";
import SettingsView from "../views/SettingsView.vue";
import LoginView from "../views/LoginView.vue";

const routes = [
  { path: "/", component: DashboardView },
  { path: "/resources", component: ResourcesView },
  { path: "/resources/:id", component: ResourceDetailView },
  { path: "/cases", component: CasesView },
  { path: "/cases/:id", component: CaseDetailView },
  { path: "/entities", component: EntitiesView },
  { path: "/entities/:id", component: EntityDetailView },
  { path: "/powermap", component: PowerMapView },
  { path: "/pipelines", component: PipelinesView },
  { path: "/observability", component: ObservabilityView },
  { path: "/settings", component: SettingsView },
  { path: "/auth/login", component: LoginView }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
