<template>
  <!-- 이 미친놈은 직접 style을 줘야 작동함 -->
  <split-carousel
    :height="300"
    :item-width="200"
    :display-amount="3"
    class=""
    v-if="bookList && bookList.length > 0"
  >
    <split-carousel-item class="w-60" v-for="book in bookList"
      ><img
        class="cursor-pointer hover:opacity-50"
        :src="book.book_img"
        alt=""
        @click="goDetail(book.id)"
    /></split-carousel-item>
  </split-carousel>
  <div v-else class="h-60 w-full flex">
    <p class="m-auto">도서 목록을 불러오는 중 입니다.</p>
  </div>
</template>

<script>
import { SplitCarousel, SplitCarouselItem } from "vue-split-carousel"
import { useStore } from "vuex"
import router from "@/router"

export default {
  name: "Carousel",
  components: {
    SplitCarousel,
    SplitCarouselItem,
  },
  props: {
    bookList: {
      type: Array,
    },
  },
  setup() {
    const store = useStore()

    const goDetail = (book_id) => {
      const bookItem = {
        book_id: book_id,
        access_token: localStorage.getItem("access_token"),
        userPk: localStorage.getItem("pk"),
      }

      store.dispatch("detail/getBookDetail", bookItem)
      setTimeout(() => {
        router.push({ name: "Detail" })
      }, 200)
    }
    return {
      goDetail,
    }
  },
}
</script>

<style lang="scss" scoped>
img {
  @apply w-full h-80;
  object-fit: fill;
}
</style>
