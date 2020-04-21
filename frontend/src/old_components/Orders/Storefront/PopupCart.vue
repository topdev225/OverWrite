<template>
  <v-card
    v-show="showing"
    class="popup-cart"
    @mouseover="focus = true"
    @mouseleave="disable(false)"
  >
    <v-card-title class="headline">Cart</v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-data-table
          v-if="products.length"
          :headers="headers"
          :items="products"
          class="elevation-1"
      >
          <template slot="items" slot-scope="props">
              <td>
                  <v-img
                      height="45"
                      contain
                  :src="getImg(props.item)">
                  </v-img>
              </td>
              <td>{{ props.item.product.name }}</td>
              <td>${{ props.item.price.toFixed(2) }}</td>
              <td class="text-xs-center">
                  {{ props.item.quantity }}
              </td>
              <td>${{ props.item.total.toFixed(2) }}</td>
          </template>
      </v-data-table>
      <div class="subheading" v-else>
        There are no items in your shopping cart
      </div>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions v-if="products.length">
      <v-btn @click="$router.push('/cart')">Go to cart</v-btn>
      <v-spacer></v-spacer>
      <div class="headline mr-4">Total: ${{ total.toFixed(2) }}</div>
    </v-card-actions>
  </v-card>
</template>


<script>

import axios from '@/axios'

export default {
  name: 'PopupCart',

  data () {
    return {
      showing: false,
      focus: false,
      cart: {},
      headers: [
          {text: '', align: 'center'},
          {text: 'Name', value: 'product.name'},
          {text: 'Price', value: 'price'},
          {text: 'Quantity', value: 'quantity', align: 'center'},
          {text: 'Total', value: 'total'}
      ],
      products: [],
    }
  },

  mounted () {
    this.update()
  },

  computed: {
    total () {
        let sum = 0
        this.products.forEach(p => {
            sum += p.total
        })
        return sum
    },
  },

  methods: {
    update () {
      this.cart = JSON.parse(localStorage.getItem('cartProducts'))
      this._loadProducts()
    },
    _loadProducts () {
      this.products = []
      if (!_.isEmpty(this.cart)) {
        let params = {headers: {
            Authorization: this.$store.state.token,
            'X-Fields': '*,product{name,resources}'}}
        try {
          Object.keys(this.cart).forEach(pvid => {
            axios.get(`/products/variants/${pvid}`, params).then(resp => {
                let pv = resp.data
                pv.quantity = this.cart[pvid]
                pv.total = pv.price * this.cart[pvid]
                this.products.push(pv)
            })
        })
        }catch (e) {
          console.log(e)
        }
      }
    },
    getImg (productVariant) {
      if (productVariant.resources[0]) {
        return `${process.env.API_BASE_URL}`+
                `/static`+
                `/resources`+
                `/${productVariant.resources[0].uuid}`+
                `.${productVariant.resources[0].type}`
      }
      if (productVariant.product.resources[0]) {
        return `${process.env.API_BASE_URL}`+
                `/static`+
                `/resources`+
                `/${productVariant.product.resources[0].uuid}`+
                `.${productVariant.product.resources[0].type}`
      }
      return `${process.env.API_BASE_URL}/static/default-product.svg`
    },

    enable () {
      this.showing = true
      this.focus = true
    },
    disable (status) {
      if (status !== undefined)
        this.focus = status
      setTimeout(function () {
        if (this.focus == false)
          this.showing = false
      }.bind(this), 100)
    }
  }
}
</script>

<style>
.popup-cart {
  position: fixed;
  top: 57px;
  right: 120px;
}
</style>
