<template>
  <div id="search-wrapper" :class="mainClass">
    <form>
      <input type="text" v-model="search" :placeholder="placeholder"/>
      <button @click="doSearch"></button>
    </form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'search',
  props: ['mainClass'],
  data () {
    return {
      search: '',
      placeholder: ''
    }
  },
  created () {
    this.search = this.$store.state.products_search
    this.placeholder = this.mainClass === 'home' ? 'Que désirez-vous...' : ''
  },
  methods: {
    doSearch () {
      if (this.$route.name === 'Products') {
        this.$store.commit('PRODUCTS_SEARCH', this.search)
      } else {
        this.$store.commit('PRODUCTS_SEARCH', this.search)
        this.$router.push({name: 'Products', query: {search: this.search}})
      }
    }
  },
  watch: {
    productsSearch (search, oldSearch) {
      this.search = search
    }
  },
  computed: {
    ...mapGetters({
      productsSearch: 'getProductsSearch'
    })
  }
}
</script>

<style scoped lang="scss">
  #search-wrapper {
    display: flex;

    & > form {
      display: flex;
      height: 35px;

      input[type='text'] {
        border: 1px solid $grey;
        background-color: transparent;
        color: #FFFFFF;
        padding: 5px;
        border-radius: 2px 0 0 2px;
      }

      button {
        background: url('/static/img/icons/search.png') no-repeat center center;
        background-size: auto 50%;
        cursor: pointer;
        transition: background-size .2s ease-in-out;
        border: 1px solid $grey;
        border-left: none;
        border-radius:  0 2px 2px 0;
        width: 50px;

        &:hover {
          background-size: auto 60%;
        }
      }
    }
  }

  .home {
    width: 100%;
    justify-content: center;
    background-color: $black-opacity;
    padding: 10px;

    & > form {

      input[type='text'] {
        font-size: 1.5rem;
        width: 300px;
      }
    }
  }

  .nav {
    padding: 10px;
    align-items: center;

    & > form {

      input[type='text'] {
        font-size: 1.5rem;
        width: 200px;
        transition: width .2s ease-in-out;

        &:focus {
          width: 300px;
        }
      }
    }
  }
</style>
