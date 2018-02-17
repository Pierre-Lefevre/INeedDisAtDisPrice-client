<template>
  <div id="product-wrapper" class="bg-cover">
    <div class="darker">
      <div v-if="product">
        <div id="product">
          <div id="product-img">
            <img :src="$store.state.serverUrl + '/api/image/' + product.store + '/' + product.image_name + '.jpg'" :alt="product.name"/>
          </div>
          <div id="product-info">
            <div class="product-name">
              <h1>{{product.name}}</h1>
            </div>
            <div class="product-price price">
              {{product.price}} {{product.currency | currencySymbol}}
            </div>
            <div class="product-avis">
              <template v-if="!product.nb_avis">
                <span>Aucun avis</span>
              </template>
              <template v-else>
                <span>{{product.rate}}/{{product.max_rate}} ({{product.nb_avis}} avis)</span>
              </template>
            </div>
          </div>
          <div id="product-price-chart">
            <line-chart :data="lineChart" :width="350" :height="350"></line-chart>
            <button id="show-modal" class="my-button" @click="showModal = true" v-if="isLoggedIn">M'alerter !</button>
          </div>
        </div>
        <div id="offer-wrapper">
          <div class="offer">
            <h2>Disponible sur</h2>
            <ul>
              <li>
                <div class="store-logo">
                  <img :src="'/static/img/stores/logos/' + product.store + '.png'" :alt="product.store">
                </div>
                <div class="store-product-name">
                  <p>{{product.name}}</p>
                </div>
                <div class="store-product-price price">
                  {{product.price}} {{product.currency | currencySymbol}}
                </div>
                <div class="store-product-avis">
                  <template v-if="!product.nb_avis">
                    <span>Aucun avis</span>
                  </template>
                  <template v-else>
                    <span>{{product.rate}}/{{product.max_rate}} ({{product.nb_avis}} avis)</span>
                  </template>
                </div>
                <div class="store-product-link"><a :href="product.url" target="_blank">Voir l'offre</a></div>
              </li>
            </ul>
          </div>
          <div class="offer" v-if="similarProducts.length > 0">
            <h2>Variantes</h2>
            <ul>
              <li :key="i" v-for="(similarProduct, i) in similarProducts">
                <div class="store-logo">
                  <img :src="'/static/img/stores/logos/' + similarProduct.store + '.png'" :alt="similarProduct.store">
                </div>
                <div class="store-product-name">
                  <router-link :to="{name: 'Product', params: {id: similarProduct._id}}" tag="a">
                    <p>{{similarProduct.name}}</p>
                  </router-link>
                </div>
                <div class="store-product-price price">
                  {{similarProduct.price}} {{similarProduct.currency | currencySymbol}}
                </div>
                <div class="store-product-avis">
                  <template v-if="!similarProduct.nb_avis">
                    <span>Aucun avis</span>
                  </template>
                  <template v-else>
                    <span>{{similarProduct.rate}}/{{similarProduct.max_rate}} ({{similarProduct.nb_avis}} avis)</span>
                  </template>
                </div>
                <div class="store-product-link"><a :href="similarProduct.url" target="_blank">Voir l'offre</a></div>
              </li>
            </ul>
          </div>
        </div>
        <transition name="modal">
          <div class="modal-mask" v-if="showModal">
            <div class="modal-wrapper" @click.self="showModal = false">
              <div class="modal-container">
                <div class="modal-header">
                  Demander à être alerter par email
                </div>
                <div class="modal-body">
                  Je souhaite être alerté par email lorsque le prix de ce produit sera de : <input type="number" v-model="alertPrice">
                </div>
                <div class="modal-footer">
                  <button class="modal-default-button my-button" @click="createAlert">Valider</button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
      <div v-else>
        <loader></loader>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
import Loader from '@/components/Loader'
import LineChart from '@/components/LineChart'
import { eventBus } from '@/services/eventBus'
import filters from '@/services/filters'

export default {
  name: 'product',
  components: {
    Loader,
    LineChart
  },
  data () {
    return {
      productId: this.$route.params.id,
      product: null,
      similarProducts: [],
      lineChart: {
        labels: [],
        data: [],
        currency: null
      },
      showModal: false,
      alertPrice: null
    }
  },
  mounted () {
    this.fetchProducts()
  },
  methods: {
    ...mapGetters(['getUser']),
    fetchProducts () {
      axios.get(this.$store.state.serverUrl + '/api/product?id=' + this.productId).then(response => {
        this.product = response.data.product
        this.similarProducts = response.data.similarProducts
      }, error => {
        console.log(error)
      })
    },
    createAlert () {
      this.showModal = false

      let data = JSON.stringify({
        id_user: this.getUser()._id,
        id_product: this.product._id,
        price: this.alertPrice
      })

      axios.post(this.$store.state.serverUrl + '/alert', data, {headers: {'Content-Type': 'application/json'}}).then(() => {
        eventBus.$emit('alert', {type: 'success', message: 'Votre demande a bien était prise en compte.'})
      }, err => {
        eventBus.$emit('alert', {type: 'error', message: 'Une erreur est survenue lors de l\'ajout de l\'alerte (' + err.message + ').'})
      })
    }
  },
  watch: {
    product (product) {
      product.price_history.forEach(price => {
        this.lineChart.labels.push(filters.dateEnToFr(price.date))
        this.lineChart.data.push(price.price)
      })
      this.lineChart.currency = filters.currencySymbol(product.price_history[0].currency)
      if (this.lineChart.labels.length === 1) {
        this.lineChart.labels.push(this.lineChart.labels[0])
        this.lineChart.data.push(this.lineChart.data[0])
      }
      this.alertPrice = product.price
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  }
}
</script>

<style scoped lang="scss">
  #product-wrapper .darker > div {
    width: 100%;
  }

  #product {
    display: flex;
    padding: 20px;
    background-color: #FFFFFF;

    & > div {
      width: calc(100% / 3);
    }

    #product-img {
      display: flex;
      align-items: center;
      margin-right: 20px;

      img {
        width: 100%;
      }
    }

    #product-info {
      display: flex;
      justify-content: center;
      flex-direction: column;
      margin-right: 20px;

      & > *:not(:last-child) {
        margin-bottom: 20px;
      }

      .product-name h1 {
        font-size: 2rem;
        font-weight: bold;
      }

      .product-avis {
        font-size: 1.6rem;
      }
    }

    #product-price-chart {

      .my-button {
        display: flex;
        margin: auto;
      }
    }
  }

  #offer-wrapper {
    padding: 20px;
  }

  .offer {
    color: #FFFFFF;

    &:not(:last-of-type) {
      margin-bottom: 20px;
    }

    h2 {
      font-size: 2rem;
      margin-bottom: 20px;
    }

    li {
      display: flex;
      font-size: 1.4rem;
      border-radius: 2px;

      &:not(:last-of-type) {
        margin-bottom: 5px;
      }

      & > div {
        width: calc((100% - 25px) / 5);
        padding: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: $black-opacity;
      }

      .store-logo img {
        height: 30px;
        width: auto;
      }

      .store-product-name a {
        text-decoration: underline;
      }

      .store-product-link {
        display: flex;
        align-items: stretch;
        padding: 0;

        a {
          flex: 1;
          display: flex;
          justify-content: center;
          align-items: center;
          text-align: center;
          background-color: $orange;
          padding: 10px;
          color: #FFFFFF;
          position: relative;

          &:after {
            content: '';
            width: 25px;
            background-color: $orange;
            clip-path: polygon(100% 50%, 0 0, 0 100%);
            position: absolute;
            top: 0;
            bottom: 0;
            right: -25px;
          }
        }
      }
    }
  }

  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: $darker;
    display: table;
    transition: opacity .3s ease;

    .modal-wrapper {
      display: table-cell;
      vertical-align: middle;
    }
  }

  .modal-container {
    width: 80%;
    max-width: 400px;
    margin: 0 auto;
    background-color: #FFFFFF;
    border-radius: 2px;
    box-shadow: 0 2px 8px $darker;
    transition: all .3s ease-in-out;
    font-size: 1.5rem;

    .modal-header {
      color: #FFFFFF;
      margin-top: 0;
      border-radius: 2px 2px 0 0;
      background-color: $black;
      padding: 20px;
    }

    .modal-body {
      padding: 20px;

      input[type='number'] {
        border: 1px solid $black;
        border-radius: 2px;
        padding: 5px;
        width: 90px;
        background-color: $black;
        color: #FFFFFF;
      }
    }

    .modal-footer {
      padding: 0 20px 20px 20px;

      button {
        color: #FFFFFF;

        &:hover {
          transform: scale(1.1);
        }
      }
    }
  }

  /*
   * The following styles are auto-applied to elements with
   * transition="modal" when their visibility is toggled
   * by Vue.js.
   *
   * You can easily play with the modal transition by editing
   * these styles.
   */

  .modal-enter-active {
    opacity: 0;
  }

  .modal-leave-active {
    opacity: 0;
  }

  .modal-enter-active .modal-container,
  .modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
  }
</style>
