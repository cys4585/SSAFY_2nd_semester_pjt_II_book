<template>
  <!-------------------------- Modal Section -------------------------->
  <section>
    <div class="edit-modal" v-if="modal">
      <div class="modal-header">
        <h1 class="text-2xl">나의 프로필</h1>
        <span class="close-btn material-icons-outlined" @click="toggleModal">
          close
        </span>
      </div>
      <hr />
      <div class="modal-body" v-if="modalPage === 'one'">
        <div class="content">
          <p class="content-name">아이디</p>
          <p>{{ userInfo.username }}</p>
        </div>
        <div class="content">
          <p class="content-name">이메일</p>
          <p v-if="activeEdit !== 'email'" class="content-info">
            {{ userInfo.email }}
          </p>
          <span
            @click="editMode('email')"
            class="material-icons-outlined"
            v-if="activeEdit !== 'email'"
          >
            edit
          </span>
          <input
            type="text"
            v-if="activeEdit === 'email'"
            class="content-input"
            v-model="newUserInfo.email"
            :placeholder="userInfo.email"
            @keyup.enter="editInfo"
            @keyup.esc="editMode('')"
          />
          <span
            class="material-icons-outlined text-green-600"
            v-if="activeEdit === 'email'"
            @click="editInfo"
          >
            done
          </span>
        </div>
        <div class="content">
          <p class="content-name">성</p>
          <p
            @click="editMode('last_name')"
            v-if="activeEdit !== 'last_name'"
            class="content-info"
          >
            {{ userInfo.last_name }}
          </p>
          <span
            @click="editMode('last_name')"
            class="material-icons-outlined align-middle"
            v-if="activeEdit !== 'last_name'"
          >
            edit
          </span>
          <input
            type="text"
            v-if="activeEdit === 'last_name'"
            class="content-input"
            v-model="newUserInfo.last_name"
            :placeholder="userInfo.last_name"
            @keyup.enter="editInfo"
            @keyup.esc="editMode('')"
          />
          <span
            class="material-icons-outlined text-green-600"
            v-if="activeEdit === 'last_name'"
            @click="editInfo"
          >
            done
          </span>
        </div>
        <div class="content">
          <p class="content-name">이름</p>
          <p
            @click="editMode('first_name')"
            v-if="activeEdit !== 'first_name'"
            class="content-info"
          >
            {{ userInfo.first_name }}
          </p>
          <span
            @click="editMode('first_name')"
            class="material-icons-outlined align-middle"
            v-if="activeEdit !== 'first_name'"
          >
            edit
          </span>
          <input
            type="text"
            v-if="activeEdit === 'first_name'"
            class="content-input"
            v-model="newUserInfo.first_name"
            :placeholder="userInfo.first_name"
            @keyup.enter="editInfo"
            @keyup.esc="editMode('')"
          />
          <span
            class="material-icons-outlined text-green-600"
            v-if="activeEdit === 'first_name'"
            @click="editInfo"
          >
            done
          </span>
        </div>
      </div>
      <div class="modal-body gap-2" v-if="modalPage === 'two'">
        <p>비밀번호 변경</p>
        <input
          class="input"
          type="password"
          placeholder="새 비밀번호"
          v-model="password.new_password1"
          @blur="passwordValid"
        />
        <p class="text-red-500 text-sm pl-1" v-if="pwStatus === false">
          8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.
        </p>
        <input
          class="input"
          type="password"
          placeholder="새 비밀번호 확인"
          v-model="password.new_password2"
          @blur="passwordSame"
        />
        <p class="text-red-500 text-sm pl-1" v-if="pwCheck === false">
          비밀번호가 일치하지 않습니다.
        </p>
        <button
          @click="changePassword"
          :class="{
            active: pwStatus && pwCheck,
            nope: (pwCheck == pwStatus) == false,
          }"
        >
          변경
        </button>
      </div>
      <div class="modal-body gap-2" v-if="modalPage === 'three'">
        <h1>회원탈퇴</h1>
        <p>비밀번호를 입력 후 탈퇴를 누르면 회원탈퇴가 진행됩니다.</p>
        <input
          type="password"
          name=""
          id=""
          class="border-2 px-2 w-1/2"
          v-model="signOutPassword"
        />
        <button
          @click="deleteUser"
          :class="{ active: signOutPassword.length > 6 }"
        >
          탈퇴
        </button>
      </div>
      <hr />
      <div class="modal-footer text-right">
        <div>
          <span class="material-icons" id="one" @click="togglePage('one')">
            looks_one
          </span>
          <span
            class="material-icons-outlined"
            id="two"
            @click="togglePage('two')"
          >
            looks_two
          </span>
          <span
            class="material-icons-outlined"
            id="three"
            @click="togglePage('three')"
          >
            looks_3
          </span>
        </div>
      </div>
    </div>
    <div class="backdrop" v-if="modal"></div>
  </section>
  <!-------------------------- Profile Section -------------------------->
  <section class="mt-8">
    <div class="mypage-bg">
      <!--사용자 정보 표시-->
      <div class="user-profile">
        <div class="nickname">
          <b>{{ userInfo.username }}</b
          >님의 마이페이지<span
            class="material-icons-outlined"
            @click="toggleModal"
          >
            edit
          </span>
        </div>
        <div class="user-profile-book">
          <div class="read-book-cnt">
            <b>읽은 책 수</b>
            <br />
            <p>{{ readList.length }}권</p>
          </div>
          <div class="liked-book-cnt">
            <b>찜한 책 수</b>
            <br />
            <p>{{ likeList.length }}권</p>
          </div>
          <div class="recent-read-date">
            <b>최근 읽은 날짜</b>
            <br />
            <p v-if="!readDate">-</p>
            <p v-else>{{ readDate }}</p>
          </div>
        </div>
      </div>

      <!-- 달력 커스텀마이징-->
      <div class="px-8 mt-20">
        <p class="bg-gray-200 inline">
          책 제목을 눌러 상세정보를 확인할 수 있습니다.
        </p>
        <v-calendar
          class="custom-calendar max-w-full"
          :masks="masks"
          :attributes="attributes"
          disable-page-swipe
          is-expanded
        >
          <!--슬롯을 사용하면 컴포넌트의 특정 마크업 영역을 재정의하여 같은 컴포넌트를 각기 다르게 표현할 수 있습니다.-->
          <template v-slot:day-content="{ day, attributes }">
            <div class="calendar-group">
              <p class="day-label">{{ day.day }}</p>
              <div class="calendar-content h-12">
                <p
                  v-for="attr in attributes"
                  :key="attr.key"
                  class="calendar-text hover:bg-opacity-50"
                  :class="attr.customData.class"
                  @click="showDetail(attr.customData.book_id)"
                >
                  {{ attr.customData.title }}
                </p>
              </div>
            </div>
          </template>
        </v-calendar>
      </div>

      <!--찜한 도서-->
      <div class="likedbook-list">
        <p class="likedbook-list-title">찜한도서❤</p>
        <Carousel :bookList="likeList" />
      </div>

      <!--작성한 리뷰-->
      <p class="review-list-title">작성한 리뷰 🎨</p>
      <div class="w-full h-60 py-20" v-if="reviewList.length < 1">
        <p>아직 작성한 리뷰가 없어요!</p>
      </div>
      <div class="review-list" v-else>
        <div
          class="review-items"
          v-for="(item, index) in reviewList"
          :key="index"
        >
          <div class="review-item">
            <div class="flex justify-between">
              <p class="review-item-title" @click="showDetail(item.book)">
                {{ item.book_title }}
              </p>
              <star-rating
                class="review-item-score"
                :rating="item.score"
                :star-size="15"
                :show-rating="false"
                :inline="true"
                :read-only="true"
              >
              </star-rating>
            </div>
            <div>
              <p class="review-item-content">{{ item.content }}</p>
            </div>
            <div>
              <p class="review-item-date">
                {{ item.updated_at.split("T")[0] }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useStore } from "vuex"
import { reactive, ref } from "@vue/reactivity"
import { onBeforeMount, computed } from "@vue/runtime-core"
import Carousel from "@/components/Carousel.vue"
import router from "@/router"
import StarRating from "vue-star-rating"

export default {
  name: "MyPage",
  components: {
    Carousel,
    StarRating,
  },
  setup() {
    const store = useStore()
    const userInfo = JSON.parse(localStorage.getItem("userInfo"))

    // true면 모달 open false면 close 상태
    const modal = ref(false)

    const access_token = localStorage.getItem("access_token")
    // 모달을 켰다 껐다 하는 버튼(edit, close)
    const toggleModal = () => {
      modal.value = !modal.value
      // 모달창을 여닫을때마다 모달창의 모든 정보를 초기화 시켜준다.
      modalPage.value = "one"
      activeEdit.value = ""
      password.new_password1 = ""
      password.new_password2 = ""
      pwStatus.value = ""
      pwCheck.value = ""
    }

    const readDate = computed(() => {
      return store.state.mypage.readDate
    })

    // 프로필에서 페이지를 토글
    const modalPage = ref("one")
    const togglePage = (num) => {
      activeEdit.value = ""
      modalPage.value = num

      const lst = ["one", "two", "three"]

      lst.forEach((item) => {
        if (num === item) {
          document.getElementById(item).className = "material-icons"
        } else {
          document.getElementById(item).className = "material-icons-outlined"
        }
      })
    }

    const password = reactive({
      new_password1: "",
      new_password2: "",
    })

    const changePassword = () => {
      store.dispatch("mypage/changePassword", { password, access_token })
    }

    const pwStatus = ref("")
    const pwCheck = ref("")
    const signOutPassword = ref("")

    const passwordValid = () => {
      if (
        /(?=.*[a-zA-ZS])(?=.*?[#?!@$%^&*-]).{7,17}/.test(password.new_password1)
      ) {
        pwStatus.value = true
      } else {
        pwStatus.value = false
      }
    }

    const passwordSame = () => {
      if (password.new_password1 === password.new_password2) {
        pwCheck.value = true
      } else {
        pwCheck.value = false
      }
    }

    const activeEdit = ref("")

    const editMode = (val) => {
      activeEdit.value = val
      newUserInfo.email = ""
      newUserInfo.last_name = ""
      newUserInfo.first_name = ""
    }

    const newUserInfo = reactive({
      email: "",
      last_name: "",
      first_name: "",
    })

    const editInfo = () => {
      store.dispatch("mypage/editInfo", { newUserInfo, access_token })
    }

    const deleteUser = () => {
      store.dispatch("mypage/deleteUser", { signOutPassword, access_token })
    }

    const masks = {
      weekdays: "WWW",
    }

    const attributes = computed(() => {
      return store.state.mypage.readList
    })

    const showDetail = (book_id) => {
      const bookItem = {
        book_id: book_id,
        access_token: localStorage.getItem("access_token"),
        userPk: localStorage.getItem("pk"),
      }

      store.dispatch("detail/getBookDetail", bookItem)
      setTimeout(() => {
        router.push({ name: "Detail" })
      }, 400)
    }

    const likeList = computed(() => {
      return store.state.mypage.likeList
    })

    const readList = computed(() => {
      return store.state.mypage.readList
    })

    const reviewList = computed(() => {
      return store.state.mypage.reviewList
    })

    onBeforeMount(() => {
      store.dispatch("mypage/getLike", access_token)
      store.dispatch("mypage/getRead", access_token)
      store.dispatch("mypage/getReview", access_token)
    })

    return {
      userInfo,
      masks,
      attributes,
      showDetail,
      toggleModal,
      modal,
      modalPage,
      togglePage,
      password,
      changePassword,
      pwStatus,
      passwordValid,
      pwCheck,
      passwordSame,
      activeEdit,
      editMode,
      newUserInfo,
      editInfo,
      signOutPassword,
      deleteUser,
      likeList,
      readList,
      reviewList,
      readDate,
    }
  },
}
</script>

<style lang="scss" scoped>
@font-face {
  font-family: "InfinitySans-RegularA1";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/InfinitySans-RegularA1.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}
//------------------------------------ 마이페이지 부분 ------------------------------------//
.mypage-bg {
  @apply w-2/3 md:w-3/4 lg:w-full mx-auto pb-12;
  background-color: #f0e5de;

  .user-profile {
    @apply mt-2 inline;

    .nickname {
      @apply relative float-left ml-4 mt-2 inline;
      font-size: 30px;
      font-family: "InfinitySans-RegularA1";
    }
  }

  .user-profile-book {
    @apply clear-left pt-4 mt-20;

    .read-book-cnt {
      @apply w-1/3 float-left border-r-2 border-gray-400;
    }

    .liked-book-cnt {
      @apply w-1/3 float-left border-r-2 border-gray-400;
    }

    .recent-read-date {
      @apply w-1/3 float-left;
    }
  }

  .custom-calendar {
    .calendar-group {
      @apply flex flex-col h-full z-10 overflow-hidden;

      .day-label {
        @apply text-sm text-gray-900;
      }

      .calendar-content {
        @apply flex-grow overflow-scroll overflow-y-auto overflow-x-auto;
        .calendar-text {
          @apply text-xs leading-tight rounded-sm p-1 mt-0 mb-1 cursor-pointer;
        }
      }
      .calendar-content::-webkit-scrollbar {
        display: none;
      }
    }
  }

  .likedbook-list {
    @apply mt-5 text-xl;
    font-family: "InfinitySans-RegularA1";
    .likedbook-list-title {
      @apply mx-9 mb-2 text-left;
    }
  }

  .review-list-title {
    @apply mx-9 mt-6 text-left text-xl;
  }
  .review-list {
    @apply mb-12 text-center grid grid-cols-2 gap-2 mx-8;
    font-family: "InfinitySans-RegularA1";
    .review-items {
      @apply bg-yellow-100 rounded-lg mt-5;
      .review-item {
        @apply p-3 flex flex-col;

        .review-item-title {
          @apply text-xl font-semibold cursor-pointer underline hover:text-blue-700 pl-2;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 1; /* 라인수 */
          -webkit-box-orient: vertical;
          word-wrap: break-word;
        }
        .review-item-score {
          @apply ml-2;
        }

        .review-item-content {
          @apply text-left pl-2 pr-4;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 1; /* 라인수 */
          -webkit-box-orient: vertical;
          word-wrap: break-word;
        }
        .review-item-date {
          @apply text-right;
        }
      }
    }
  }
}

//------------------------------------ 모달 부분 ------------------------------------//
.backdrop {
  @apply absolute z-20 w-2/5 opacity-80;
  background: rgba(0, 0, 0, 0.8);
  top: 0;
  height: 156vh;
}

.edit-modal {
  @apply z-30 bg-white rounded-2xl border shadow-xl flex flex-col justify-evenly sm:w-1/2 lg:w-1/5 w-3/5;
  position: fixed;
  margin: 10% auto;
  left: 0;
  right: 0;

  span {
    @apply cursor-pointer;
  }

  .modal-header {
    @apply flex justify-between p-4 flex-none;

    .close-btn {
      @apply text-red-600;
    }
  }

  .modal-body {
    @apply text-left p-4 text-lg flex flex-col flex-1;

    .content {
      @apply flex items-center;

      .content-name {
        @apply w-16;
      }

      .content-info {
        @apply w-56;
      }

      .content-input {
        @apply w-56 border-2 px-1;
      }
    }

    .input {
      @apply w-1/2 border-gray-300 border-2 rounded-md px-1;
    }

    button {
      @apply bg-gray-600 w-20 text-white rounded-3xl h-8 shadow-md ml-auto mt-auto;
    }

    .active {
      @apply bg-blue-600;
    }

    .nope {
      @apply bg-red-500 pointer-events-none;
    }
    p {
      @apply my-3;
    }
  }

  .modal-footer {
    @apply flex-none px-4 py-1.5;

    span {
      @apply text-right;
    }
  }
}
</style>
