<template>
  <div class="loader" :class="mainClass">
    <div></div>
  </div>
</template>

<script>
export default {
  name: 'loader',
  props: ['mainClass']
}
</script>

<style scoped lang="scss">
  .loader {
    display: flex;
    z-index: 700;
    width: 100vw;
    justify-content: center;
    align-items: center;
    transition: opacity 2s linear;

    &.products {
      height: 400px;
    }

    &:not(.products) {
      position: fixed;
      height: calc(100vh - 60px);
    }

    > div {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      border: 3px solid transparent;
      border-top-color: $black;
      border-bottom-color: $black;
      animation: spin 3s linear infinite;

      &:before {
        content: '';
        position: absolute;
        top: 15px;
        left: 15px;
        right: 15px;
        bottom: 15px;
        border-radius: 50%;
        border: 3px solid transparent;
        border-top-color: $black;
        border-bottom-color: $black;
        animation: spin 4s linear infinite;
      }

      &:after {
        content: '';
        position: absolute;
        top: 32px;
        left: 32px;
        right: 32px;
        bottom: 32px;
        border-radius: 50%;
        border: 3px solid transparent;
        border-top-color: $black;
        border-bottom-color: $black;
        animation: spin 2s linear infinite;
      }
    }
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(360deg);
    }
  }
</style>
