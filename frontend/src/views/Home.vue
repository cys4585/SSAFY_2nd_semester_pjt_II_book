<template>
  <div class="flex flex-col gap-4 pb-12">
    <div class="">
      <div class="pb-4">
        <p class="text-left p-4">추천도서</p>
        <div v-if="!access_token" class="h-60 flex bg-gray-200 opacity-80">
          <p class="m-auto">
            <router-link class="signup-span" :to="{ name: 'Signup' }"
              >회원가입</router-link
            >
            후 더 많은 서비스를 이용해보세요!
          </p>
        </div>
        <div v-else class="">
          <Carousel :bookList="conList" class="" />
        </div>
      </div>
    </div>
    <div class="pb-4">
      <p class="text-left p-4">인기 도서</p>
      <Carousel :bookList="randomList" />
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex"
import Carousel from "@/components/Carousel.vue"
import { onBeforeMount, computed } from "@vue/runtime-core"

export default {
  name: "Home",
  components: {
    Carousel,
  },

  setup() {
    const store = useStore()
    const access_token = localStorage.getItem("access_token")
    const recList = computed(() => {
      return store.state.home.recList
    })
    const conList = computed(() => {
      return store.state.home.conList
    })

    const randomList = computed(() => {
      return store.state.auth.books.book_list
    })

    onBeforeMount(() => {
      if (access_token) {
        // store.dispatch("home/getRec", access_token)
        store.dispatch("home/getCon", access_token)
      }
      store.dispatch("auth/getBooks", access_token)
    })

    return { access_token, recList, randomList, conList }
  },
}
</script>

<style lang="scss" scoped>
.signup-span {
  @apply underline hover:text-blue-700 cursor-pointer;
}

p {
  @apply text-xl;
}
</style>
