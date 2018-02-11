<template>
  <div id="sign-in-wrapper" class="bg-cover">
    <div class="darker center-content">
      <div class="form-wrapper black-bloc">
        <h1>Connexion</h1>
        <form @submit.prevent="login">
          <input class="my-input" type="text" placeholder="Pseudo" v-model="pseudo">
          <input class="my-input" type="password" placeholder="Mot de passe" v-model="password">
          <button type="submit" class="my-button">Valider</button>
        </form>
      </div>
    </div>
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

<style scoped lang="scss">
  #sign-in-wrapper .darker .form-wrapper {
    align-items: center;
    width: 80%;
    max-width: 400px;

    h1 {
      margin-bottom: 20px;
      font-size: 2.5rem;
    }

    & > form {
      display: flex;
      flex-direction: column;
      width: 100%;

      .my-input:not(:last-of-type) {
        margin-bottom: 10px;
      }

      button {
        margin-top: 20px;
        align-self: flex-start;

        &:hover {
          transform: scale(1.1);
        }
      }
    }
  }
</style>
