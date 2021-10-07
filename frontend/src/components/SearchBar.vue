<template>
  <div class="search-bar bg-yellow-50">
    <div class="top-content">
      <router-link :to="{ name: 'Home' }">
        <div class="flex">
          <span class="material-icons-outlined my-auto text-3xl">
            menu_book
          </span>
          <p class="my-auto text-2xl">북적북적</p>
        </div></router-link
      >
      <div class="btn-group">
        <!-- v-if else는 같은 div안에 있어야 친구가 될 수 있다.. -->
        <button class="sign signout-btn" @click="signout" v-if="activeSignin">
          로그아웃
        </button>
        <button v-else class="sign signin-btn" @click="signin">로그인</button>
      </div>
    </div>
    <div
      class="bottom-content pb-4"
      v-if="
        $route.fullPath.includes('search') || $route.fullPath.includes('detail')
      "
    >
      <input
        class="search-input"
        type="text"
        placeholder="도서명을 입력하세요"
        v-model="searchInput"
      />
      <span
        class="material-icons-outlined my-auto pl-2 text-3xl cursor-pointer"
        @click="searchBook"
      >
        search
      </span>
    </div>
  </div>
</template>

<script>
// import { ref } from "vue"
import { useRouter } from "vue-router"
import { useStore } from "vuex"
import { onUnmounted, ref } from "vue"

export default {
  name: "SearchBar",
  components: {},
  setup() {
    const store = useStore()
    const router = useRouter()
    const activeSignin = localStorage.getItem("access_token")
    const refresh = localStorage.getItem("refresh_token")

    const searchInput = ref("")

    const signin = () => {
      router.push({ name: "Signin" })
    }

    const signout = () => {
      router.push({ name: "Home" })
      store.dispatch("auth/signout", refresh)
    }

    const searchBook = () => {
      const bookItem = {
        word: searchInput.value,
        access_token: localStorage.getItem("access_token"),
      }

      store.dispatch("search/setSelected", "search")
      store.commit("search/RESET_PAGENUMBER")
      store.commit("search/SET_CATEGORYITEM", searchInput.value)
      store.dispatch("search/getBookList", bookItem)

      router.push({ name: "Search" })
    }

    return { signin, signout, activeSignin, searchInput, searchBook }
  },
}
</script>

<style lang="scss" scoped>
.search-bar {
  .top-content {
    @apply flex justify-between p-4;

    .btn-group {
      .sign {
        @apply w-20 bg-gray-600 text-white rounded-3xl h-8 shadow-md;
      }
    }
  }

  .bottom-content {
    @apply flex justify-center;

    .search-input {
      @apply w-80 rounded-lg h-12 p-4 shadow;
    }
  }
}
</style>
