<template>
    <v-container grid-list-xs>
        <v-layout row wrap justify-center>
            <v-flex xs10 mt-5 mb-5>
                <v-card flat color="rgb(213, 237, 243)">
                    <v-card-title primary-title>
                    <div>
                        <h3 class="headline mb-2">Checkout</h3>
                    </div>
                    </v-card-title>

                    <v-divider></v-divider>

                    <v-card-text>
                        <!-- Predefined fields -->
                        <v-text-field
                            solo
                            v-if="checkoutFields.includes('First Name')"
                            label="First Name *"
                            v-model="firstName"
                        ></v-text-field>
                        <v-text-field
                            solo
                            v-if="checkoutFields.includes('Last Name')"
                            label="Last Name *"
                            v-model="lastName"
                        ></v-text-field>
                        <v-text-field
                            solo
                            v-if="checkoutFields.includes('Company Email')"
                            label="Company Email *"
                            v-model="companyEmail"
                            :rules="[validateEmail]"
                        ></v-text-field>
                        <v-select
                            solo
                            v-if="checkoutFields.includes('Department') && departments.length > 0"
                            label="Department *"
                            v-model="selectedDepartment"
                            :items="departments"
                            :item-text="d => d.name"
                            return-object
                        ></v-select>
                        <v-select
                            solo
                            v-if="checkoutFields.includes('Location') && locations.length > 0"
                            label="Location *"
                            v-model="selectedLocation"
                            :items="locations"
                            :item-text="l => l.nickname"
                            return-object
                        ></v-select>
                        <v-select
                            solo
                            v-if="checkoutFields.includes('Manager') && managers.length > 0"
                            label="Manager *"
                            v-model="selectedManager"
                            :items="managers"
                            :item-text="m => `${m.first_name} ${m.last_name}`"
                            return-object
                        ></v-select>

                        <!-- Custom fields -->
                        <v-text-field
                            solo
                            v-for="field in customCheckoutFields"
                            :key="field"
                            :label="field + '*'"
                            v-model="customCheckoutFieldsResult[field]"
                        ></v-text-field>

                    </v-card-text>
                </v-card>
            </v-flex>
            <v-flex xs10 mb-5>
                <v-card flat>

                    <v-card-text class="pa-0">
                        <v-data-table
                            :headers="headers"
                            :items="products"
                            class="elevation-1"
                            :rows-per-page-items="[25]"
                            :hide-actions="products.length < 50"
                        >
                            <template slot="items" slot-scope="props">
                                <td>
                                    <v-img
                                        crossorigin="anonymous"
                                        height="45"
                                        contain
                                    :src="getImg(props.item)">
                                    </v-img>
                                </td>
                                <td>{{ props.item.product.name }}</td>
                                <td>{{ props.item.attributes.size || 'No size'}}</td>
                                <td>${{ props.item.price.toFixed(2) }}</td>
                                <td class="text-xs-center text-no-wrap">
                                    <v-btn :disabled="quantityDecreaseDisabled(props.item)" icon @click="decreaseQuantity(props.item.id)">-</v-btn>
                                    {{ props.item.quantity }}
                                    <v-btn :disabled="quantityIncreaseDisabled(props.item)" icon @click="increaseQuantity(props.item.id)">+</v-btn>
                                </td>
                                <td>${{ props.item.total.toFixed(2) }}</td>
                                <td>
                                    <v-btn flat color="error" @click="deleteItem(props.item.id)">remove</v-btn>
                                </td>
                            </template>
                        </v-data-table>
                    </v-card-text>

                    <v-card-actions class="mt-3">
                        <v-spacer></v-spacer>
                        <div class="headline mr-4">Total: ${{ total.toFixed(2) }}</div>
                    </v-card-actions>
                </v-card>
                <div class="text-xs-center">
                    <v-btn
                        outline
                        large
                        @click="$router.push('/')"
                        color="primary"
                    >
                        keep shopping
                    </v-btn>



                     <v-tooltip :disabled='stateTip' bottom >
                       <v-btn slot="activator"
                              large
                              @click="checkout"
                              color="primary"
                              :disabled="placeOrderButtonDisabled"
                          >
                              place order
                          </v-btn>
                      <span>Yikes! Please complete the checkout form above before placing your order, thanks!</span>
                      </v-tooltip>


                    </div>

            </v-flex>
        </v-layout>
    </v-container>
</template>


<script>

import axios from '@/axios'
import rules from '@/mixins/rules'

export default {

    mixins: [
        rules
    ],

    data () {
        return {
            disabledTip: false,
            cart: {},
            headers: [
                {text: '', align: 'center'},
                {text: 'Name', value: 'product.name'},
                {text: 'SKU', value: 'attributes.size'},
                {text: 'Price', value: 'price'},
                {text: 'Quantity', value: 'quantity', align: 'center'},
                {text: 'Total', value: 'total'},
                {text: 'Actions'},
            ],
            products: [],

            checkoutFields: [],
            customCheckoutFields: [],

            managers: [],
            departments: [],
            locations: [],

            firstName: null,
            lastName: null,
            companyEmail: null,
            selectedManager: null,
            selectedDepartment: null,
            selectedLocation: null,
            customCheckoutFieldsResult: {},
            checkouting: false
        }
    },

    mounted () {
        this.load()
    },




    watch: {
        firstName (val) {
            localStorage.setItem('firstName', val)
        },
        lastName (val) {
            localStorage.setItem('lastName', val)
        },
        companyEmail (val) {
            localStorage.setItem('companyEmail', val)
        },
        selectedManager (val) {
            localStorage.setItem('selectedManager', JSON.stringify(val))
        },
        selectedDepartment (val) {
            localStorage.setItem('selectedDepartment', JSON.stringify(val))
        },
        selectedLocation (val) {
            localStorage.setItem('selectedLocation', JSON.stringify(val))
        }
    },


    computed: {
        total () {
            let sum = 0
            this.products.forEach(p => {
                sum += p.total
            })
            return sum
        },

        stateTip() {
          return this.disabledTip
        },


        placeOrderButtonDisabled () {
            let disabled = false
            this.disabledTip = true

            if (
                (this.checkoutFields.includes('First Name') && !this.firstName) ||
                (this.checkoutFields.includes('Last Name') && !this.lastName) ||
                (this.checkoutFields.includes('Company Email') && !this.companyEmail) ||
                (this.checkoutFields.includes('Manager') && this.managers.length > 0 && !this.selectedManager) ||
                (this.checkoutFields.includes('Department') && this.departments.length > 0 && !this.selectedDepartment) ||
                (this.checkoutFields.includes('Location') && this.locations.length > 0 && !this.selectedLocation) ||
                this.checkouting
            ) {
                disabled = true
                this.disabledTip = false
            } else {
                if (this.$data.products.length === 0) {
                     disabled = true
                    this.disabledTip = false
                }
            }

            this.customCheckoutFields.forEach(field => {
                if (!this.customCheckoutFieldsResult[field]) {
                   disabled = true
                    this.disabledTip = false
                }
            })

            return disabled
        }
    },

    methods: {

        load () {
            this.cart = JSON.parse(localStorage.getItem('cartProducts'))
            this.loadProducts()
            let params2 = {headers: {
                'Authorization': this.$store.state.token,
                'X-Fields': '*,accounts{*}'}}
            axios.get(`/campaigns/${localStorage.getItem('campaign_id')}`, params2).then(resp => {

                // Managers
                this.managers = resp.data.accounts.filter(account => account.role.name == 'Manager')

                // Departments
                this.departments = resp.data.departments

                // Locations
                this.locations = resp.data.locations

                // Checkout fields
                this.checkoutFields = Object.keys(resp.data.checkout_fields.properties)
                this.customCheckoutFields = Object.keys(resp.data.checkout_fields.properties).filter(
                    f => ![
                        'First Name',
                        'Last Name',
                        'Company Email',
                        'Department',
                        'Location',
                        'Manager'
                    ].includes(f)
                )
                this.loadCheckoutInfo()
            }).catch(err => {
                this.$store.dispatch('raiseError', err)
            })
        },

       off() {
        return false
      },

        loadCheckoutInfo () {
            this.firstName = localStorage.getItem('firstName');
            this.lastName = localStorage.getItem('lastName');
            this.companyEmail = localStorage.getItem('companyEmail');
            this.selectedManager = JSON.parse( localStorage.getItem('selectedManager') )
            this.selectedDepartment = JSON.parse( localStorage.getItem('selectedDepartment') );
            this.selectedLocation = JSON.parse( localStorage.getItem('selectedLocation') );
        },

        clearCheckoutInfo () {
            localStorage.setItem('firstName', '');
            localStorage.setItem('lastName', '');
            localStorage.setItem('companyEmail', '');
            localStorage.setItem('selectedManager', '');
            localStorage.setItem('selectedDepartment', '');
            localStorage.setItem('selectedLocation', '');
        },

        loadProducts () {
            if (!_.isEmpty(this.cart)) {
                this.products = []
                let params = {headers: {
                    Authorization: this.$store.state.token,
                    'X-Fields': '*,product{name,resources}'}}
                Object.keys(this.cart).forEach(pvid => {
                    axios.get(`/products/variants/${pvid}`, params).then(resp => {
                        let pv = resp.data
                        pv.quantity = this.cart[pvid]
                        pv.total = pv.price * this.cart[pvid]
                        let attributes = {}
                        pv.attributes.forEach(attr => {
                            attributes[attr.name.toLowerCase()] = attr.value
                        })
                        pv.attributes = attributes
                        this.products.push(pv)
                    })
                })
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
            return `${process.env.API_BASE_URL}/static/default-product.png`
        },

        increaseQuantity (id) {
            let index = this.products.findIndex(p => p.id == id)
            this.products[index].quantity += 1
            this.products[index].total += this.products[0].price
            this.cart[id] += 1
            localStorage.setItem('cartProducts', JSON.stringify(this.cart))
            this.updateParents()
        },

        decreaseQuantity (id) {
            let index = this.products.findIndex(p => p.id == id)
            this.products[index].quantity -= 1
            this.products[index].total-= this.products[0].price
            this.cart[id] -= 1
            localStorage.setItem('cartProducts', JSON.stringify(this.cart))
            this.updateParents()
        },
        quantityDecreaseDisabled (item) {
            return item.quantity <= 1
        },
        quantityIncreaseDisabled (item) {
            return false
        },

        updateParents () {
            this.$parent.$parent.$parent.update()
            this.$parent.$parent.$parent.$refs.popupCart.update()
        },

        deleteItem (id) {
            delete this.cart[id];
            localStorage.setItem('cartProducts', JSON.stringify(this.cart))
            this.products = this.products.filter(p => p.id != id)
            this.updateParents()
        },

        getDataUri(url, callback) {
            var image = new Image();
            image.setAttribute('crossOrigin', 'anonymous');
            image.onload = function () {
                var canvas = document.createElement('canvas');
                canvas.width = this.naturalWidth; // or 'width' if you want a special/scaled size
                canvas.height = this.naturalHeight; // or 'height' if you want a special/scaled size

                canvas.getContext('2d').drawImage(this, 0, 0);

                // Get raw image data
                callback(canvas.toDataURL('image/png').replace(/^data:image\/(png|jpg);base64,/, ''));

                // ... or get as Data URI
                callback(canvas.toDataURL('image/png'));
            };

            image.src = url;
        },

        loadBasketImg (data) {
            let dataBasketLength = data.basket.length
            let loadedImagesCount = 0
            let i = 0
            for (i; i < dataBasketLength-1 ; i++) {
                this.getDataUri(data.basket[i].img_url, (uri) => {
                    data.basket[i].img_url = uri
                    loadedImagesCount++;
                    if (dataBasketLength == loadedImagesCount) {
                        this.sendOrder(data);
                    }
                })
            }
        },

        getBasketArr (basketObj) {
            let basketArr = []
            let basketIndex = 0
            for (var property in basketObj) {
              if (basketObj.hasOwnProperty(property)) {
                basketArr.push({
                    'product_variant_id': property,
                    'quantity': basketObj[property],
                    'img_url': this.getImg(this.products.filter(obj => { return obj.id === parseInt(property) })[0])
                })
                basketIndex++;
              }
            }
            return basketArr;
        },

        checkout () {
            this.checkouting = true;
            let data = {}
            this.checkoutFields.includes('First Name') && (data['First Name'] = this.firstName)
            this.checkoutFields.includes('Last Name') && (data['Last Name'] = this.lastName)
            this.checkoutFields.includes('Company Email') && (data['Company Email'] = this.companyEmail)
            this.checkoutFields.includes('Department') && (data['Department'] = this.selectedDepartment.name)
            this.checkoutFields.includes('Location') && (data['Location'] = this.selectedLocation.nickname)
            this.checkoutFields.includes('Manager') && (
                data['Manager'] = `${this.selectedManager.first_name} ${this.selectedManager.last_name}`)
            data = Object.assign({}, data, this.customCheckoutFieldsResult)
            let basketObj = JSON.parse(localStorage.getItem('cartProducts'))

            data = {
                'checkout_fields': data,
                'basket': this.getBasketArr(basketObj)
            }
            if ( this.checkItemsCountLimit(basketObj) && this.checkPriceLimit() ) {
                //this.loadBasketImg(data)
                this.sendOrder(data);
            } else {
                this.checkouting = false;
            }
        },

        sendOrder (data) {
            let params = {headers: {'Authorization': this.$store.state.token}}
            axios.post('/storefront/checkout', data, params).then(resp => {
                this.checkouting = false;
                this.clearCheckoutInfo();
                this.updateParents()
                localStorage.removeItem('cartProducts')
                this.logout()
                this.$router.push('/order_confirmation')
            }).catch(err => {
                this.$store.dispatch('raiseError', err)
            })
        },

        checkItemsCountLimit (basketObj) {
            let isLimitCorrect = true
            if (this.$store.state.account.campaign.items_count_limit) {
                let total = 0;
                for (var property in basketObj) {
                    total += basketObj[property];
                }
                if ( total > this.$store.state.account.campaign.items_count_limit) {
                    this.$store.dispatch('raiseError', 'Total items in basket are more than limit('+ this.$store.state.account.campaign.items_count_limit +')')
                    isLimitCorrect = false
                }
            }
            return isLimitCorrect
        },

        checkPriceLimit () {
            let isLimitCorrect = true

            if ( this.$store.state.account.campaign.price_limit && this.total > this.$store.state.account.campaign.price_limit) {
                this.$store.dispatch('raiseError', 'Total items cost are more than limit('+ this.$store.state.account.campaign.price_limit +')')
                isLimitCorrect = false
            }
            return isLimitCorrect
        },

        logout () {
             this.clearCheckoutInfo()
             localStorage.removeItem('cartProducts')
            localStorage.removeItem('user')
            localStorage.removeItem('user_id')
          this.$store.commit('setAccount', null)
        }
    }
}
</script>

<style scoped>
.total {
    float: right;
}
</style>
