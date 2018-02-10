<template>
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
        <div v-if="isLoggedIn">
          <button id="show-modal" @click="showModal = true">M'alerter</button>
        </div>
      </div>
    </div>
    <div class="stores">
      <h2>Disponible sur</h2>
      <ul>
        <li>
          <div class="store-logo">
            <img :src="'/static/img/stores/logos/' + product.store + '.png'" :alt="product.store">
          </div>
          <div class="store-product-avis">
            <template v-if="!product.nb_avis">
              <span>Aucun avis</span>
            </template>
            <template v-else>
              <span>{{product.rate}}/{{product.max_rate}} ({{product.nb_avis}} avis)</span>
            </template>
          </div>
          <div class="store-product-name"><h3>{{product.name}}</h3></div>
          <div class="store-product-price price">
            {{product.price}} {{product.currency | currencySymbol}}
          </div>
          <div class="store-product-link"><a :href="product.url" target="_blank">Voir l'offre</a></div>
        </li>
      </ul>
    </div>
    <div class="stores" v-if="similarProducts.length > 0">
      <h2>Variantes</h2>
      <ul>
        <li :key="i" v-for="(similarProduct, i) in similarProducts">
          <div class="store-logo">
            <img :src="'/static/img/stores/logos/' + similarProduct.store + '.png'" :alt="similarProduct.store">
          </div>
          <div class="store-product-avis">
            <template v-if="!similarProduct.nb_avis">
              <span>Aucun avis</span>
            </template>
            <template v-else>
              <span>{{similarProduct.rate}}/{{similarProduct.max_rate}} ({{similarProduct.nb_avis}} avis)</span>
            </template>
          </div>
          <div class="store-product-name"><h3>{{similarProduct.name}}</h3></div>
          <div class="store-product-price price">
            {{similarProduct.price}} {{similarProduct.currency | currencySymbol}}
          </div>
          <div class="store-product-link"><a :href="similarProduct.url" target="_blank">Voir l'offre</a></div>
        </li>
      </ul>
    </div>

    <transition name="modal">
      <div class="modal-mask" v-if="showModal">
        <div class="modal-wrapper" @click.self="showModal = false">
          <div class="modal-container">
            <div class="modal-header">
              <slot name="header">
                Demander à être alerter par email
              </slot>
            </div>

            <div class="modal-body">
              <slot name="body">
                Je souhaite être alerté par email lorsque le prix de ce produit sera de :
                <input type="number" v-model="alertPrice">
              </slot>
            </div>

            <div class="modal-footer">
              <slot name="footer">
                default footer
                <button class="modal-default-button" @click="createAlert">
                  Valider
                </button>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
  <div v-else>
    <loader></loader>
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
      axios.get(this.$store.state.serverUrl + '/api/product/' + this.productId).then(response => {
        this.product = response.data.product
        this.similarProducts = response.data.similarProducts
      }, error => {
        console.log(error)
      })
    },
    createAlert () {
      this.showModal = false

      console.log(this.alertPrice)

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
      console.log(product.price_history)
      product.price_history.forEach(price => {
        this.lineChart.labels.push(filters.dateEnToFr(price.date))
        this.lineChart.data.push(price.price)
      })
      this.lineChart.currency = filters.currencySymbol(product.price_history[0].currency)

      if (this.lineChart.labels.length === 1) {
        this.lineChart.labels.push(this.lineChart.labels[0])
        this.lineChart.data.push(this.lineChart.data[0])
      }

      // this.lineChart.labels = ['10/12/2017', '15/12/2017', '27/12/2017', '10/01/2018', '14/01/2018', '25/01/2018', '27/01/2018']
      // this.lineChart.data = [4000, 3000, 2000, 2780, 1890, 2390, product.price]
      this.alertPrice = product.price
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  }
}
</script>

<style scoped lang="scss">
  #product {
    display: flex;
    margin-bottom: 20px;

    & > div {
      width: calc(100% / 3);
    }

    #product-img img {
      width: 100%;
    }

    #product-info {

      .product-name h1 {
        font-size: 2rem;
        font-weight: bold;
      }

      .product-price {
        margin-top: 10px;
      }

      .product-avis {
        font-size: 1.6rem;
      }
    }
  }

  .stores {
    padding-bottom: 10px;

    h2 {
      font-size: 1.8rem;
      margin-bottom: 20px;
    }

    li {
      display: flex;
      border: 1px solid #E7E7E7;
      background-color: #F8F8F8;
      margin-bottom: 10px;
      font-size: 1.4rem;

      & > div {
        width: calc(100% / 5);
        padding: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
      }

      .store-product-link {
        display: flex;

        a {
          flex: 1;
          text-align: center;
          background-color: #FF6600;
          border-radius: 2px;
          padding: 10px;
          color: #FFFFFF;
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
    background-color: rgba(0, 0, 0, .5);
    display: table;
    transition: opacity .3s ease;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .modal-container {
    width: 300px;
    margin: 0px auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease-in-out;
    font-family: Helvetica, Arial, sans-serif;
  }

  .modal-header h3 {
    margin-top: 0;
    color: #42b983;
  }

  .modal-body {
    margin: 20px 0;
  }

  .modal-default-button {
    float: right;
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
