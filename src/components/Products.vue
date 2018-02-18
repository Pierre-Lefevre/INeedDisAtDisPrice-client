<template>
  <div id="products-wrapper">
    <div id="filter">
      <div id="price-filter">
        <p>Prix&nbsp;:</p>
        <span>
          <template v-if="parseInt(getParams.minPrice) < parseInt(getParams.maxPrice)">{{ getParams.minPrice }}</template>
          <template v-else>{{ getParams.maxPrice }}</template>
        </span>
        <div class="range-slider">
          <input v-model="getParams.minPrice" :min="minPriceBound" :max="maxPriceBound" step="1" type="range"/>
          <input v-model="getParams.maxPrice" :min="minPriceBound" :max="maxPriceBound" step="1" type="range"/>
        </div>
        <span>
          <template v-if="parseInt(getParams.maxPrice) > parseInt(getParams.minPrice)">{{ getParams.maxPrice }}</template>
          <template v-else>{{ getParams.minPrice }}</template>
        </span>
      </div>
      <button class="my-button" @click="filter">Filtrer</button>
      <button class="my-button" @click="filterReset">Annuler</button>
    </div>
    <div class="pagination">
      <button :class="{disable: getParams.page === 1}" @click="firstPage">&#60;&#60;</button>
      <button :class="{disable: getParams.page === 1}" @click="previousPage">&#60;</button>
      <button @click="page(getParams.page - 3)" v-if="getParams.page > 3">{{ getParams.page - 3 }}</button>
      <button @click="page(getParams.page - 2)" v-if="getParams.page > 2">{{ getParams.page - 2 }}</button>
      <button @click="page(getParams.page - 1)" v-if="getParams.page > 1">{{ getParams.page - 1 }}</button>
      <button class="current" @click="page(getParams.page)">{{ getParams.page }}</button>
      <button @click="page(getParams.page + 1)" v-if="getParams.page <= nbPage - 1">{{ getParams.page + 1 }}</button>
      <button @click="page(getParams.page + 2)" v-if="getParams.page <= nbPage - 2">{{ getParams.page + 2 }}</button>
      <button @click="page(getParams.page + 3)" v-if="getParams.page <= nbPage - 3">{{ getParams.page + 3 }}</button>
      <button :class="{disable: getParams.page === nbPage}" @click="nextPage">&#62;</button>
      <button :class="{disable: getParams.page === nbPage}" @click="lastPage">&#62;&#62;</button>
    </div>
    <div v-if="products">
      <div v-if="products.length > 0">
        <ul id="products-list" v-if="products.length > 0">
          <li :key="i" v-for="(product, i) in products">
            <router-link :to="{name: 'Product', params: {id: product._id}}" tag="a">
              <figure>
                <img :src="$store.state.serverUrl + '/api/image/' + product.store + '/' + product.image_name + '.jpg'" :alt="product.name"/>
                <figcaption>
                  <div class="product-name">{{product.name}}</div>
                  <div class="product-price price">{{ product.price }} {{ product.currency | currencySymbol }}</div>
                  <template v-if="product.similarities.length > 0">
                    <div class="product-offer">
                      {{ product.similarities.length }} offre{{ product.similarities.length > 1 ? 's' : '' }}
                      <template v-if="product.minPrice === product.maxPrice">
                        à <span class="price">{{ product.minPrice }} {{ product.currency | currencySymbol }}</span>
                      </template>
                      <template v-else>
                        entre <span class="price">{{ product.minPrice }} {{ product.currency | currencySymbol }} - {{ product.maxPrice }} {{ product.currency | currencySymbol }}</span>
                      </template>
                    </div>
                  </template>
                </figcaption>
              </figure>
            </router-link>
          </li>
        </ul>
      </div>
      <div class="no-product" v-else>
        <div class="notification notification-info">
          <p>Aucun produit ne correspond à votre recherche.</p>
        </div>
      </div>
    </div>
    <div v-else>
      <loader mainClass="products"/>
    </div>
    <div class="pagination">
      <button :class="{disable: getParams.page === 1}" @click="firstPage">&#60;&#60;</button>
      <button :class="{disable: getParams.page === 1}" @click="previousPage">&#60;</button>
      <button @click="page(getParams.page - 3)" v-if="getParams.page > 3">{{ getParams.page - 3}}</button>
      <button @click="page(getParams.page - 2)" v-if="getParams.page > 2">{{ getParams.page - 2}}</button>
      <button @click="page(getParams.page - 1)" v-if="getParams.page > 1">{{ getParams.page - 1}}</button>
      <button class="current" @click="page(getParams.page)">{{ getParams.page }}</button>
      <button @click="page(getParams.page + 1)" v-if="getParams.page <= nbPage - 1">{{ getParams.page + 1}}</button>
      <button @click="page(getParams.page + 2)" v-if="getParams.page <= nbPage - 2">{{ getParams.page + 2}}</button>
      <button @click="page(getParams.page + 3)" v-if="getParams.page <= nbPage - 3">{{ getParams.page + 3}}</button>
      <button :class="{disable: getParams.page === nbPage}" @click="nextPage">&#62;</button>
      <button :class="{disable: getParams.page === nbPage}" @click="lastPage">&#62;&#62;</button>
    </div>
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
        page: 1,
        minPrice: -1,
        maxPrice: -1
      },
      products: null,
      nbPage: 1,
      minPriceBound: 0,
      maxPriceBound: 0
    }
  },
  watch: {
    '$route': function (newRoute, oldRoute) {
      this.getParams.search = newRoute.query.search ? newRoute.query.search : ''
      this.getParams.page = newRoute.query.page ? parseInt(newRoute.query.page) : 1
      this.getParams.minPrice = newRoute.query.minPrice ? parseInt(newRoute.query.minPrice) : -1
      this.getParams.maxPrice = newRoute.query.maxPrice ? parseInt(newRoute.query.maxPrice) : -1
      this.fetchProducts()
    },
    productsSearch (search, oldSearch) {
      this.getParams.search = search
      this.getParams.page = 1
      this.updateRoute()
    }
  },
  mounted () {
    this.getParams.search = this.$route.query.search ? this.$route.query.search : ''
    this.getParams.page = this.$route.query.page ? parseInt(this.$route.query.page) : 1
    this.getParams.minPrice = this.$route.query.minPrice ? parseInt(this.$route.query.minPrice) : -1
    this.getParams.maxPrice = this.$route.query.maxPrice ? parseInt(this.$route.query.maxPrice) : -1
    this.fetchProducts()
  },
  methods: {
    updateRoute () {
      if (this.getParams.minPrice > this.getParams.maxPrice) {
        let tmp = this.getParams.minPrice
        this.getParams.minPrice = this.getParams.maxPrice
        this.getParams.maxPrice = tmp
      }
      let query = {}
      if (this.getParams.search !== '') {
        query.search = this.getParams.search
      }
      if (this.getParams.page !== 1) {
        query.page = this.getParams.page
      }
      if (this.getParams.minPrice !== -1) {
        query.minPrice = this.getParams.minPrice
      }
      if (this.getParams.maxPrice !== -1) {
        query.maxPrice = this.getParams.maxPrice
      }
      this.$router.push({name: 'Products', query})
    },
    firstPage () {
      if (this.getParams.page === 1) {
        return
      }
      this.getParams.page = 1
      this.updateRoute()
    },
    previousPage () {
      if (this.getParams.page <= 1) {
        return
      }
      this.getParams.page--
      this.updateRoute()
    },
    page (page) {
      if (this.getParams.page === page) {
        return
      }
      this.getParams.page = page
      this.updateRoute()
    },
    nextPage () {
      if (this.getParams.page >= this.nbPage) {
        return
      }
      this.getParams.page++
      this.updateRoute()
    },
    lastPage () {
      if (this.getParams.page === this.nbPage) {
        return
      }
      this.getParams.page = this.nbPage
      this.updateRoute()
    },
    filter () {
      this.updateRoute()
    },
    filterReset () {
      this.getParams.minPrice = -1
      this.getParams.maxPrice = -1
      this.updateRoute()
    },
    fetchProducts () {
      this.products = null
      axios.get(this.buildUrl()).then(response => {
        this.products = response.data.products
        this.nbPage = parseInt(response.data.nbPage) > 0 ? parseInt(response.data.nbPage) : 1
        this.minPriceBound = parseInt(response.data.min)
        this.maxPriceBound = parseInt(response.data.max)
        this.getParams.minPrice = this.minPriceBound
        this.getParams.maxPrice = this.maxPriceBound
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
  #products-wrapper {
    min-height: calc(100vh - 60px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  #filter {
    margin: 20px 20px 0 20px;

    #price-filter {
      display: flex;
      margin-bottom: 20px;
      align-items: center;

      p, span {
        font-size: 1.5rem;
      }

      span {
        margin: 0 10px;
        text-align: center;
      }

      .range-slider {
        position: relative;
        max-width: 200px;
        width: 100%;
        height: 35px;
        text-align: center;
        display: flex;
        align-items: center;

        input[type=range] {
          pointer-events: none;
          position: absolute;
          overflow: hidden;
          top: 0;
          bottom: 0;
          max-width: 200px;
          width: 100%;
          outline: none;
          height: 18px;
          margin: auto;

          &::-webkit-slider-thumb {
            pointer-events: all;
            position: relative;
            z-index: 1;
            outline: 0;
          }

          &::-moz-range-thumb {
            pointer-events: all;
            position: relative;
            z-index: 10;
            /*-moz-appearance: none;*/
          }

          &::-moz-range-track {
            position: relative;
            z-index: -1;
            background-color: $black;
            border: 0;
          }

          &:last-of-type::-moz-range-track {
            /*-moz-appearance: none;*/
            background: none transparent;
            border: 0;
          }

          &::-moz-focus-outer {
            border: 0;
          }
        }
      }
    }

    button:not(:last-of-type) {
      margin-right: 10px;
    }
  }

  .pagination {
    display: flex;
    justify-content: center;
    padding: 50px 20px;
    font-size: 1.5rem;

    button {
      border: none;
      cursor: pointer;
      background-color: transparent;
      height: 30px;
      width: 30px;
      transition: transform .2s ease-in-out;

      &:not(:last-child) {
        margin-right: 10px;
      }

      &.current {
        color: $orange;
        text-decoration: underline;
      }

      &.disable {
        color: $grey;
        cursor: inherit;
      }

      &:hover {
        transform: scale(1.2);
      }
    }
  }

  #products-list {
    display: flex;
    flex-wrap: wrap;

    li {
      display: flex;
      width: calc((100% + 3px) / 4);
      background-color: #FFFFFF;
      border: 1px solid $grey;
      margin-left: -1px;
      margin-top: -1px;
      transition: transform .2s ease-in-out;

      &:nth-child(4n+1) {
        margin-left: 0;
        transform-origin: left center;
      }

      &:nth-child(4n+4) {
        transform-origin: right center;
      }

      &:hover {
        transform: scale(1.040);
      }

      a {
        padding: 20px;
        display: flex;
        width: 100%;

        figure {
          display: flex;
          flex-direction: column;
          align-items: center;
          width: 100%;

          img {
            height: 130px;
            width: auto;
            max-width: 100%;
          }

          figcaption {
            margin-top: 20px;
            flex: 1;
            width: 100%;
            display: flex;
            flex-direction: column;

            .product-name {
              font-size: 1.6rem;
              margin-bottom: 20px;
            }

            .product-price:not(:last-child) {
              margin-bottom: 20px;
              flex: 1;
            }

            .product-offer {
              font-size: 1.4rem;
              align-self: flex-end;

              .price {
                font-size: 1.6rem;
              }
            }
          }
        }
      }
    }
  }

  .no-product {
    display: flex;
    justify-content: center
  }

  @media screen and (min-width: 501px) and (max-width: 900px) {
    #products-list li {
      width: calc((100% + 2px) / 3);

      &:nth-child(4n+1) {
        margin-left: -1px;
        transform-origin: initial;
      }

      &:nth-child(4n+4) {
        transform-origin: initial;
      }

      &:nth-child(3n+1) {
        margin-left: 0;
        transform-origin: left center;
      }

      &:nth-child(3n+3) {
        transform-origin: right center;
      }
    }
  }

  @media screen and (min-width: 301px) and (max-width: 500px) {
    #products-list li {
      width: calc((100% + 1px) / 2);

      &:nth-child(3n+1) {
        margin-left: -1px;
        transform-origin: initial;
      }

      &:nth-child(3n+3) {
        transform-origin: initial;
      }

      &:nth-child(2n+1) {
        margin-left: 0;
        transform-origin: left center;
      }

      &:nth-child(2n+2) {
        transform-origin: right center;
      }
    }
  }

  @media screen and (max-width: 300px) {
    #products-list li {
      width: 100%;

      &:nth-child(2n+1) {
        margin-left: -1px;
        transform-origin: initial;
      }

      &:nth-child(2n+2) {
        transform-origin: initial;
      }

      &:nth-child(1n+1) {
        margin-left: 0;
      }

      &:hover {
        transform: initial;
      }
    }
  }
</style>
