import axios from "axios"
import router from "@/router"
import { BASEURL } from "@/lib/url"

export const auth = {
  namespaced: true,
  state: () => ({
    userInfo: null,
    books: [],
    userStatus: null,
    mailStatus: null,
  }),
  mutations: {
    SET_USERINFO(state, value) {
      state.userInfo = value.user
      localStorage.setItem("pk", value.user.pk)
      localStorage.setItem("userInfo", JSON.stringify(value.user))
      localStorage.setItem("access_token", value.access_token)
      localStorage.setItem("refresh_token", value.refresh_token)
    },
    SET_NAMESTATUS(state, value) {
      state.userStatus = value
    },
    SET_MAILSTATUS(state, value) {
      state.mailStatus = value
    },
    // 관심분야 책 리스트 불러오기
    SET_BOOKS(state, value) {
      state.books = value
    },
  },
  getters: {},
  actions: {
    // 회원가입
    signUp({ commit }, userInfo) {
      axios({
        method: "post",
        url: `${BASEURL}/api/accounts/signup/`,
        data: {
          username: userInfo.username,
          password1: userInfo.password,
          password2: userInfo.password2,
          email: userInfo.email,
          last_name: userInfo.last_name,
          first_name: userInfo.first_name,
        },
      })
        .then((response) => {
          console.log(response.status)
          commit("SET_USERINFO", response.data)
          alert("회원가입이 완료됐습니다")
          router.replace({ name: "Register" })
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 아이디 중복체크
    nameDuplicateCheck({ commit }, payload) {
      console.log(payload)
      axios({
        method: "get",
        url: `${BASEURL}/api/accounts/duplicate_check`,
        params: {
          username: payload,
        },
      })
        .then((response) => {
          commit("SET_NAMESTATUS", response.status)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 메일 중복체크
    mailDuplicateCheck({ commit }, payload) {
      axios({
        method: "get",
        url: `${BASEURL}/api/accounts/duplicate_check`,
        params: {
          email: payload,
        },
      })
        .then((response) => {
          commit("SET_MAILSTATUS", response.status)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 로그인
    signin({ commit }, signinForm) {
      axios({
        method: "post",
        url: `${BASEURL}/api/accounts/login/`,
        data: {
          username: signinForm.id,
          password: signinForm.password,
        },
      })
        .then((response) => {
          commit("SET_USERINFO", response.data)
          router.replace({ name: "Home" })
        })
        .catch((error) => {
          console.error(error)
          alert("아이디와 비밀번호를 확인해주세요")
        })
    },
    // 로그아웃
    signout({ commit }, refresh) {
      axios({
        method: "post",
        url: `${BASEURL}/api/accounts/logout/`,
        data: {
          refresh: refresh,
        },
      })
        .then((response) => {
          localStorage.clear()
          router.go()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 비밀번호 찾기
    // -------------------------------- ING -------------------------------- //
    passwordReset({ commit }, payload) {
      console.log(payload.value)
      axios({
        method: "post",
        url: `${BASEURL}/api/accounts/password_reset/`,
        data: {
          email: payload.value,
        },
      })
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // -------------------------------- ING -------------------------------- //
    // 책 가져오기
    getBooks({ commit }, access_token) {
      axios({
        method: "get",
        url: `${BASEURL}/api/book/list`,
        params: {
          // review_cnt 순으로
          base: "review_cnt",
          // 리뷰가 50개 넘는 것만,
          min_review_cnt: 50,
          // 한 페이지에 60개씩
          cnt_per_page: 60,
          // PAGE는 랜덤하게(유저마다 다르게 보이도록)
          page_num: Math.floor(Math.random() * 7) + 1,
        },
        // headers: { Authorization: `Bearer ${access_token}` },
      })
        .then((response) => {
          commit("SET_BOOKS", response.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 책 찜하기(가입 시)
    makeLike({ commit }, payload) {
      axios({
        method: "post",
        url: `${BASEURL}/api/book/like/`,
        data: {
          book_ids: payload.likeList,
          user_id: payload.user_id,
        },
        headers: { Authorization: `Bearer ${payload.access_token}` },
      })
        .then((response) => {
          router.push({ name: "Home" })
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },
}
