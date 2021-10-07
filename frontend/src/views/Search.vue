<template>
  <div class="wrapper pt-8">
    <div class="select-bar flex justify-center gap-2">
      <!-- <select v-model="categoryItem.first_selected">
        <option v-for="option in category_set.first">
          {{ option.text }}
        </option>
      </select> -->
      <div>
        <select
          class="select-element"
          v-model="categoryItem.second_selected"
          @change="func_third()"
        >
          <option value="" selected>분류</option>
          <option v-for="option in category_second">
            {{ option }}
          </option>
        </select>
      </div>
      <div>
        <select
          class="select-element"
          v-model="categoryItem.third_selected"
          @change="func_fourth()"
        >
          <option value="" selected>분류</option>
          <option v-for="option in category_third">
            {{ option }}
          </option>
        </select>
      </div>
      <div>
        <select class="select-element" v-model="categoryItem.fourth_selected">
          <option value="" selected>분류</option>
          <option v-for="option in category_fourth">
            {{ option }}
          </option>
        </select>
      </div>
      <span
        class="material-icons-outlined my-auto pl-2 text-3xl cursor-pointer"
        @click="searchBook"
      >
        search
      </span>
    </div>

    <div class="spinner-box">
      <div v-if="isLoading == true">
        <spinner />
      </div>
    </div>

    <div
      class="search-list px-2"
      v-if="isLoading == false && bookList != null && bookList.length"
    >
      <div class="book-wrapper" v-for="(book, index) in bookList" :key="index">
        <div class="book-img cursor-pointer">
          <img :src="book.book_img" @click="showDetail(book.id)" />
        </div>
        <div class="book-overview">
          <!-- <h1 class="font-bold text-2xl">{{ book.title }}</h1> -->
          <p class="text-center text-xl text-white px-2">
            {{ book.author }}
          </p>
        </div>
      </div>
    </div>
    <div v-else>
      <div v-if="isLoading == false" class="h-60 flex">
        <p class="m-auto">검색 결과가 없어요 😢</p>
      </div>
    </div>

    <div
      class="search-list-footer flex justify-center gap-4"
      v-if="isLoading == false && bookList != null"
    >
      <button
        class="none-btn pointer-events-none cursor-default"
        v-if="categoryItem.page_number == 1"
      ></button>
      <button class="page-btn" @click="prevPage" v-else>이전</button>
      <p class="text-2xl">{{ categoryItem.page_number }} / {{ lastPage }}</p>
      <button
        class="none-btn pointer-events-none cursor-default"
        v-if="categoryItem.page_number == lastPage"
      ></button>
      <button class="page-btn" v-else @click="nextPage">다음</button>
    </div>
  </div>
</template>

<script>
import { reactive, ref } from "@vue/reactivity"
import { useStore } from "vuex"
import { computed } from "vue"
import { category } from "../assets/select-box"
import Spinner from "./Spinner.vue"
import router from "@/router"

export default {
  components: { Spinner },
  name: "Search",
  componets: {},
  setup() {
    const store = useStore()

    const userPK = localStorage.getItem("pk")
    const access_token = localStorage.getItem("access_token")

    const categoryItem = reactive({
      first_selected: "",
      second_selected: "",
      third_selected: "",
      fourth_selected: "",
      page_number: computed(() => {
        return store.state.search.page_number
      }),
      access_token: access_token,
    })

    const page_number = ref(1)
    const bookList = computed(() => {
      return store.state.search.bookList
    })

    const lastPage = computed(() => {
      return store.state.search.lastPage
    })

    const isLoading = computed(() => {
      return store.state.search.isLoading
    })

    const categoryList = category

    var category_second = []
    const category_third = computed(() => {
      return store.state.search.category_third
    })

    const category_fourth = computed(() => {
      return store.state.search.category_fourth
    })

    for (let item in categoryList) {
      category_second.push(item)
    }

    // third category 바꾸어주는 함수
    const func_third = () => {
      store.dispatch("search/getThirdCategory", categoryItem.second_selected)
    }

    //fourth categort바꾸어주는 함수
    const func_fourth = () => {
      const item = {
        second_selected: categoryItem.second_selected,
        third_selected: categoryItem.third_selected,
      }
      store.dispatch("search/getFourthCategory", item)
    }

    const prevPage = () => {
      store.commit("search/SET_PAGENUMBER", -1)
      searchBookPage()
    }

    const nextPage = () => {
      store.commit("search/SET_PAGENUMBER", 1)
      searchBookPage()
    }

    const searchBookPage = () => {
      store.dispatch("search/getBookList", categoryItem)
    }

    const searchBook = () => {
      store.dispatch("search/setSelected", "category")
      store.commit("search/RESET_PAGENUMBER")
      store.dispatch("search/setCategory", categoryItem)
      store.dispatch("search/getBookList", categoryItem)
    }

    const showDetail = (id) => {
      const bookItem = {
        book_id: id,
        access_token: access_token,
        userPk: userPK,
      }
      store.dispatch("detail/getBookDetail", bookItem)
      setTimeout(() => {
        router.push({ name: "Detail" })
      }, 400)
    }

    return {
      categoryItem,
      searchBook,
      bookList,
      isLoading,
      showDetail,
      page_number,
      prevPage,
      nextPage,
      lastPage,
      category_second,
      category_third,
      category_fourth,
      func_third,
      func_fourth,
    }
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  @apply pb-28;
  .search-list {
    @apply grid grid-cols-3 mt-8 gap-2;

    .book-wrapper {
      @apply flex flex-col items-center justify-center h-full;

      .book-img {
        @apply shadow-2xl w-full h-80 hover:opacity-50;
      }

      .book-overview {
        @apply bg-black w-full;
      }
    }
  }
  .search-list-footer {
    @apply mt-4;
    .page-btn {
      @apply w-20 bg-gray-600 text-white rounded-3xl h-8;
    }
    .none-btn {
      @apply w-20 bg-none h-8;
    }
  }
}

img {
  @apply w-full h-80;
  object-fit: fill;
}

select {
  @apply w-40 h-12 rounded-xl shadow-md px-2;

  -webkit-appearance: none; /* for chrome */
}
</style>
