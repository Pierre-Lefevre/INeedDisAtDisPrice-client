<template>
  <div v-show="alerts.length" id="alert-wrapper">
    <transition-group name="fade">
      <div v-for="(alert, i) in alerts" v-if="alert.show" :key="i" class="notification" :class="alert.class">
        <p>{{ alert.message }}</p>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { eventBus } from '@/services/eventBus'

export default {
  name: 'alert',
  data () {
    return {
      alerts: []
    }
  },
  created () {
    // Si l'évènement "alert" est reçu...
    eventBus.$on('alert', alert => {
      alert.show = true

      switch (alert.type) {
        case 'success':
          alert.class = 'notification-success'
          break
        case 'info':
          alert.class = 'notification-info'
          break
        case 'error':
          alert.class = 'notification-error'
          break
      }

      // On ajoute l'alerte à les listes des alertes.
      this.alerts.push(alert)

      // Affichage de l'alerte pendant 5 secondes.
      setTimeout(() => {
        alert.show = false
      }, 5000)

      // Suppression de l'alerte au bout de 6 secondes (1 seconde de transition).
      setTimeout(() => {
        this.alerts.splice(this.alerts.indexOf(alert), 1)
      }, 6000)
    })
  }
}
</script>

<style scoped>
  #alert-wrapper {
    position: fixed;
    bottom: 0;
    width: 100%;
    opacity: 1;
    padding: 20px;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
