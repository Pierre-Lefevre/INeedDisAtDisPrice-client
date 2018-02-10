<template>
  <div>
    <h1 class="color-blue">Inscription</h1>
    <form @submit.prevent="signUp">
      <input type="text" placeholder="Prénom" v-model="firstname">
      <input type="text" placeholder="Nom" v-model="lastname">
      <input type="text" placeholder="Pseudo" v-model="pseudo">
      <input type="email" placeholder="Email" v-model="email">
      <input type="password" placeholder="Mot de passe" v-model="password">
      <button type="submit" class="btn-primary bg-blue hvr-grow">S'inscrire</button>
    </form>
  </div>
</template>

<script>
import { eventBus } from '@/services/eventBus'
import axios from 'axios'
import crypto from 'crypto-js'

export default {
  name: 'signUp',
  data () {
    return {
      firstname: '',
      lastname: '',
      pseudo: '',
      email: '',
      password: ''
    }
  },
  methods: {
    signUp () {
      // Vérifie que tous les champs sont renseignés.
      if (this.firstname === '' || this.lastname === '' || this.pseudo === '' || this.email === '' || this.password === '') {
        eventBus.$emit('alert', {type: 'error', message: 'Vous devez remplir tous les champs.'})
        return
      }

      let data = JSON.stringify({
        firstname: this.firstname,
        lastname: this.lastname,
        pseudo: this.pseudo,
        email: this.email,
        password: crypto.SHA256(this.password).toString(crypto.enc.Hex)
      })

      axios.post(this.$store.state.serverUrl + '/sign-up', data, {headers: {'Content-Type': 'application/json'}}).then(() => {
        eventBus.$emit('alert', {type: 'success', message: 'Inscription effectuée avec succès.'})
        this.$router.push({name: 'SignIn'})
      }, err => {
        eventBus.$emit('alert', {type: 'error', message: 'Une erreur est survenue pendant l\'inscription (' + err.message + ').'})
      })
    }
  }
}
</script>

<style scoped>

</style>
