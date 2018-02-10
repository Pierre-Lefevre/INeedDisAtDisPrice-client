<template>
  <div v-show="alerts.length" id="alert-wrapper">
    <transition-group name="fade">
      <div v-for="(alert, i) in alerts" v-if="alert.show" :key="i" class="alert" :class="alert.class">
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
          alert.class = 'bg-green'
          break
        case 'info':
          alert.class = 'bg-blue'
          break
        case 'error':
          alert.class = 'bg-red'
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

  .alert {
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  }

  .alert:not(:last-child) {
    margin-bottom: 20px;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
