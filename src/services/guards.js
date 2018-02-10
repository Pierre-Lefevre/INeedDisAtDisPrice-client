import store from '@/store/store'

// Intercepteurs utilisés par l'application.
export default {

  // L'utilisateur ne doit pas être connecté, sinon redirection vers la page d'accueil.
  guest (to, from, next) {
    next(!store.getters.isLoggedIn ? true : {name: 'Home'})
  },

  // L'utilisateur doit être connecté, sinon redirection vers la page d'accueil.
  auth (to, from, next) {
    next(store.getters.isLoggedIn ? true : {name: 'Home'})
  }
}
