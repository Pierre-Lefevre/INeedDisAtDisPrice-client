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
        let query = {}
        if (this.search !== '') {
          query.search = this.search
        }
        this.$router.push({name: 'Products', query})
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
        color: #FFFFFF;
        padding: 5px;
        border-radius: 2px 0 0 2px;
      }

      button {
        background-size: auto 50%;
        cursor: pointer;
        transition: background-size .2s ease-in-out;
        border: 1px solid $grey;
        border-left: none;
        border-radius: 0 2px 2px 0;
        width: 50px;

        &:hover {
          background-size: auto 60%;
        }
      }
    }
  }

  .home > form {
    margin: 10px;

    input[type='text'] {
      background-color: $black-opacity;
      font-size: 1.5rem;
      width: 300px;
    }

    button {
      background: $black-opacity url('/static/img/icons/search.png') no-repeat center center;
    }
  }

  .nav {
    padding: 10px;
    align-items: center;

    & > form {

      input[type='text'] {
        font-size: 1.5rem;
        background-color: transparent;
        width: 200px;
        transition: width .2s ease-in-out;

        &:focus {
          width: 300px;
        }
      }

      button {
        background: transparent url('/static/img/icons/search.png') no-repeat center center;
      }
    }
  }
</style>
