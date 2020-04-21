<template>
  <v-app class="app">
    <v-snackbar
      v-model='$store.getters.notificationIsActive'
      :timeout='0'
      :right='true'
      :top='true'
      :color="$store.getters.notificationColor">
      {{$store.getters.notificationMessage}}
      <v-btn dark flat>
        Close
      </v-btn>
    </v-snackbar>

    <navbar
      v-if="$store.getters.isLoggedIn && !$store.getters.isShopper"
      :drawer=drawer
      :updateDrawer="handleUpdateDrawer"
    />

    <v-toolbar
      v-if="$store.getters.isLoggedIn && $store.getters.isShopper"
      app
      fixed
      flat
      class="storefront-toolbar"
    >
      <!-- <popup-cart ref="popupCart"></popup-cart> -->
      <router-link
        d-flex
        to="/"
        tag="a"
        class="main-logo"

      >
        <img src="./assets/logo/logo.png" alt="Logo">
      </router-link>
      <v-spacer></v-spacer>
      <v-btn
        @click="$router.push('/cart')"
        @mouseover="isMounted && $refs.popupCart.enable()"
        @mouseleave="isMounted && $refs.popupCart.disable()"
        flat icon
      >
        <v-badge left>
          <span slot="badge">{{ itemsCount }}</span>
          <v-icon>shopping_cart</v-icon>
        </v-badge>
      </v-btn>
      <v-btn flat round @click="logout">Logout</v-btn>
    </v-toolbar>

    <v-toolbar
      v-else
      app
      ligth
      fixed
      clipped-left
      color='white'
    >
      <v-toolbar-side-icon
        v-if="$route.path.indexOf('/login') === -1"
        @click="drawer = !drawer"
        color="Green"
      ></v-toolbar-side-icon>
      <v-toolbar-title>
        {{ $store.state.title }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <router-link
        d-flex
        to="/"
        tag="a"
        class="main-logo"

      >
        <img src="./assets/logo/logo.png" alt="Logo">
      </router-link>
      <v-toolbar-items class="hidden-sm-and-down">
      </v-toolbar-items>
    </v-toolbar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
  import TheNavbar from './components/TheNavbar';
  // import PopupCart from './components/Orders/Storefront/PopupCart'

  export default {
    components: {
      navbar: TheNavbar,
      // PopupCart
    },

    data() {
      return {
        isMounted: false,
        drawer: true,
        itemsCount: 0,
        homeLinks: [
          {title: 'Home', url: '/'},
          {
            title: 'Reports', group: true, links: [
              {title: 'Order Details', url: '/#'}
            ]
          }
        ],
        catalogLinks: [
          {title: 'Products', url: '/products'},
          {title: 'Product types', url: '/product_types'},
          {title: 'Attributes', url: '/attributes'},
          {title: 'Campaigns', url: '/campaigns'}
        ],
        peopleManagementLinks: [
          {title: 'Distributors', url: '/distributors'},
          {title: 'User Accounts', url: '/accounts'}
        ],
        orderManagementLinks: [
          {title: 'Orders', url: '/orders'},
          {title: 'Storefront', url: '/storefront'},
          {title: 'Cart', url: '/cart'}
        ]
      }
    },

    watch: {
      '$route'() {
        this.update()
      }
    },

    methods: {
      update() {
        // Update items count
        this.itemsCount = 0;
        this.$data.cartItems = JSON.parse(localStorage.getItem('cartProducts'));
        if (this.$data.cartItems != null) {
          Object.keys(this.$data.cartItems).forEach(k => {
            this.itemsCount += this.$data.cartItems[k]
          })
        }
        this.$store.state.title = ''
      },

      handleUpdateDrawer(v) {
        this.drawer = v;
      },

      async logout() {
        try {
          await this.$store.dispatch('logout');
          this.$router.push('/login');
        } catch (e) {
          console.error(e);
        }
      }
    }
  }
</script>

<style>
  .app {
    background-color: white !important;
  }

  .storefront-toolbar .v-toolbar__content {
    height: 80px !important;
  }

  .clip {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 250px;
  }


  .clip:hover {
    text-overflow: clip;
    white-space: normal;
    word-break: break-all;
  }

  .word-break-all {
    word-break: break-all;
  }

</style>
