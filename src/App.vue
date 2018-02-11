<template>
  <div id="app-wrapper">
    <header>
      <nav id="navbar">
        <div id="brand">
          <router-link :to="{name: 'Home'}" tag="a">
            <img src="/static/img/icons/logo.svg"/>
            <p>I Need Dis At Dis Price</p>
          </router-link>
        </div>
        <div id="menu-container">
          <search mainClass="nav"/>
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
      <router-view :key="$route.fullPath"/>
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
  #navbar {
    display: flex;
    background-color: $black;
    height: 60px;
    color: #FFFFFF;

    #brand {
      display: flex;

      a {
        width: 340px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 30px;
        font-size: 2rem;

        img {
          height: 100%;
          width: auto;
          margin-right: 30px;
        }
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
