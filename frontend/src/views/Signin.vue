<template>
  <div class="wrapper">
    <div class="header"><h1>로그인</h1></div>
    <div class="content">
      <div class="input-form">
        <input
          type="text"
          name="signin-id"
          class="input"
          placeholder="이메일을 입력해주세요"
          @input="usernameValid"
          v-model="signinForm.id"
        />
        <label for="email" class="label">아이디</label>
        <p class="text-red-500 pt-1" v-if="usernameStatus === false">
          5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.
        </p>
      </div>
      <div class="input-form">
        <input
          type="password"
          name="signin-password"
          id="signin-password"
          class="input"
          placeholder="비밀번호를 입력해주세요"
          v-model="signinForm.password"
          autocomplete="off"
          @keyup.enter="signin"
        />
        <label for="password" class="label">비밀번호</label>
      </div>
    </div>
    <div>
      <button
        class="signin-button"
        :class="{ active: isActive === true }"
        @click="signin"
      >
        로그인
      </button>
    </div>
    <div class="signup-button">
      <span>아직 회원이 아니신가요?</span><br />
      <router-link class="signup-span" :to="{ name: 'Signup' }"
        >회원가입 하기
      </router-link>
    </div>
    <!-- <div class="signup-button mt-4">
      <span>비밀번호를 잊으셨나요?</span><br />
      <router-link class="signup-span" :to="{ name: 'PasswordReset' }"
        >비밀번호 재설정하기
      </router-link>
    </div> -->
  </div>
</template>

<script>
import { reactive, ref } from "@vue/reactivity"
import { watch } from "@vue/runtime-core"
import { useStore } from "vuex"

export default {
  name: "Signin",
  components: {},
  setup() {
    const store = useStore()
    const signinForm = reactive({
      id: "",
      password: "",
    })
    const isActive = ref(false)
    const usernameStatus = ref("")

    const usernameValid = () => {
      if (/^[A-Za-z0-9_-]{5,21}$/.test(signinForm.id)) {
        usernameStatus.value = true
      } else {
        usernameStatus.value = false
      }
    }

    const signin = () => {
      store.dispatch("auth/signin", signinForm)
    }

    const isValidate = () => {
      if (
        signinForm.id.length > 4 &&
        signinForm.password.length > 4 &&
        usernameStatus.value
      ) {
        isActive.value = true
      }
    }

    watch(
      () => signinForm.id,
      (id, prevId) => {
        if (id.length > 0) {
          isValidate()
        }
      }
    )

    watch(
      () => signinForm.password,
      (password, prevPassword) => {
        if (password.length > 0) {
          isValidate()
        }
      }
    )

    return {
      signinForm,
      isActive,
      isValidate,
      signin,
      usernameValid,
      usernameStatus,
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

//class가 4개 이상이면 tailwind로 apply해주기
* {
  font-family: "InfinitySans-RegularA1";
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
  }

  .signin-button {
    @apply w-20 h-10 bg-gray-400 rounded-md text-white my-12 pointer-events-none shadow-md;
    // background-color: saddlebrown;
  }
  .signin-button.active {
    @apply bg-blue-500  pointer-events-auto;
  }

  .signup-button {
    @apply text-base;

    .signup-span {
      @apply underline hover:text-blue-700 cursor-pointer;
    }
  }
}
</style>
