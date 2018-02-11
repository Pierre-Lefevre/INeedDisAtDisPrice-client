<template>
  <div id="home-wrapper" class="bg-cover">
    <div class="darker center-content">
      <img src="/static/img/icons/logo.svg"/>
      <h1>I Need Dis At Dis Price</h1>
      <search mainClass="home"/>
      <h2>Comparez & soyez avertis</h2>
    </div>
  </div>
</template>

<script>
import Search from '@/components/Search'

export default {
  name: 'Home',
  components: {
    Search
  }
}
</script>

<style scoped lang="scss">
  #home-wrapper .darker {

    img {
      height: 250px;
      margin-bottom: 20px;
    }

    h1 {
      font-size: 6rem;
      margin-bottom: 20px;
      text-align: center;
    }

    h2 {
      font-size: 2rem;
      margin-top: 20px;
      text-align: center;
    }
  }
</style>
