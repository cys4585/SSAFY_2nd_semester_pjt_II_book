<template>
  <!-- <div class="bg-white w-2/5 z-10 fixed h-80"></div> -->
  <div class="header">
    <div>
      {{ userInfo.username }}님의 마음에 드는 책을 다섯 권 이상 선택한 후 다음을
      눌러주세요.
    </div>
    <div>고객님의 취향에 맞는 책을 추천해드리겠습니다.</div>
    <br />
    <button
      @click="likeSubmit(like)"
      class="submit-button"
      :class="{ active: likeListSize >= 5 }"
    >
      다음
    </button>
  </div>
  <div class="content">
    <div v-for="book in books" class="book-wrapper">
      <img :src="book.book_img" alt="" class="book-img" />
      <div class="book-overview">
        <h1 class="font-bold text-2xl">{{ book.title }}</h1>
        <p class="text-center overflow-hidden px-2">
          {{ book.author }}
        </p>
        <span
          :id="'heart-' + book.id"
          class="material-icons-outlined"
          @click="addLike(book.id)"
        >
          favorite
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex"
import { useRouter } from "vue-router"
import { computed, ref, onBeforeMount } from "vue"

export default {
  name: "Register",
  components: {},
  setup() {
    const router = useRouter()
    const store = useStore()
    const userInfo = JSON.parse(localStorage.getItem("userInfo"))
    const access_token = localStorage.getItem("access_token")

    const user_id = localStorage.getItem("user_id")

    const books = computed(() => {
      return store.state.auth.books.book_list
    })

    const like = ref(new Set())

    const addLike = (id) => {
      if (like.value.size >= 1) {
        if (like.value.has(id)) {
          like.value.delete(id)
          const active = document.getElementById(`heart-${id}`)
          active.style = "color:white"
        } else {
          like.value.add(id)
          const active = document.getElementById(`heart-${id}`)
          active.style = "color:red"
        }
      } else {
        like.value.add(id)
        const active = document.getElementById(`heart-${id}`)
        active.style = "color:red"
      }
    }

    const likeListSize = computed(() => {
      return like.value.size
    })

    const likeSubmit = (like) => {
      const likeList = [...like]
      store.dispatch("auth/makeLike", { likeList, access_token, user_id })
    }

    onBeforeMount(() => {
      store.dispatch("auth/getBooks", access_token)
    })

    return { books, addLike, like, likeSubmit, likeListSize, books, userInfo }
  },
}
</script>

<style lang="scss" scoped>
.header {
  @apply pt-20 pb-10 bg-white w-1/3 fixed left-0 right-0 z-20 rounded-2xl border-2 border-black;
  margin: 0 auto;

  .submit-button {
    @apply w-24 h-12 bg-gray-400 border-black rounded-xl text-white pointer-events-none;
  }
  .active {
    @apply bg-blue-600 pointer-events-auto;
  }
}

.content {
  @apply grid-cols-3 grid mx-auto pt-48 pb-20;

  .book-wrapper {
    @apply mx-auto mt-20 relative shadow-md w-60 h-96 flex flex-col items-center;
    .book-img {
      @apply absolute max-h-screen bg-white shadow-2xl w-60 h-96 flex items-center hover:opacity-20;
    }
    .book-overview {
      @apply mt-16 flex items-center flex-col justify-center w-60 h-56;
    }
  }
}

.material-icons-outlined {
  @apply text-white absolute text-6xl cursor-pointer;
  margin-top: 420px;
}
</style>
