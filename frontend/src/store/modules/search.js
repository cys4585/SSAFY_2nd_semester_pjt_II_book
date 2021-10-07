import axios from "axios"
import { category } from "../../assets/select-box"
import { BASEURL } from "@/lib/url"

export const search = {
  namespaced: true,
  state: () => ({
    bookList: null,
    isLoading: false,
    lastPage: null,
    category_second: [],
    category_third: [],
    category_fourth: [],
    isSelected: "",
    categoryItem: {},
    page_number: 1,
  }),
  mutations: {
    //책 리스트 저장
    SET_BOOKLIST(state, value) {
      state.bookList = value
    },
    // 마지막 페이지 저장
    SET_LASTPAGE(state, value) {
      state.lastPage = value
    },
    // 로딩 스피너 저장
    SET_ISLOADING(state) {
      state.isLoading = !state.isLoading
    },
    SET_CATEGORY_THIRD(state, value) {
      state.category_third = value
    },
    SET_CATEGORY_FOURTH(state, value) {
      state.category_fourth = value
    },
    SET_ISSELECTED(state, value) {
      state.isSelected = value
    },
    SET_CATEGORYITEM(state, value) {
      state.categoryItem = value
    },
    SET_PAGENUMBER(state, value) {
      state.page_number += value
    },
    RESET_PAGENUMBER(state) {
      state.page_number = 1
    },
  },
  getters: {
    GET_BOOKLIST(state) {
      return state.bookList
    },
    GET_ISLOADING(state) {
      return state.isLoading
    },
  },
  actions: {
    setSelected({ commit }, base) {
      commit("SET_ISSELECTED", base)
    },
    setCategory({ commit }, categoryItem) {
      commit("SET_CATEGORYITEM", categoryItem)
    },

    async getBookList({ commit, state }, item) {
      commit("SET_ISLOADING")

      var isSelected = state.isSelected
      if (isSelected == "category") {
        try {
          const response = await axios({
            method: "get",
            url: `${BASEURL}/api/book/list`,
            headers: {
              Authorization: `Bearer ${item.access_token}`,
            },
            params: {
              base: "category",
              category_first: "국내도서",
              category_second: state.categoryItem.second_selected,
              category_third: state.categoryItem.third_selected,
              category_fourth: state.categoryItem.fourth_selected,
              page_num: state.page_number,
              cnt_per_page: 12,
            },
          })

          commit("SET_BOOKLIST", response.data.book_list)
          commit("SET_LASTPAGE", response.data.last_page)
          setTimeout(() => {
            commit("SET_ISLOADING")
          }, 1500)
          // console.log(response.data)
        } catch (error) {
          console.error(error)
        }
      } else if (isSelected == "search") {
        try {
          const response = await axios({
            method: "get",
            url: `${BASEURL}/api/book/list`,
            headers: {
              Authorization: `Bearer ${item.access_token}`,
            },
            params: {
              base: "search",
              word: state.categoryItem,
              page_num: state.page_number,
              cnt_per_page: 12,
            },
          })
          commit("SET_BOOKLIST", response.data.book_list)
          commit("SET_LASTPAGE", response.data.last_page)
          setTimeout(() => {
            commit("SET_ISLOADING")
          }, 1500)
        } catch (error) {
          console.error(error)
        }
      }
    },

    // async getBookListName({ commit }, bookItem) {
    //   commit("SET_ISLOADING")
    //   try {
    //     const response = await axios({
    //       method: "get",
    //       url: `http://localhost:8000/book/list`,
    //       headers: {
    //         Authorization: `Bearer ${bookItem.access_token}`,
    //       },
    //       params: {
    //         base: "search",
    //         word: bookItem.word,
    //         cnt_per_page: 12,
    //       },
    //     })
    //     commit("SET_BOOKLIST", response.data.book_list)
    //     commit("SET_LASTPAGE", response.data.last_page)
    //     commit("SET_ISLOADING")
    //   } catch (error) {
    //     console.error(error)
    //   }
    // },

    getThirdCategory({ commit }, second_selected) {
      commit("SET_CATEGORY_THIRD", [])
      commit("SET_CATEGORY_FOURTH", [])
      var third_category = []
      for (let item in category[second_selected][0]) {
        third_category.push(item)
      }
      commit("SET_CATEGORY_THIRD", third_category)
    },

    getFourthCategory({ commit }, item) {
      commit("SET_CATEGORY_FOURTH", [])
      var fourth_category =
        category[item.second_selected][1][item.third_selected]

      commit("SET_CATEGORY_FOURTH", fourth_category)
    },
  },
}
