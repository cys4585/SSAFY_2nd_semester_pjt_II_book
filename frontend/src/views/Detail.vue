<template>
  <div>
    <div class="modal-header flex justify-between">
      <p>{{ book.title }}, {{ book.author }}</p>
      <span class="material-icons-outlined cursor-pointer" @click="back">
        close
      </span>
    </div>
    <hr />
    <div class="modal-body">
      <!---------------------------------------- left ---------------------------------------->
      <div class="left">
        <div class="left-top">
          <img :src="book.book_img" alt="이미지를 불러올 수 없어요." />
        </div>
        <div class="left-bottom">
          <div>
            <p>출판사 {{ book.publisher }}</p>
            <p>출판일 {{ book.publish_date }}</p>
            <p>가격 {{ book.price }}</p>
            <p v-if="book.kb_score == null">😢점수가 없어요</p>
            <p v-else>{{ book.kb_score }}</p>
          </div>
          <div>
            <div class="detail-read icon">
              <!--읽음 -->
              <span
                class="material-icons"
                v-if="isRead"
                @click="unReadBook(book.id)"
              >
                visibility_off
              </span>
              <span class="material-icons" v-else @click="readBook(book.id)">
                visibility
              </span>
              <p>{{ book.read_users.length + fake.read }}명이 읽었어요</p>
            </div>

            <div class="detail-like icon">
              <!--찜 했을 때-->
              <span
                class="material-icons"
                v-if="isLike"
                @click="unLikeBook(book.id)"
              >
                favorite
              </span>
              <!-- 찜 안했을 때 -->
              <span class="material-icons" v-else @click="likeBook(book.id)">
                favorite_border
              </span>
              <p>{{ book.like_users.length + fake.like }}명이 찜했어요</p>
            </div>
          </div>
        </div>
      </div>
      <!---------------------------------------- right ---------------------------------------->
      <div class="right">
        <div class="right-top">
          <p>{{ book.content }}</p>
        </div>
        <hr />
        <div class="right-bottom">
          <div class="review-wrapper">
            <div class="review-content">
              <textarea
                class="float-left rounded-2xl p-2"
                name=""
                id=""
                cols="50"
                rows="3"
                style="resize: none"
                v-model="content"
              >
              </textarea>
            </div>

            <div class="review-write ml-2">
              <p>{{ userInfo.username }}</p>
              <div class="star mb-2">
                <star-rating
                  v-model:rating="rating"
                  :star-size="15"
                  :show-rating="false"
                  :inline="true"
                ></star-rating>
              </div>
              <button class="btn-write" @click="writeReview(book.id)">
                작성
              </button>
            </div>
          </div>
          <div class="mt-4 h-20">
            <div
              v-for="(bookReview, idx) in bookReviewList"
              class="flex bg-gray-50 my-2 rounded-md"
            >
              <div class="text-left flex-1 p-2">
                <p>{{ bookReview.content }}</p>
              </div>
              <div class="w-32 flex-col border-l-2">
                <p>
                  {{ bookReview.user_name }}
                  <span
                    v-if="bookReview.user_name === userInfo.username"
                    class="
                      material-icons
                      cursor-pointer
                      align-middle
                      text-red-700 text-sm
                    "
                    @click="deleteReview(bookReview.id)"
                  >
                    clear
                  </span>
                  <!-- v-if="userinfo.username == bookReview.user_name" -->
                </p>
                <p>
                  <star-rating
                    :rating="bookReview.score"
                    :star-size="15"
                    :show-rating="false"
                    :inline="true"
                    :read-only="true"
                  >
                  </star-rating>
                </p>
                <!-- <p>{{ bookReview.score }}점</p> -->
                <!-- <p>리뷰 작성 시간</p> -->
                <p>
                  {{ bookReview.created_at.slice(2, 4) }}.{{
                    bookReview.created_at.slice(5, 7)
                  }}.{{ bookReview.created_at.slice(8, 10) }}
                  {{ bookReview.created_at.slice(11, 16) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex"
import { computed } from "vue"
import { reactive, ref } from "@vue/reactivity"
import { useRouter } from "vue-router"
import ReviewWrite from "../components/ReviewWrite.vue"
import StarRating from "vue-star-rating"

export default {
  name: "Detail",
  components: {
    ReviewWrite,
    StarRating,
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const access_token = localStorage.getItem("access_token")
    const userInfo = JSON.parse(localStorage.getItem("userInfo"))

    const back = () => {
      router.go(-1)
    }

    const book = computed(() => {
      return store.state.detail.bookDetail
    })

    const bookReviewList = computed(() => {
      return store.state.detail.bookReview
    })

    const fake = reactive({
      read: 0,
      like: 0,
    })

    const isRead = computed(() => {
      return store.state.detail.isRead
    })

    const isLike = computed(() => {
      return store.state.detail.isLike
    })

    const readBook = (book_id) => {
      const date = new Date()
      var year = date.getFullYear()
      var month = date.getMonth() + 1
      var day = date.getDate()

      if (month < 10) month = "0" + month
      if (day < 10) day = "0" + day

      const fullDay = year + "-" + month + "-" + day

      store.dispatch("detail/readBook", { book_id, fullDay, access_token })
      fake.read += 1
    }

    const unReadBook = (book_id) => {
      store.dispatch("detail/unReadBook", { book_id, access_token })
      fake.read -= 1
    }

    const likeBook = (book_id) => {
      // var access_token = localStorage.getItem("access_token")
      store.dispatch("detail/likeBook", { book_id, access_token })
      fake.like += 1
    }

    const unLikeBook = (book_id) => {
      // var access_token = localStorage.getItem("access_token")
      store.dispatch("detail/unLikeBook", { book_id, access_token })
      fake.like -= 1
    }

    const content = ref("")
    const rating = ref(0)

    const writeReview = (id) => {
      if (rating.value == 0 && content.value == "") {
        alert("내용과 점수를 입력해 주세요.")
      } else if (content.value == "") {
        alert("내용을 입력해 주세요")
      } else if (rating.value == 0) {
        alert("점수를 입력해주세요.")
      } else {
        const reviewItem = {
          book_id: id,
          content: content.value,
          score: rating.value,
          access_token: access_token,
        }
        store.dispatch("detail/writeReview", reviewItem)
        content.value = null
        rating.value = null
      }
    }

    const deleteReview = (id) => {
      const reviewItem = {
        review_id: id,
        access_token: access_token,
      }

      store.dispatch("detail/deleteReview", reviewItem)
    }

    return {
      book,
      userInfo,
      readBook,
      unReadBook,
      likeBook,
      unLikeBook,
      rating,
      content,
      bookReviewList,
      writeReview,
      deleteReview,
      back,
      isRead,
      isLike,
      fake,
    }
  },
}
</script>

<style lang="scss" scoped>
.modal-header {
  @apply text-left h-12 text-2xl py-2 px-4 bg-black text-white;
}

.modal-body {
  @apply mt-2 flex;

  .left {
    .left-top {
      @apply flex-initial ml-4;

      img {
        @apply h-96 rounded-2xl;
      }
    }

    .left-bottom {
      @apply text-left mt-4 ml-4;

      .icon {
        @apply flex;
      }
      span {
        @apply cursor-pointer mr-1;
      }
    }
  }

  .right {
    @apply flex-1 flex flex-col;

    .right-top {
      @apply h-72 overflow-hidden px-4 text-left;
    }

    .right-top:hover {
      @apply overflow-scroll;
    }

    hr {
      @apply h-1 bg-white text-white border-0 mx-1;
    }
    .right-bottom {
      @apply p-2 flex-1;
      overflow: scroll;
      -ms-overflow-style: none;

      .review-wrapper {
        @apply flex;
        .review-content {
          textarea {
            @apply float-left rounded-2xl p-2;
          }
        }
        .btn-write {
          @apply w-20 bg-gray-600 text-white rounded-3xl h-8;
        }
      }
    }
    .right-bottom::-webkit-scrollbar {
      display: none; /* Chrome, Safari, Opera*/
      width: 0;
    }
  }
}
</style>
