<template>
  <v-layout justify-center column fill-height mt-3 ml-3>
    <v-flex xs10 mt-5>
      <v-card>

        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2">Add Product</h3>
          </div>
        </v-card-title>



        <v-card-text>
          <v-form v-model="validProductSetup">
            <v-autocomplete
              v-model="newProduct"
              :items="products"
              item-text="name"
              item-value="id"
              label="Product"
              return-object
              @change="getProductAttributes(newProduct.product_type.id)"
            ></v-autocomplete>
            <v-card v-for="(item, index) in newAttributes" px-2 :key="item.index">
              <v-card-text>
                <h3>Attribute {{item.name}}</h3>
                <v-layout align-center justify-center row fill-height wrap>
                  <v-checkbox
                    v-for="(item) in newAttributes[index].values"
                    :label="item"
                    @change="addValue(item, index)"
                    :key="index"
                  ></v-checkbox>
                </v-layout>
              </v-card-text>
            </v-card>
            <v-card>
              <v-layout>
                <v-flex ml-2>
                  <h3 v-if="OwCost">Order Write Cost: ${{OwCost.toFixed(2)}}</h3>
                  <v-text-field v-model="vendorName" label="Vendor Name" :rules="emptyRules" required></v-text-field>
                  <v-text-field v-model.number="vendorCost" type="number" label="Vendor Cost $" :rules="numberRules" required></v-text-field>
                  <v-btn @click="createUpcharge" v-if="vendorCost">
                    Add Upcharge
                  </v-btn>
                  <v-form v-for="(upcharge, index) in upcharges" :key="index">
                    <v-select
                      :items="attributesNames"
                      label="Attribute"
                      v-model="upcharge.attribute.name"
                    ></v-select>
                    <v-radio-group v-if="upcharge.attribute.name" v-model="upcharge.attribute.value">
                      <v-radio
                        v-for="(attributeName) in getAttributesValues(upcharge.attribute.name)"
                        :label="attributeName"
                        :value="attributeName"
                        :key="attributeName"
                      ></v-radio>
                    </v-radio-group>
                    <v-text-field
                      v-if="upcharge.attribute.value"
                      label="Margin %"
                      type="number"
                      :rules="marginRules"
                      required
                      v-model.number="upcharge.margin"
                    ></v-text-field>
                    <v-text-field
                      v-if="upcharge.margin"
                      label="UpCharge $"
                      type="number"
                      v-model.number="upcharge.upcharge"
                    ></v-text-field>
                    <h3 v-if="upcharge.upcharge">Sell Price: ${{getTotalPriceUpcharge(upcharge.upcharge, upcharge.margin)}}</h3>
                    <v-btn @click="removeUcharge(index)">
                      Remove
                    </v-btn>
                  </v-form>
                  <v-text-field v-model.number="margin" type="number" label="Margin %" :rules="marginRules" required></v-text-field>
                  <v-text-field v-model.number="bagFoldLabelCost" type="number" label="Bag Fold Label Cost $" :rules="numberRules" required></v-text-field>
                  <h3 v-if="vendorName">Sell Price: ${{getTotal()}}</h3>

                </v-flex>
                <v-flex ml-2>
                  <v-card v-for="(item, index) in decorations" :key="item.index">
                    <v-text-field v-model="item.decorator_name" label="Decorator name" text-overflow='ellipsis'></v-text-field>
                    <v-text-field v-model="item.logo_description" label="Logo Description" ></v-text-field>
                    <v-text-field v-model.number="item.decoration_cost"
                                  @change="countDecorationSum(item.decoration_cost)"
                                  label="Decoration Cost $"
                                  type="number" ></v-text-field>
                    <v-text-field v-model="item.decoration_location" label="Decoration Location" ></v-text-field>
                    <v-btn @click="removeDecoration(index)">Remove</v-btn>
                  </v-card>
                  <v-btn
                    @click="createDecoration"
                  >
                    Add decoration
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-card>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="primary"
            @click="submit"
            :disabled="!validProductSetup"
          >
            Create
          </v-btn>
        </v-card-actions>



      </v-card>
    </v-flex>

  </v-layout>
</template>

<script>
  import axios from '@/axios'
  const nameRegex = /^[a-z A-Z0-9]+$/
  const numberRegex = /^[0-9]+$/

  export default {
    data () {
      return {
        validProductSetup: false,
        id: this.$route.params.id,
        token: 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
        //UpCharges
        attributesNames: [],
        upcharges: [],
        //
        OwCost: null,
        distributorId: null,
        description: '',
        vendorCost: null,
        vendorName: '',
        bagFoldLabelCost: null,
        decorationsCost: 0,
        decorations: [],
        newProduct: {name: '', id: ''},
        products: [],
        attributes: [],
        newAttributes: [],
        attributesList: [],
        margin: null,
        marginOversize: '',
        attributesObg: {},
        sellPrice: 0,
        //validation
        nameRules: [
          v => !!v || 'Is required',
          v => nameRegex.test(v) || 'Must be valid'
        ],
        emptyRules: [
          v => !!v || 'Is required'
        ],
        numberRules: [
          v => numberRegex.test(v) || 'Must be valid'
        ],
        marginRules: [
          v => v < 100 || 'Must be less than 100%'
        ],
      }
    },
    methods: {
      getTotalPriceUpcharge(upcharge, margin){
        let totalPrice = this.$data.vendorCost +
          this.$data.bagFoldLabelCost +
          this.$data.OwCost + upcharge +
          this.$data.decorationsCost
        let sellPrice = totalPrice / (1 - (margin / 100))
        return sellPrice.toFixed(2)
      },
      getTotal () {
        let totalPrice = this.$data.vendorCost +
          this.$data.bagFoldLabelCost +
          this.$data.OwCost +
          this.$data.decorationsCost
        let sellPrice = totalPrice / (1 - (this.$data.margin / 100))
        return sellPrice.toFixed(2)
      },
      getOwCost (){
        let params = {
          headers: {
            'Authorization': this.$data.token,
            'X-Fields': 'distributor_id'
          }
        }
        axios.get(`/campaigns/${this.$data.id}`, params).then(resp => {
          this.$data.distributorId= resp.data.distributor_id
          let params = {
            headers: {
              'Authorization': this.$data.token,
              'X-Fields': 'ow_cost'
            }
          }
          axios.get(`/distributors/${this.$data.distributorId}`, params).then(resp => {
            this.$data.OwCost = resp.data.ow_cost
          }).catch(err => {
            console.log(err)
          })
        }).catch(err => {
          console.log(err)
        })
      },
      getAttributesValues(name){
        if  (this.$data.attributesList.find(x => x.name === name)) {
          let attribute = this.$data.attributesList.find(x => x.name === name);
          let values = attribute.values
          return values
        }
      },
      removeUcharge(index) {
        this.$data.upcharges.splice(index, 1);
      },
      createUpcharge() {
        function UpchargeConstructor() {
          this.attribute = {
            name: '',
            value: ''
          }
          this.upcharge = 0
          this.margin = 0
        }
        let upcharge = new UpchargeConstructor();
        this.$data.upcharges.push(upcharge);
        console.log(this.$data.upcharges)
      },
      addValue (valueName, index) {
        let valueIndex = this.attributesList[index].values.indexOf(valueName)
        if (valueIndex === -1) {
          this.$data.attributesList[index].values.push(valueName)
          console.log(this.$data.attributesList)
        } else {
          this.$data.attributesList[index].values.splice(valueIndex, 1)
        }
      },
      countDecorationSum(sum) {
        this.$data.decorationsCost =+sum
      },
      createDecoration () {
        function DecorationConstructor () {
          this.decorator_name = ''
          this.logo_description = ''
          this.decoration_cost = 0
          this.decoration_location = ''
        }

        let decoration = new DecorationConstructor()
        this.$data.decorations.push(decoration)
        console.log(this.$data.decorations)
      },
      removeDecoration (index) {
        this.$data.decorations.splice(index, 1)
      },
      createAttributesObg () {
        this.$data.attributesList.forEach((item) => {
           delete item.id
        })
      },
      submit () {
        this.createAttributesObg()
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        let data = {
          vendor_name: this.$data.vendorName,
          vendor_cost: this.$data.vendorCost,
          upcharges: this.$data.upcharges,
          decorations: this.$data.decorations,
          margin: this.$data.margin,
          attributes: this.$data.attributesList,
          product_id: parseInt(this.$data.newProduct.id),
          campaign_id: parseInt(this.$data.id)
        }
        axios
          .post(`/products/variants/multiple`, data, params)
          .then(resp => {
            this.$router.go(`/campaign_edit/${this.$data.id}/6`);
          })
          .catch(err => {
            console.log(err)
          })
      },
      // Badges removing from input
      getProductAttributes (id) {
        this.$data.newAttributes = []
        this.$data.attributesList = []
        this.$data.attributesNames = []
        this.$data.upcharges = []
        let params = {
          headers: {
            'Authorization': this.$data.token,
            'X-Fields': '*'
          }
        }
        axios.get(`/products/types/${id}`, params).then(resp => {
          this.$data.attributes = resp.data.product_attributes
          this.$data.newAttributes = JSON.parse(JSON.stringify(resp.data.product_attributes))
          this.$data.attributesList = JSON.parse(JSON.stringify(resp.data.product_attributes))
          this.$data.attributesList.forEach((item, index) => {
            this.$data.attributesList[index].values = []
          })
          this.$data.attributesList.forEach((val) => {
            this.$data.attributesNames.push(val.name)
          })
          console.log(this.$data.attributesNames)
          console.log(this.$data.attributesList)
        }).catch(err => {
          console.log(err)
        })
      }
    },
    mounted () {
      // Get products
      this.getOwCost()
      let params = {
        headers: {
          'Authorization': this.$data.token,
          'X-Fields': 'id,name,product_type'
        }
      }
      axios.get('/products', params).then(resp => {
        console.log(resp.data)
        this.$data.products = resp.data
      }).catch(err => {
        console.log(err)
      })
    }
  }
</script>
