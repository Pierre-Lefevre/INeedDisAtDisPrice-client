<template>
  <div>
    <input type="text" v-model="search"/>
    <button @click="doSearch">search</button>
  </div>
</template>

<script>
export default {
  name: 'search',
  data () {
    return {
      search: ''
    }
  },
  methods: {
    doSearch () {
      if (this.$route.name === 'Products') {
        this.$store.commit('PRODUCTS_SEARCH', this.search)
      } else {
        this.$router.push({name: 'Products', query: {search: this.search}})
      }
    }
  }
}
</script>

<style scoped>

</style>
