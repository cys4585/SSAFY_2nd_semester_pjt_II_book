<template>
  <div class="wrapper">
    <div class="header">
      <h1>회원가입</h1>
    </div>
    <div class="content">
      <div class="input-form">
        <input
          type="text"
          class="input"
          v-model="userInfo.username"
          @focus="clear"
          @input="usernameValid"
          @blur="nameDuplicateCheck"
          placeholder="name@example.com"
          autocomplete="off"
        />
        <label for="email" class="label">아이디</label>
        <p class="text-red-500 pt-1" v-if="usernameStatus === false">
          5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.
        </p>
        <p class="text-red-500 pt-1" v-if="dupName == 200">
          중복된 아이디입니다.
        </p>
        <p class="text-green-500 pt-1" v-else-if="dupName == 204">
          사용 가능한 아이디입니다.
        </p>
      </div>
      <div class="input-form">
        <form>
          <input
            type="password"
            id="password"
            class="input"
            placeholder="password"
            autocomplete="off"
            v-model="userInfo.password"
            @focus="pwClear"
            @input="passwordValid"
          />
          <label for="password" class="label">비밀번호</label>
          <p class="text-red-500 pt-1" v-if="pwStatus === false">
            8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.
          </p>
        </form>
      </div>
      <div class="input-form">
        <form>
          <input
            type="password"
            id="password2"
            class="input"
            placeholder="password2"
            autocomplete="off"
            v-model="userInfo.password2"
            @focus="checkClear"
            @input="passwordSame"
          />
          <label for="password2" class="label">비밀번호 확인</label>
          <p class="text-red-500 pt-1" v-if="pwCheck === false">
            비밀번호가 일치하지 않습니다.
          </p>
        </form>
      </div>
      <div class="input-form">
        <input
          type="email"
          class="input"
          v-model="userInfo.email"
          placeholder="name@example.com"
          autocomplete="off"
          @focus="emailClear"
          @input="emailValid"
          @blur="mailDuplicateCheck"
        />
        <label for="email" class="label">이메일</label>
        <p class="text-red-500 pt-1" v-if="emailStatus === false">
          이메일 주소를 다시 확인해주세요.
        </p>
        <p class="text-red-500 pt-1" v-if="dupMail == 200">
          중복된 이메일입니다.
        </p>
        <p class="text-green-500 pt-1" v-else-if="dupMail == 204">
          사용 가능한 이메일입니다.
        </p>
      </div>
      <div class="flex gap-4">
        <div class="input-form flex-1">
          <input
            type="lastname"
            id="lastname"
            class="input"
            placeholder="lastname"
            autocomplete="off"
            v-model="userInfo.last_name"
            @input="nameValid"
          />
          <label for="lastname" class="label">성</label>
        </div>
        <div class="input-form flex-1">
          <input
            type="firstname"
            id="firstname"
            class="input"
            placeholder="firstname"
            autocomplete="off"
            v-model="userInfo.first_name"
            @input="nameValid"
          />
          <label for="firstname" class="label">이름</label>
        </div>
      </div>
      <p class="text-red-500 pt-1" v-if="nameStatus === false">
        이름을 정확히 입력해주세요.
      </p>
      <!-- <p class="text-red-500 pt-1" v-if="pwCheck === false">
          비밀번호가 일치하지 않습니다.
        </p> -->
      <div class="btn-group">
        <button
          class="btn pointer-events-none"
          v-if="
            usernameStatus === '' &&
            pwStatus === '' &&
            pwStatus === '' &&
            emailStatus === ''
          "
        >
          회원가입
        </button>
        <button
          class="btn nope"
          v-else-if="
            usernameStatus === false ||
            pwCheck === false ||
            pwStatus === false ||
            emailStatus === false
          "
        >
          회원가입
        </button>
        <button @click="signUp" class="btn ok" v-else>회원가입</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex"
import { reactive, ref } from "@vue/reactivity"
import { computed } from "vue"
import router from "@/router"

export default {
  name: "Signup",
  components: {},
  setup() {
    const store = useStore()

    const pwStatus = ref("")
    const emailStatus = ref("")
    const pwCheck = ref("")
    const usernameStatus = ref("")
    const nameStatus = ref("")
    const mailStatus = ref("")

    const dupName = computed(() => {
      return store.state.auth.userStatus
    })

    const dupMail = computed(() => {
      return store.state.auth.mailStatus
    })

    const clear = () => {
      usernameStatus.value = true
      dupName.value = ""
    }

    const pwClear = () => {
      pwStatus.value = true
    }

    const checkClear = () => {
      pwCheck.value = true
    }

    const emailClear = () => {
      emailStatus.value = true
    }

    const usernameValid = () => {
      if (/^[A-Za-z0-9_-]{5,21}$/.test(userInfo.username)) {
        // if (/^[A-Za-z]{1}[A-Za-z0-9_-]{5,13}$/.test(userInfo.username)) {
        usernameStatus.value = true
      } else {
        usernameStatus.value = false
      }
    }

    const nameDuplicateCheck = () => {
      if (userInfo.username.length > 4) {
        store.dispatch("auth/nameDuplicateCheck", userInfo.username)
      }
    }

    const passwordValid = () => {
      if (/(?=.*[a-zA-ZS])(?=.*?[#?!@$%^&*-]).{7,17}/.test(userInfo.password)) {
        pwStatus.value = true
      } else {
        pwStatus.value = false
      }
    }
    const passwordSame = () => {
      if (userInfo.password === userInfo.password2) {
        pwCheck.value = true
      } else {
        pwCheck.value = false
      }
    }

    const emailValid = () => {
      if (
        /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}/.test(
          userInfo.email
        )
      ) {
        emailStatus.value = true
      } else {
        emailStatus.value = false
      }
    }

    const mailDuplicateCheck = () => {
      if (userInfo.email.length > 7) {
        store.dispatch("auth/mailDuplicateCheck", userInfo.email)
      }
    }

    const nameValid = () => {
      if (
        /^[가-힣a-zA-Z]/.test(userInfo.last_name) &&
        /^[가-힣a-zA-Z]/.test(userInfo.first_name)
      ) {
        nameStatus.value = true
      } else {
        nameStatus.value = false
      }
    }

    const userInfo = reactive({
      username: "",
      password: "",
      password2: "",
      email: "",
      last_name: "",
      first_name: "",
    })
    const signUp = () => {
      store.dispatch("auth/signUp", userInfo)
    }

    return {
      userInfo,
      signUp,
      usernameValid,
      usernameStatus,
      clear,
      passwordValid,
      pwStatus,
      pwClear,
      checkClear,
      passwordSame,
      pwCheck,
      emailValid,
      emailStatus,
      emailClear,
      nameValid,
      nameStatus,
      nameDuplicateCheck,
      dupName,
      mailStatus,
      dupMail,
      mailDuplicateCheck,
    }
  },
}
</script>

<style lang="scss" scoped>
p {
  @apply text-sm text-left pl-2;
}

.wrapper {
  @apply w-3/5 mx-auto pb-32;

  .header {
    @apply py-10;

    h1 {
      @apply text-3xl;
    }
  }

  .content {
    .input-form {
      @apply my-4 relative rounded-xl;

      .input {
        @apply border border-gray-200 focus:outline-none rounded-2xl focus:border-gray-500 focus:shadow-sm w-full p-3 h-14 shadow-md;
      }

      input::placeholder {
        color: transparent;
      }
      input:focus,
      input:not(:placeholder-shown) {
        @apply pt-8;
      }
      input:focus ~ label,
      input:not(:placeholder-shown) ~ label {
        @apply opacity-75 scale-75 -translate-y-3 translate-x-1;
      }

      .label {
        @apply absolute top-0 left-0 px-3 py-4 h-full pointer-events-none transform origin-left transition-all duration-100 ease-in-out;
      }
    }
    .btn-group {
      @apply my-8;

      .btn {
        @apply w-20 h-10 bg-gray-400 rounded-md text-white shadow-md;
      }
      .nope {
        @apply bg-red-600 cursor-not-allowed;
      }
      .ok {
        @apply bg-blue-500;
      }
    }
  }
}
</style>
