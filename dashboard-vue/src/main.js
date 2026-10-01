import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";

const app = createApp(App);
app.mount("#app");

/* Hilangkan splash LEBIH CEPAT */
const splash = document.getElementById("splash");
if (splash) {
  requestAnimationFrame(() => {
    splash.classList.add("hidden");
    setTimeout(() => splash.remove(), 300);
  });
}
