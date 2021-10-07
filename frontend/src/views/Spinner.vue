<template>
  <div>
    <div class="spinner-wrapper">
      <div class="spinner-content">
        <img :src="require(`@/assets/book.png`)" class="" alt="" />
        <div class="spinner-words hidden" id="1">
          <p>책 없는 방은 영혼 없는 육체와 같다.</p>
          <p>-키케로-</p>
        </div>
        <div class="spinner-words hidden" id="2">
          <p>하루라도 책을 읽지 않으면 입에 가시가 돋는다.</p>
          <p>-안중근-</p>
        </div>
        <div class="spinner-words hidden" id="3">
          <p>
            좋은 책을 읽는 것은 과거의 가장 뛰어난 사람들과 대화를 나누는 것과
            같다.
          </p>
          <p>-데카르트-</p>
        </div>
        <div class="spinner-words hidden" id="4">
          <p>독서의 참다운 기쁨은 몇 번이고 다시 읽는 것이다.</p>
          <p>-로렌스-</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from "@vue/runtime-core"
export default {
  name: "Spinner",
  components: {},
  setup() {
    const arr = [1, 2, 3, 4]

    const random_words = (arr) => {
      const pick = arr[Math.floor(Math.random() * arr.length)]
      document.getElementById(pick).classList.remove("hidden")
    }

    onMounted(() => {
      random_words(arr)
    })

    return {
      random_words,
    }
  },
}
</script>

<style lang="scss" scoped>
.spinner-wrapper {
  @apply max-w-sm mx-auto mt-24;

  .spinner-content {
    @apply h-80 flex items-center;

    .spinner-words {
      @apply animate-pulse absolute w-64 text-center;
      left: 50%;
      transform: translateX(-50%);
    }
  }
}
</style>
