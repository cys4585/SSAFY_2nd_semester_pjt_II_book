<template>
  <div class="main-wrapper">
    <section>
      <p class="h-60 txt">
        잘못된 경로로 왔어요. <br /><br />
        <a
          class="underline hover:text-blue-700 cursor-pointer"
          href="http://j5d203.p.ssafy.io"
        >
          돌아갑시다!</a
        >
      </p>
    </section>
  </div>
</template>

<script>
export default {
  name: "NotFound",
  components: {},
  setup() {
    return {}
  },
}
</script>

<style lang="scss" scoped>
.main-wrapper {
  background-color: #f0e5de;
  section {
    @apply w-full h-auto min-h-screen mx-auto shadow-2xl sm:w-full lg:w-2/5;
    .txt {
      @apply text-3xl;
      padding: 50% 0;
    }
  }
}
</style>
