<template>
  <div id="app">
    <header>
      <nav id="navbar">
        <div id="brand">
          <router-link :to="{name: 'Home'}" tag="a">I Need Dis At Dis Price</router-link>
        </div>
        <div id="menu-container">
          <ul class="menu">
            <li>
              <router-link :to="{name: 'Products'}" tag="a">Produits</router-link>
            </li>
          </ul>
          <search/>
          <ul class="menu authenticated-navigation" v-if="isLoggedIn">
            <li>
              <router-link :to="{name: 'Profile'}" tag="a">Profil</router-link>
            </li>
            <li>
              <a @click="logout">Déconnexion</a>
            </li>
          </ul>
          <ul class="menu not-authenticated-navigation" v-if="!isLoggedIn">
            <li>
              <router-link :to="{name: 'SignIn'}" tag="a">Connexion</router-link>
            </li>
            <li>
              <router-link :to="{name: 'SignUp'}" tag="a">Inscription</router-link>
            </li>
          </ul>
        </div>
      </nav>
    </header>
    <main>
      <router-view/>
    </main>
    <alert/>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import Alert from '@/components/Alert'
import Search from '@/components/Search'

export default {
  name: 'App',
  components: {
    Alert,
    Search
  },
  methods: {
    ...mapActions({processLogout: 'logout'}),
    logout () {
      this.processLogout()
      this.$router.push({name: 'Home'})
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn'])
  }
}
</script>

<style lang="scss">
  #app {
    /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
    /*-webkit-font-smoothing: antialiased;*/
    /*-moz-osx-font-smoothing: grayscale;*/
    /*text-align: center;*/
    /*color: #2c3e50;*/
    /*margin-top: 60px;*/
  }

  * {
    box-sizing: border-box;
  }

  html {
    font-family: sans-serif;
    font-size: 10px;
    color: #222222;
  }

  body, h1, h2, h3, ul {
    margin: 0;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  a:hover, a:visited, a:link, a:active {
    text-decoration: none;
    color: inherit;
    outline: none;
  }

  main {
    margin: 20px;
  }

  .price {
    color: #FF6600;
    font-weight: bold;
    font-size: 2rem;
    line-height: 2rem;
  }

  /* Menu */

  #navbar {
    display: flex;
    background-color: #222222;
    height: 60px;
    color: #FFFFFF;

    #brand {
      display: flex;

      a {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 30px;
        font-size: 2rem;
      }
    }

    #menu-container {
      flex: 1;
      display: flex;
      justify-content: space-between;

      .menu {
        display: flex;

        li {
          display: flex;

          a {
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 10px 30px;
            font-size: 1.6rem;
          }
        }
      }
    }
  }
</style>
