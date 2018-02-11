<template>
  <div id="profile-wrapper" class="bg-cover">
    <div class="darker center-content">
      <div id="profile" class="black-bloc">
        <h1>{{user.firstname}} {{user.lastname}}</h1>
        <p>Pseudo : {{user.pseudo}}</p>
        <p>Email : {{user.email}}</p>
      </div>
      <div id="my-alerts" class="black-bloc" v-if="alerts.length > 0">
        <h2>Mes alertes</h2>
        <ul>
          <li class="alert" :key="i" v-for="(alert, i) in alerts">
            <router-link :to="{name: 'Product', params: {id: alert.product._id}}" tag="a">
              <div class="alert-product-name">{{alert.product.name}}</div>
              <div class="alert-product-price">Prix actuel : {{alert.product.price}} {{alert.product.currency | currencySymbol}}</div>
              <div class="alert-price">Prix souhaité : {{alert.price}} {{alert.product.currency | currencySymbol}}</div>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapGetters } from 'vuex'

export default {
  name: 'profile',
  data () {
    return {
      user: this.getUser(),
      alerts: null
    }
  },
  created () {
    this.fetchAlerts()
  },
  methods: {
    fetchAlerts () {
      this.alerts = null
      axios.get(this.$store.state.serverUrl + '/api/alerts/' + this.user._id).then(response => {
        this.alerts = response.data
      }, error => {
        console.log(error)
      })
    },
    ...mapGetters(['getUser'])
  }
}
</script>

<style scoped lang="scss">
  #profile-wrapper .darker {

    #profile, #my-alerts {
      width: 80%;
      font-size: 1.5rem;

      h1 {
        margin-bottom: 20px;
        font-size: 2.5rem;
        align-self: center;
      }

      h2 {
        margin-bottom: 20px;
        font-size: 2rem;
        align-self: center;
      }
    }

    #profile {
      max-width: 400px;
      margin: 50px;
    }

    #my-alerts {
      max-width: 800px;
      margin: 0 50px 50px 50px;

      .alert {

        &:not(:last-of-type) {
          border-bottom: 1px solid #FFFFFF;
        }

        a {
          display: flex;
          padding: 10px;

          .alert-product-name {
            width: 50%;
            padding-right: 20px;
          }

          .alert-product-price {
            width: 25%;
            padding-right: 20px;
          }

          .alert-price {
            width: 25%;
          }
        }
      }
    }
  }
</style>
