<template>
  <div class="footer-wrapper">
    <div class="pt-4">
      <span>(주) 북적북적</span>
      <div class="flex justify-evenly px-24 mt-2">
        <a
          href="mailto:iamlegend_@naver.com?subject=북적북적 문의사항&body=질문이 있으시다면 메일을 보내주세요."
          >문의하기</a
        >
        <!-- <p>문의하기</p> -->
        |
        <p>고객센터</p>
        <!-- <router-link :to="{ name: 'Member' }">고객센터</router-link> -->
        |
        <p>공지사항</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Footer",
  components: {},
  setup() {
    return {}
  },
}
</script>

<style lang="scss" scoped>
.footer-wrapper {
  @apply h-24 mx-auto shadow-inner lg:w-2/5 w-full bg-white;
  position: fixed;
  bottom: 0;
}
</style>
