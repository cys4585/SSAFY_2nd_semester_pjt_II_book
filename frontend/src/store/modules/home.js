import axios from "axios"
import { BASEURL } from "@/lib/url"

export const home = {
  namespaced: true,
  state: () => ({
    recList: [],
    conList: [],
  }),
  mutations: {
    SET_REC(state, value) {
      state.recList = value
    },
    SET_CON(state, value) {
      state.conList = value
    },
  },
  getters: {},
  actions: {
    getRec({ commit }, token) {
      axios({
        method: "get",
        url: `${BASEURL}/api/book/recommend/tag/`,
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((response) => {
          console.log(response.status)
          commit("SET_REC", response.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getCon({ commit }, token) {
      axios({
        method: "get",
        url: `${BASEURL}/api/book/recommend/content/`,
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((response) => {
          console.log(response.status)
          commit("SET_CON", response.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },
}
