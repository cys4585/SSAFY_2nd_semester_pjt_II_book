<template>
  <div class="review-wrapper">
    <h1>리뷰 작성</h1>
    <div class="star-rating space-x-4 mx-auto">
      <input
        type="radio"
        id="5-stars"
        name="rating"
        value="5"
        v-model="ratings"
      />
      <label for="5-stars" class="star pr-4">★</label>
      <input
        type="radio"
        id="4-stars"
        name="rating"
        value="4"
        v-model="ratings"
      />
      <label for="4-stars" class="star">★</label>
      <input
        type="radio"
        id="3-stars"
        name="rating"
        value="3"
        v-model="ratings"
      />
      <label for="3-stars" class="star">★</label>
      <input
        type="radio"
        id="2-stars"
        name="rating"
        value="2"
        v-model="ratings"
      />
      <label for="2-stars" class="star">★</label>
      <input
        type="radio"
        id="1-star"
        name="rating"
        value="1"
        v-model="ratings"
      />
      <label for="1-star" class="star">★</label>
    </div>

    <textarea name="" id="" cols="30" rows="10" v-model="content"> </textarea>
    <div>
      <button class="btn-write" @click="writeReview">작성</button>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity"
import { useStore } from "vuex"
import { computed } from "vue"

export default {
  name: "ReviewWrite",
  components: {},
  setup() {
    const store = useStore()
    const access_token = localStorage.getItem("access_token")

    const book_id = computed(() => {
      return store.state.detail.bookDetail.id
    })
    const content = ref("")
    const ratings = ref("")

    const writeReview = () => {
      if (ratings.value == "") {
        alert("점수를 입력해 주세요")
      }

      if (content.value == "") {
        alert("내용을 입력해 주세요")
      } else {
        const reviewItem = {
          book_id: book_id.value,
          content: content.value,
          score: parseInt(ratings.value),
          access_token: access_token,
        }

        store.dispatch("detail/writeReview", reviewItem)
      }
    }
    return {
      content,
      ratings,
      writeReview,
    }
  },
}
</script>

<style lang="scss" scoped>
.review-wrapper {
  @apply bg-gray-300 rounded-lg shadow-lg;

  .star-rating {
    @apply flex flex-row-reverse text-4xl leading-10 justify-around text-center w-12;
  }

  .star-rating input {
    display: none;
  }

  .star-rating label {
    -webkit-text-fill-color: transparent; /* Will override color (regardless of order) */
    -webkit-text-stroke-width: 2.3px;
    -webkit-text-stroke-color: #2b2a29;
    cursor: pointer;
  }

  .star-rating :checked ~ label {
    -webkit-text-fill-color: gold;
  }

  .star-rating label:hover,
  .star-rating label:hover ~ label {
    -webkit-text-fill-color: #fff58c;
  }

  .btn-write {
    @apply w-20 bg-gray-600 text-white rounded-3xl h-8;
  }
}
</style>
