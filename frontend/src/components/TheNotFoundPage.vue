<template>
  <v-container fluid fill-height>
    <v-layout align-center>
      <v-flex md1></v-flex>
      <v-flex xs12 md4>
        <div>
          <div class="display-1 my-3 text-center">404</div>
          <div class="display-2 my-3 text-center">Page not found</div>
          <div class="">return to <router-link to="/login" class="text--primary">login</router-link> page</div>
        </div>
      </v-flex>
      <v-flex md7 hidden-sm-and-down class="background">
        <img src="@/assets/woman_jumping.png" alt="Woman Jumping"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    data() {},
    computed: {},
    methods: {},
  }
</script>

<style scoped>
  .background {
    text-align: right;
    padding-right: 5vw;
  }

  .background img {
    height: 80vh;
  }

  .container {
    background-color: white;
  }
</style>
