<template>
  <div v-if="products">
    <button @click="firstPage">First</button>
    <button @click="previousPage">Previous</button>
    <button @click="page(getParams.page - 3)" v-if="getParams.page > 3">{{ getParams.page - 3}}</button>
    <button @click="page(getParams.page - 2)" v-if="getParams.page > 2">{{ getParams.page - 2}}</button>
    <button @click="page(getParams.page - 1)" v-if="getParams.page > 1">{{ getParams.page - 1}}</button>
    <button @click="page(getParams.page)" style="background-color: red">{{ getParams.page }}</button>
    <button @click="page(getParams.page + 1)" v-if="getParams.page <= nbPage - 1">{{ getParams.page + 1}}</button>
    <button @click="page(getParams.page + 2)" v-if="getParams.page <= nbPage - 2">{{ getParams.page + 2}}</button>
    <button @click="page(getParams.page + 3)" v-if="getParams.page <= nbPage - 3">{{ getParams.page + 3}}</button>
    <button @click="nextPage">Next</button>
    <button @click="lastPage">Last</button>
    <ul id="products-list" v-if="products.length > 0">
      <li :key="i" v-for="(product, i) in products">
        <router-link :to="{name: 'Product', params: {id: product._id}}" tag="a">
          <figure>
            <img :src="$store.state.serverUrl + '/api/image/' + product.store + '/' + product.image_name + '.jpg'" :alt="product.name"/>
            <figcaption>
              <div class="product-name">{{product.name}}</div>
              <div class="product-price price">
                <template v-if="product.minPrice === product.maxPrice">
                  {{product.price}} {{product.currency | currencySymbol}}
                </template>
                <template v-else>
                  {{product.minPrice}} {{product.currency | currencySymbol}} - {{product.maxPrice}} {{product.currency | currencySymbol}}
                </template>
              </div>
              <div>
                {{ product.similarities.length + 1 }} offre{{ product.similarities.length + 1 > 1 ? 's' : '' }}
              </div>
            </figcaption>
          </figure>
        </router-link>
      </li>
    </ul>
    <div v-else>
      <p>Aucun produit ne correspond à votre recherche.</p>
    </div>
  </div>
  <div v-else>
    <loader></loader>
  </div>
</template>

<script>
import axios from 'axios'
import Loader from '@/components/Loader'
import { mapGetters } from 'vuex'

export default {
  name: 'products',
  components: {
    Loader
  },
  data () {
    return {
      getParams: {
        search: '',
        page: 1
      },
      products: null,
      nbPage: null
    }
  },
  watch: {
    '$route': function (newRoute, oldRoute) {
      this.getParams.search = newRoute.query.search ? newRoute.query.search : ''
      this.getParams.page = newRoute.query.page ? newRoute.query.page : 1
      this.fetchProducts()
    },
    productsSearch (search, oldSearch) {
      this.getParams.search = search
      this.getParams.page = 1
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    }
  },
  mounted () {
    this.getParams.search = this.$route.query.search ? this.$route.query.search : ''
    this.getParams.page = this.$route.query.page ? this.$route.query.page : 1
    this.fetchProducts()
  },
  methods: {
    updateRoute (query) {
      let finalQuery = {}
      if (query.page !== 1) {
        finalQuery.page = query.page
      }
      finalQuery.search = query.search
      this.$router.push({name: 'Products', query: finalQuery})
    },
    firstPage () {
      if (this.getParams.page === 1) {
        return
      }
      this.getParams.page = 1
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    },
    previousPage () {
      if (this.getParams.page <= 1) {
        return
      }
      this.getParams.page--
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    },
    page (page) {
      if (this.getParams.page === page) {
        return
      }
      this.getParams.page = page
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    },
    nextPage () {
      if (this.getParams.page >= this.nbPage) {
        return
      }
      this.getParams.page++
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    },
    lastPage () {
      if (this.getParams.page === this.nbPage) {
        return
      }
      this.getParams.page = this.nbPage
      this.updateRoute({page: this.getParams.page, search: this.getParams.search})
      this.fetchProducts()
    },
    fetchProducts () {
      this.products = null
      axios.get(this.buildUrl()).then(response => {
        this.products = response.data.products
        this.nbPage = response.data.nbPage
      }, error => {
        console.log(error)
      })
    },
    buildUrl () {
      let url = this.$store.state.serverUrl + '/api/products'
      Object.keys(this.getParams).map((param, i) => {
        if (i === 0) {
          url += '?'
        } else {
          url += '&'
        }
        url += param + '=' + this.getParams[param]
      })
      return url
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
  #products-list {
    display: flex;
    flex-wrap: wrap;

    li {
      display: flex;
      width: calc((100% - 30px) / 4);
      border: 1px solid #E7E7E7;
      margin-bottom: 10px;

      &:not(:nth-child(4n+0)) {
        margin-right: 10px;
      }

      a {
        display: block;
        padding: 20px;

        &:hover img {
          transform: scale(0.95);
        }

        img {
          width: 100%;
          transition: transform 150ms ease-out;
        }

        figcaption {
          margin-top: 20px;

          .product-name {
            color: #000000;
            font-size: 1.6rem;
          }

          .product-price {
            margin-top: 10px;
          }
        }
      }
    }
  }
</style>
