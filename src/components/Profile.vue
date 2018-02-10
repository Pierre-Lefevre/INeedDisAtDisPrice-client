<template>
  <div>
    <pre>{{user}}</pre>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'profile',
  data () {
    return {
      user: this.getUser()
    }
  },
  methods: {
    ...mapGetters(['getUser'])
  }
}
</script>

<style scoped>

</style>
