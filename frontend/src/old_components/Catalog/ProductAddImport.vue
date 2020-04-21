<template>
  <v-layout justify-center>
    <v-flex mt-5>
      <v-card>

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2">New Product</h3>
          </div>
        </v-card-title>

        <v-form ref="form" lazy-validation>

          <v-card-text>
            <v-text-field
              v-model="name"
              label="Name"
              required
            ></v-text-field>
            <v-text-field
              v-model="number"
              label="Item #"
              required
            ></v-text-field>
            <v-select
              v-model="selectedDistributor"
              :items="possibleDistributors"
              item-text="name"
              item-value="id"
              label="Distributors"
              return-object
            >
            </v-select>
            <v-radio-group v-model="type_id" row>
              <v-radio  v-for="type in types"
                        :label="type.name"
                        :key="type.name"
                        :value="type.id"></v-radio>
            </v-radio-group>
          </v-card-text>

          <v-card-actions>
            <v-btn
              color="primary"
              left
              @click="save"
            >
              Save
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
        number: null,
        types: [],
        type_id: null,
        selected_attributes: [],
        possibleDistributors: [],
        selectedDistributor: {
        },
        attributes_mapping: {}
      }
    },

    mounted () {
      axios.get(`/products/types`, {
        headers: {
          'Authorization': this.$data.token
        }
      }).then(resp => {
        this.$data.types = resp.data
      })
      axios.get(`/distributors`, {
        headers: {
          'Authorization': this.$data.token,
          'X-Fields': 'id, name'
        }
      }).then(resp => {
        this.$data.possibleDistributors = resp.data
      })
    },
    methods: {
      save () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        let data = {
          name: this.$data.name,
          item_number: this.$data.number,
          product_type_id: this.$data.type_id,
          distributor_id: this.$data.selectedDistributor.id
        }
        axios
          .post('/products', data, params)
          .then(resp => {
            this.$router.push(`/product/${resp.data.id}`)
          })
          .catch(err => {
            console.log(err)
          })
      }
    }
  }
</script>
