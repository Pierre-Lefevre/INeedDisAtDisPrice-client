import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import crypto from 'crypto-js'
import config from '@/config/config'
import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'

const LOGIN = 'LOGIN'
const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
const LOGOUT = 'LOGOUT'
const PRODUCTS_SEARCH = 'PRODUCTS_SEARCH'

Vue.use(Vuex)

// Store de l'application.
export default new Vuex.Store({
  state: {
    isLoggedIn: !!localStorage.getItem('token'),
    user: null,
    products_search: '',
    serverUrl: config.serverUrl
  },
  mutations: {
    [LOGIN] (state) {
      state.pending = true
    },
    [LOGIN_SUCCESS] (state, user) {
      state.isLoggedIn = true
      state.user = user
      state.pending = false
    },
    [LOGOUT] (state) {
      state.isLoggedIn = false
      state.user = null
    },
    [PRODUCTS_SEARCH] (state, search) {
      state.products_search = search
    }
  },
  actions: {
    login ({commit, state}, input) {
      commit(LOGIN)

      // Renvoie une promesse permettant de savoir si la tentative de connexion a réussi ou non.
      return new Promise((resolve, reject) => {
        let data = JSON.stringify({
          pseudo: input.pseudo,
          password: crypto.SHA256(input.password).toString(crypto.enc.Hex)
        })

        axios.post(state.serverUrl + '/sign-in', data, {headers: {'Content-Type': 'application/json'}}).then(response => {
          if (response.data.login) {
            let user = response.data.user
            localStorage.setItem('token', user._id)
            commit(LOGIN_SUCCESS, user)
            resolve()
          } else {
            reject(new Error('Pseudo ou mot de passe incorrect.'))
          }
        }, error => {
          console.log(error)
        })
      })
    },
    logout ({commit}) {
      localStorage.removeItem('token')
      commit(LOGOUT)
    }
  },
  getters: {
    isLoggedIn: state => {
      return state.isLoggedIn
    },
    getUser: state => {
      return state.user
    },
    getProductsSearch: state => {
      return state.products_search
    }
  },
  plugins: [
    createPersistedState({
      storage: {
        getItem: key => Cookies.get(key),
        setItem: (key, value) => Cookies.set(key, value, {expires: 3, secure: false}),
        removeItem: key => Cookies.remove(key)
      }
    })
  ]
})
