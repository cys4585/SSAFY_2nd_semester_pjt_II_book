import axios from "axios"
import router from "@/router"
import { BASEURL } from "@/lib/url"

export const mypage = {
  namespaced: true,
  state: () => ({
    userInfo: null,
    likeList: [],
    readList: [],
    reviewList: [],
    readDate: null,
    colors: [
      "bg-blue-500 text-white",
      "bg-indigo-400 text-white",
      "bg-purple-400 text-white",
      "bg-pink-800 text-white",
      "bg-indigo-900 text-white",
      "bg-green-700 text-white",
      "bg-gray-600 text-white",
    ],
  }),
  mutations: {
    SET_USERINFO(state, value) {
      state.userInfo = value
      localStorage.setItem("userInfo", JSON.stringify(value.data))
    },
    SET_LIKEBOOK(state, value) {
      state.likeList = value
    },
    SET_READBOOK(state, value) {
      state.readList.push(value)
    },
    SET_READBOOK_NULL(state) {
      state.readList = []
    },
    SET_REVIEW(state, value) {
      state.reviewList = value
    },
    SET_READDATE(state, value) {
      state.readDate = value
    },
  },
  getters: {},
  actions: {
    // 비밀번호 변경
    changePassword({ commit }, info) {
      axios({
        method: "post",
        url: `${BASEURL}/api/accounts/password/change/`,
        data: {
          new_password1: info.password.new_password1,
          new_password2: info.password.new_password2,
        },
        headers: { Authorization: `Bearer ${info.access_token}` },
      })
        .then((response) => {
          console.log(response.status)
          alert("비밀번호 변경이 완료됐습니다.")
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 유저 정보 변경
    editInfo({ commit }, userData) {
      axios({
        method: "patch",
        url: `${BASEURL}/api/accounts/about-user/`,
        data: {
          email: userData.newUserInfo.email,
          last_name: userData.newUserInfo.last_name,
          first_name: userData.newUserInfo.first_name,
        },
        headers: { Authorization: `Bearer ${userData.access_token}` },
      })
        .then((response) => {
          commit("SET_USERINFO", response)
          alert("회원 정보 수정이 완료됐습니다.")
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 회원 탈퇴
    deleteUser({ commit }, data) {
      axios({
        method: "delete",
        url: `${BASEURL}/api/accounts/signout/`,
        data: {
          password: data.signOutPassword.value,
        },
        headers: { Authorization: `Bearer ${data.access_token}` },
      })
        .then((response) => {
          console.log(response.status)
          localStorage.clear()
          router.go({ name: "Home" })
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 내가 찜한 책 리스트 가져오기
    getLike({ commit }, token) {
      axios({
        method: "get",
        url: `${BASEURL}/api/book/like/list/`,
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((response) => {
          commit("SET_LIKEBOOK", response.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // 내가 읽은 책 리스트 가져오기
    getRead({ commit, state }, token) {
      let colors = state.colors
      axios({
        method: "get",
        url: `${BASEURL}/api/book/read/list/`,
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((response) => {
          commit("SET_READBOOK_NULL")
          for (let items in response.data.book) {
            const data = {
              key: items,
              customData: {
                book_id: response.data.book[items].id,
                title: response.data.book[items].title,
                class: colors[items % 7],
              },
              dates: new Date(response.data.read_date[items].read_at),
            }

            commit("SET_READBOOK", data)
            commit("SET_READDATE", response.data.read_date[items].read_at)
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getReview({ commit }, token) {
      axios({
        method: "get",
        url: `${BASEURL}/api/accounts/review/list/`,
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((response) => {
          commit("SET_REVIEW", response.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },
}
