<template>
  <div class="accounts-wrapper">
    <section>
      <SearchBar />
      <router-view />
      <Footer v-if="$route.fullPath.includes('sign')" />
    </section>
  </div>
</template>

<script>
import Footer from "@/components/Footer.vue"
import SearchBar from "@/components/SearchBar.vue"

export default {
  name: "AccountsLayout",
  components: { Footer, SearchBar },
  setup() {
    return {}
  },
}
</script>

<style lang="scss" scoped>
.accounts-wrapper {
  background-color: #f0e5de;

  section {
    @apply min-h-screen mx-auto shadow-2xl sm:w-full lg:w-2/5;
  }
}
</style>
