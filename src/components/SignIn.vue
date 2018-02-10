<template>
  <div>
    <h1 class="color-green">Connexion</h1>
    <form @submit.prevent="login">
      <input type="text" placeholder="Pseudo" v-model="pseudo">
      <input type="password" placeholder="Mot de passe" v-model="password">
      <button type="submit" class="btn-primary bg-green hvr-grow">Se connecter</button>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { eventBus } from '@/services/eventBus'

export default {
  name: 'signIn',
  data () {
    return {
      pseudo: '',
      password: ''
    }
  },
  methods: {
    ...mapActions({processLogin: 'login'}),
    login () {
      // Promesse de connexion.
      this.processLogin({
        pseudo: this.pseudo,
        password: this.password
      }).then(() => {
        this.$router.push({name: 'Profile'})
      }, err => {
        eventBus.$emit('alert', {type: 'error', message: err.message})
      })
    }
  }
}
</script>

<style scoped>

</style>
