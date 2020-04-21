<template>
  <v-layout justify-center column wrap mb-5>
    <v-layout align-center justify-center column wrap fill-height ma-3>
      <h2 v-if="campaignName">{{campaignName}}</h2>
      <v-jumbotron v-if="message">
        <v-container fill-height>
          <v-layout align-center>
            <v-flex>
              <h3>Message to users: </h3>
              <span>{{message}}</span>
            </v-flex>
          </v-layout>
        </v-container>
      </v-jumbotron>
    </v-layout>
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title>Product added to the Cart</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="dialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-layout justify-center row wrap ma-1>
      <v-flex v-for="(item) in products" :key="item.id" ma-2 xs3>
        <v-card>
          <v-card-text>
            <v-img
              contain
              :src="getImg(item)"
            ></v-img>
            <v-card-title primary-title>
              <v-layout align-start justify-center column fill-height>
                <div>
                  <v-text-field
                    v-if="item.selected_product_variant"
                    v-model="item.quantity"
                    label="Quantity"></v-text-field>
                  <h3>{{item.name}}</h3>
                  <p v-if='item.selected_product_variant'>
                    ${{item.selected_product_variant.price.toFixed(2)}}
                  </p>
                  <p v-else>Select the attributes</p>
                </div>
                <v-select
                  v-for="(attribute, index) in item.attributes"
                  :items="attribute.values"
                  :label="attribute.name"
                  @change="onAttributeChange(item, attribute.name)"
                  v-model="attr"
                  :key="index"
                ></v-select>
              </v-layout>
            </v-card-title>
          </v-card-text>
          <v-card-actions>
            <v-btn disabled
                   @click="addToCart(item.selected_product_variant.id, item.quantity)"
            >
              Add to Cart
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-layout>
</template>

<script>
  import axios from '@/axios'

  export default {
    data () {
      return {
        message:'',
        dialog: false,
        token: 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
        campaignId: this.$route.params.id,
        campaignName: '',
        raw_data: [],

        products: [],

        selectedAttributes: {},  // {item_id: {attr_name: attr_value}}
        selectedVariants: {},
        prices: {},

        attr: ''  // temp storage
      }
    },

    mounted () {
      this.retrieveData()
      this.getCampaignName(this.$data.campaignId)
    },

    methods: {
      getImg (item) {
        let defaultImg = `${process.env.API_BASE_URL}/static/default-product.svg`
        if (item.resources[0])
          return `${process.env.API_BASE_URL}/static/resources/${item.resources[0].uuid}.${item.resources[0].type}`
        else
          return defaultImg
      },
      addToCart (id, quantity) {
        axios.put(`/storefront/basket/${id}/${quantity}`, null, {
          headers: {
            'Authorization': this.$data.token
          }
        }).then(resp => {
          this.$data.dialog = true
        }).catch(err => {
          this.$store.dispatch('raiseError', err.response.data.message)
        })
      },
      getCampaignName (id) {
        axios.get(`campaigns/${id}`, {
          headers: {
            'Authorization': this.$data.token,
            'X-Fields': 'name,message'
          }
        }).then(resp => {
          this.$data.campaignName = resp.data.name
          this.$data.message = resp.data.message
        }).catch(err => {
          console.log(err)
          this.errors.push(err)
        })
      },
      retrieveData () {
        axios.get(`/storefront/products?campaign_id=${this.$route.params.id}`, {
          headers: {
            'Authorization': this.$data.token,
            'X-Fields': 'id,name,resources,product_variants{id,price,attributes}'
          }
        }).then(resp => {
          this.$data.raw_data = resp.data
          this.updateProducts()
        }).catch(err => {
          console.log(err)
          this.errors.push(err)
        })
      },

      updateProducts () {
        // Generate products list from raw data
        let products = []
        this.$data.raw_data.forEach((product) => {
          let selected = this.$data.selectedAttributes[product.id] || {}
          // Temp data structure {"attr_name": ["attr1", ...], ...}
          let attributes_temp = {}
          product.product_variants.forEach((product_variant) => {
            product_variant.attributes.forEach((attribute) => {
              if (!attributes_temp[attribute.name]) {
                attributes_temp[attribute.name] = []
              }
              attributes_temp[attribute.name].push(attribute.value)
            })
          })
          // Generate structure [ {"name": "attr_name", "values": ["attr1", ...]}, ... ]
          let attributes = []
          Object.entries(attributes_temp).forEach((pair) => {
            attributes.push({
              name: pair[0],
              values: pair[1]
            })
          })

          // Determine selected product variant
          // Extract needed attributes
          let attributes_names = attributes.map((attr) => {
            return attr.name
          })
          // Check all selected attributes
          let selected_needed = true
          attributes_names.forEach((attr_name) => {
            if (!selected[attr_name]) {
              selected_needed = false
            }
          })

          // Extract product variant
          let variant = null
          if (selected_needed) {
            product.product_variants.forEach((pv) => {
              // Check attributes
              let match = true
              pv.attributes.forEach((attr) => {
                if (selected[attr.name] !== attr.value) {
                  match = false
                }
              })
              if (match) {
                variant = pv
              }
            })
          }

          // Copy product
          let temp_product = JSON.parse(JSON.stringify(product))
          // Update nested info
          temp_product.attributes = attributes
          temp_product.selected_product_variant = variant
          temp_product.quantity = 1
          // Push to list
          products.push(temp_product)

        })
        // Update data
        this.$data.products = products

      },

      createAttributes (arr, index) {
        function AttributesConstructor () {
          this.name = ''
          this.values = []
        }
        let attributes = new AttributesConstructor()
        arr[index] = attributes
      },

      onAttributeChange (item, attr_name) {
        // Update selected attributes structure
        if (!this.$data.selectedAttributes[item.id]) {
          this.$data.selectedAttributes[item.id] = {}
        }
        this.$data.selectedAttributes[item.id][attr_name] = this.$data.attr
        this.$data.attr = ''
        this.updateProducts()
      }
    }
  }
</script>
