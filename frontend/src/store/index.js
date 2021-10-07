import { createStore } from "vuex"
import { auth } from "@/store/modules/auth"
import { home } from "@/store/modules/home"
import { mypage } from "@/store/modules/mypage"
import { search } from "@/store/modules/search"
import { detail } from "@/store/modules/detail"

export default createStore({
  modules: { auth, home, mypage, search, detail },
})
