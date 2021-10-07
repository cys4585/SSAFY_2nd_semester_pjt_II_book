import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import store from "./store"
import "./assets/tailwind.css"
import SplitCarousel from "vue-split-carousel"
import VCalendar from "v-calendar"

createApp(App)
  .use(store)
  .use(router)
  .use(SplitCarousel)
  .use(VCalendar, {})
  .mount("#app")
window.Kakao.init("7cf386e0133b0a19ae8303dbf80d5039")
