<template>
    <v-container grid-list-lg v-if="campaign && rawProducts">
        <!-- Message -->
        <div class="message mt-3">
            <div class="headline mb-1">Shopper instructions:</div>
            <v-divider></v-divider>
            <div class="subheading mt-2" v-html="campaign.message"></div>
        </div>

        <!-- Controls -->
        <v-layout row wrap class="mt-4">
            <v-flex md8>
            </v-flex>
            <v-flex xs12 md4>
                <v-text-field
                    solo
                    v-model="search"
                    label="Search...">
                </v-text-field>
            </v-flex>
        </v-layout>

        <!-- Products -->
        <div class="mt-1">
            <v-layout row wrap align-content-space-around ref="infinite-list">
                <v-flex
                    xs12 md4
                    v-for="product in productsSubset"
                    :key="product.id">
                    <storefront-product-card
                        :product=product
                        @add-product="addProductHandler">
                    </storefront-product-card>
                </v-flex>
            </v-layout>
        </div>

        <!-- Pagination -->
<!--         <div v-if="totalPages > 1" class="text-xs-center mt-5 mb-5">
            <v-pagination
                v-model="page"
                :length="totalPages"
                @input="loadSubset"
            ></v-pagination>
        </div> -->

        <div class="text-xs-center mb-5 mt-4">
            <v-btn @click="$router.push('/cart')" depressed color="primary" class="goto-cart">go to cart</v-btn>
        </div>

    </v-container>
</template>


<script>

import axios from '@/axios'
import StorefrontProductCard from './StorefrontProductCard';

export default {
    name: 'Storefront',

    components: {
        'storefront-product-card': StorefrontProductCard
    },

    data () {
        return {
            campaign: null,
            rawProducts: null,
            productsSubset: [],
            cartProducts: {},
            page: 1,
            perPage: 20,
            search: '',
            bottom: false
        }
    },

    computed: {
        totalPages () {
            return Math.ceil(this.processedProducts.length / this.perPage)
        },
        processedProducts () {
            return this.rawProducts ? this.rawProducts.filter(p => p.name.toLowerCase().indexOf(this.search.toLowerCase()) !== -1) : []
        }
    },

    watch: {
        processedProducts () {
            this.loadSubset()
        },
        search () {
            this.page = 1
        },
        bottom(bottom) {
          if (bottom) {
            this.updateSubset()
          }
        }
    },

    created() {
        window.addEventListener('scroll', (e) => {
            e.preventDefault()
            e.stopPropagation()
            this.bottom = this.bottomVisible()
      })
        //this.updateSubset()
    },

    mounted () {
        if (localStorage.getItem('cartProducts')) {
          try {
            this.cartProducts = JSON.parse(localStorage.getItem('cartProducts'));
          } catch(e) {
            localStorage.removeItem('cartProducts');
          }
        }

        if (!this.isShopper())
            this.$router.push('/admin')
        else
            this.load()
    },

    updated () {
/*        this.$vuetify.goTo(0, {
            duration: 1000,
            easing: 'easeInOutCubic'
        })*/
    },

    methods: {
        bottomVisible() {
          const scrollY = window.scrollY
          const visible = document.documentElement.clientHeight
          const pageHeight = document.documentElement.scrollHeight
          const bottomOfPage = visible + scrollY >= pageHeight
          return bottomOfPage || pageHeight < visible
        },

        isShopper () {
            return this.$store.state.account.role.name == 'Shopper'
        },

        addProductHandler (cartProduct) {
            this.cartProducts = Object.assign(this.cartProducts, cartProduct)
            const parsed = JSON.stringify(this.cartProducts);
            localStorage.setItem('cartProducts', parsed);
            this.$parent.$parent.$parent.update()
            this.$parent.$parent.$parent.$refs.popupCart.update()
        },

        load () {
            // Campaign
            let params = {headers: {
                'Authorization': this.$store.state.token}}
            let url = `/campaigns/${this.$store.state.account.campaign_id}`
            axios.get(url, params).then(resp => {
                this.campaign = resp.data
            }).catch(err => {
                this.$store.dispatch('raiseError', err)
            })

            // Products
            let fields = '*,product_variants{*}'
            params = {headers: {
                'Authorization': this.$store.state.token,
                'X-Fields': fields}}
            url = '/storefront/products'
            axios.get(url, params).then(resp => {
                this.rawProducts = resp.data
                this.loadSubset()
            }).catch(err => {
                this.$store.dispatch('raiseError', err)
            })
        },

        loadSubset( ) {
            this.page = 1;
            let from = (this.page-1) * this.perPage
            let to = this.page * this.perPage
            this.productsSubset = this.processedProducts.slice(from, to)
        },
        updateSubset() {
            if (this.page != this.totalPages){
                this.page++
                let from = (this.page-1) * this.perPage
                let to = this.page * this.perPage
                this.productsSubset = this.processedProducts.slice(0, to)
            }
        }

    }
}
</script>

<style scoped>
.message {
    background-color: rgb(213, 237, 243);
    padding: 15px;
}
.goto-cart {
    height: 70px;
    font-size: 2em;
}
</style>
