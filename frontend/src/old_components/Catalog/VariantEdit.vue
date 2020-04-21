<template>
  <v-layout justify-center>
    <v-flex xs10 mt-5>
      <v-card>

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2">Update variant</h3>
          </div>
        </v-card-title>

        <v-form ref="form" lazy-validation>

          <v-card-text>
            <v-text-field
              v-model="name"
              label="Variant name"
              required
            ></v-text-field>
            <v-text-field
              v-model="sku"
              label="SKU"
              required
            ></v-text-field>
            <v-flex xs12 sm6 d-flex v-for="attribute in attributes" :key="attribute.id">
              <v-select
                :items="attribute.values"
                :label="attribute.name"
                v-model="setAttributes[attribute.name]"
              ></v-select>
            </v-flex>
          </v-card-text>

          <v-card-actions>
            <v-btn @click="$router.push('/admin/products/'+ productId)" absolute right flat color="primary">Cancel</v-btn>
            <v-btn
              @click="submit"
              color="primary">
              submit
            </v-btn>
          </v-card-actions>

        </v-form>

      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>

  import axios from '@/axios'

  export default {

    data () {
      return {
        token: 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
        name: '',
        sku:  '',
        productId: null,
        attributes: [],
        setAttributes: {},
      }
    },

    mounted () {
      // Request params
      let params = { headers: {
          'Authorization': this.$data.token,
          'X-Fields' : '*'
        }}
      // Get possible attributes
      axios.get(`/products/variants/${this.$route.params.id}`, params).then(resp => {
        this.$data.productId = resp.data.product.id
        this.$data.name = resp.data.name
        this.$data.sku = resp.data.sku
        this.$data.setAttributes = resp.data.attributes
        console.log(resp.data)
        let paramsAttribute = { headers: {
            'Authorization': this.$data.token,
            'X-Fields': 'type{attributes}'
          }}
        // Get possible attributes
        axios.get(`/products/${this.$data.productId}`, paramsAttribute).then(resp => {
          this.$data.attributes = resp.data.type.attributes
        }).catch(err => {
          console.log(err)
        })
      }).catch(err => {
        console.log(err)
      })
    },

    methods: {
      submit () {
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        let data = {
          name: this.$data.name,
          sku: this.$data.sku,
          attributes: this.$data.setAttributes
        }
        axios.put(`/products/variants/${this.$route.params.id}`, data, params)
          .then(resp => {
          this.$router.push(`/admin/products/${this.$data.productId}`)
        }).catch(err => {
          console.log(err)
        })
      }
    }
  }
</script>
