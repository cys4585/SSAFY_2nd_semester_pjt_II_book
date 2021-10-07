<template>
  <div class="wrapper">
    <router-link :to="{ name: 'Home' }"
      ><span class="material-icons"> home </span></router-link
    >
    <router-link :to="{ name: 'Search' }"
      ><span class="material-icons"> explore </span>
    </router-link>
    <router-link :to="{ name: 'MyPage' }"
      ><span class="material-icons"> account_circle </span></router-link
    >
  </div>
</template>

<script>
export default {
  name: "NavBar",
  components: {},
  setup() {
    return {}
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  @apply sm:w-full lg:w-2/5 bg-blue-300 flex justify-around h-20 align-middle fixed bottom-0 w-full shadow-inner;

  .router-link-exact-active {
    @apply text-indigo-600;
  }

  .material-icons {
    @apply text-5xl leading-relaxed;
  }
}
</style>
