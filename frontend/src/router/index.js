import { createRouter, createWebHistory } from "vue-router"

import HomeLayout from "@/layouts/HomeLayout.vue"
import AccountsLayout from "@/layouts/AccountsLayout.vue"
import Home from "../views/Home.vue"
import Search from "../views/Search.vue"
import MyPage from "../views/MyPage.vue"
import Register from "../views/Register.vue"
import Signup from "../views/Signup.vue"
import Signin from "../views/Signin.vue"
import PasswordReset from "../views/PasswordReset.vue"
// import Member from "../views/Member.vue"
import Detail from "../views/Detail.vue"
import NotFound from "../views/NotFound.vue"

const requireAuth = () => (from, to, next) => {
  const isAuthenticated = localStorage.getItem("access_token")
  if (isAuthenticated) return next()
  next("/accounts/signin")
}

const requireAuth2 = () => (from, to, next) => {
  const isAuthenticated = localStorage.getItem("access_token")
  if (isAuthenticated) {
    next({ name: "Home" })
  } else {
    next()
  }
}

// children
// https://router.vuejs.org/kr/guide/essentials/nested-routes.html
const routes = [
  {
    path: "/",
    component: HomeLayout,
    children: [
      {
        path: "",
        name: "Home",
        component: Home,
      },
      {
        path: "search",
        name: "Search",
        component: Search,
        beforeEnter: requireAuth(),
      },
      {
        path: "mypage",
        name: "MyPage",
        component: MyPage,
        beforeEnter: requireAuth(),
      },
      {
        path: "detail",
        name: "Detail",
        component: Detail,
        beforeEnter: requireAuth(),
        // props: true,
      },
      // {
      //   path: "/member",
      //   name: "Member",
      //   component: Member,
      // },,
    ],
  },
  {
    path: "/accounts",
    component: AccountsLayout,
    beforeEnter: requireAuth2(),
    children: [
      {
        path: "signup",
        name: "Signup",
        component: Signup,
      },
      {
        path: "signin",
        name: "Signin",
        component: Signin,
      },
      {
        path: "register",
        name: "Register",
        component: Register,
      },
      // {
      //   path: "passwordReset",
      //   name: "PasswordReset",
      //   component: PasswordReset,
      // },
    ],
  },
  // {
  //   path: "/:pathMatch(.*)*",
  //   // redirect: "/404",
  //   component: NotFound,
  // },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
