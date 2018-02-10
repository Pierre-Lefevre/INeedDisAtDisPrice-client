import Vue from 'vue'
import Router from 'vue-router'
import guards from '@/services/guards'
// import Home from '@/components/Home'
import Products from '@/components/Products'
import Product from '@/components/Product'
import SignIn from '@/components/SignIn'
import SignUp from '@/components/SignUp'
import Profile from '@/components/Profile'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Products,
      meta: {
        title: 'Accueil'
      }
    },
    {
      path: '/products',
      name: 'Products',
      component: Products,
      meta: {
        title: 'Liste des produits'
      }
    },
    {
      path: '/product/:id',
      name: 'Product',
      component: Product,
      meta: {
        title: 'Détail d\'un produit'
      }
    },
    {
      path: '/sign-in',
      name: 'SignIn',
      component: SignIn,
      beforeEnter: guards.guest,
      meta: {
        title: 'Connexion'
      }
    },
    {
      path: '/sign-up',
      name: 'SignUp',
      component: SignUp,
      beforeEnter: guards.guest,
      meta: {
        title: 'Inscription'
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      beforeEnter: guards.auth,
      meta: {
        title: 'Profil'
      }
    }
  ]
})

// Permet de modifier la balise 'title' de chaque page.
router.beforeEach((to, from, next) => {
  const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title)
  if (nearestWithTitle) {
    document.title = nearestWithTitle.meta.title + ' - I Need Dis At Dis Price'
  }
  next()
})

export default router
