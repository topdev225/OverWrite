<template>

  <v-card class="elevation-3" v-show="productCreationModalEnabled">
    <v-card-text>
      <v-window v-model="activeWindow">

        <v-window-item :value="1">
          <product
            ref="product"
            :product-types="productTypes"
            @switch-window="switchWindow"
            @show-options="showOptionsEvent"
            @add-product="addProduct"
          />
          <product-variant
            class="mt-4"
            v-show="showOptions || editing"
            ref="productVariant"
            :products="products"
            :productName="productName"
            @switch-window="switchWindow"
          />
        </v-window-item>

      </v-window>
    </v-card-text>

    <v-divider></v-divider>


    <v-alert
      :value="product.is_ordered"
      color="error"
      icon="priority_high"
      outline
      class="ma-3"
    >
      <div>
        Can't update while product is ordered
      </div>
    </v-alert>

    <v-progress-linear
      :active="isSaving"
      :indeterminate="isSaving"
      absolute
      bottom
      color="success"
    ></v-progress-linear>

    <div class="text-xs-right px-2 py-2">
      <v-btn color="error" @click="close">Close</v-btn>
      <v-btn v-if="showOptions == true" color="primary" @click="save" :disabled="saveButtonDisabled">Save</v-btn>
      <v-btn v-if="showOptions == false" color="info" @click="next" :disabled="nextButtonDisabled">Next</v-btn>
    </div>


    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Warning!</v-card-title>
        <v-card-text>All data is not saved. Do you really want to leave?</v-card-text>
        <div class="text-xs-center px-2 py-2">
          <div class="flex-grow-1"></div>
          <v-btn color="error" text @click="hideWarningDialog">Cancel</v-btn>
          <v-btn color="success" text @click="exitFromEditMode">Ok</v-btn>
        </div>
      </v-card>
    </v-dialog>

  </v-card>


</template>


<script>

  import axios from '@/axios'

  import SelectType from './SelectType'
  import Product from './Product'
  import ProductVariant from './ProductVariant'

  export default {

    props: [
      'products'
    ],

    components: {
      'select-type': SelectType,
      'product': Product,
      'product-variant': ProductVariant
    },

    data() {
      return {
        dialog: false,
        isMounted: false,
        isSaved: true,
        isSaving: false,
        // Window related
        productCreationModalEnabled: false,
        activeWindow: 1,
        showOptions: false,
        productName: null,
        productID: null,

        // Loaded data
        productTypes: [],

        // Edit mode
        editing: false,
        editingIndex: null,

        product: {},
      }
    },

    computed: {
      saveButtonDisabled() {
        // Default state
        let disabled = true
        // Pass if not mounted yet
        if (!this.$data.isMounted)
          return disabled

        if (
          /* enable if is not ordered + ... */
          !this.$data.product.is_ordered &&
          this.$refs.productVariant.productName &&
          this.$refs.productVariant.$data.basicInfoFormValid &&
          this.$refs.productVariant.$data.vendor_name &&
          this.$refs.productVariant.$data.vendor_cost &&
          parseFloat(this.$refs.productVariant.$data.margin) > 0 &&
          this.$refs.productVariant.$data.decorations &&
          this.$refs.productVariant.$data.decorations.length &&
          this.checkProductVariantSets() &&
          this.$data.isSaved
        )
          disabled = false
        return disabled
      },

      nextButtonDisabled() {
        let disabled = true
        // Pass if not mounted yet
        if (!this.$data.isMounted)
          return disabled
        if (this.$refs.product.$data.name && this.$refs.product.$data.productTypeID && this.$refs.product.$data.productFormValid)
          disabled = false
        return disabled
      },
    },

    mounted() {
      this.$data.isMounted = true
      this.$data.isSaving = false
    },

    methods: {

      checkProductVariantSets() {
        let setsNotEmpty = true
        if (!this.$refs.productVariant.productVariantSets || this.$refs.productVariant.productVariantSets.length === 0) {
          setsNotEmpty = false
        } else {
          this.$refs.productVariant.productVariantSets.forEach((productVariantSet) => {
            setsNotEmpty = setsNotEmpty && (productVariantSet.major && productVariantSet.major.length != 0)
            if (Object.keys(this.$refs.productVariant.productAttributes).length > 1) {
              setsNotEmpty = setsNotEmpty && Object.values(productVariantSet.minor).indexOf(true) != -1
            }
          })
        }
        return setsNotEmpty
      },

      // Data loaders

      async loadProductTypes() {
        const {distributor} = this.$store.state.campaign;
        const filters = [];
        if (distributor && distributor.id) {
          filters.push({"field": "distributor_id", "op": "==", "value": distributor.id});
        }
        const params = {headers: {'X-Filters': JSON.stringify(filters)}};
        const {data} = await this.$axios.get('/products/related-product-types', params);
        this.productTypes = data.map(relatedProductType => relatedProductType.product_type);
      },

      // Modal events

      enable(product, index) {
        this.productCreationModalEnabled = true
        this.isSaved = true
        this.loadProductTypes()
        this.$refs.product.drop()
        this.$store.state.title = 'Product Uploader'
        // Editing mode
        if (product) {
          this.editing = product
          this.editingIndex = index
          this.showOptions = true
          this.productName = product.name
          this.productID = product.id
          this.product = product;
          this.$store.state.title = `Product Uploader - ${product.name}`
          this.$nextTick(() => {
            this.$refs.product.load(product)
            this.$refs.productVariant.load(product.product_variants)
            setTimeout(this.$refs.productVariant.init, 300)
            setTimeout(function () {
              window.dispatchEvent(new Event('resize'))
            }, 400)
          })
        }
      },

      close() {
        // if (confirm('Are you sure you want to save this thing into the database?')) {
        //   !this.editing && (this.products[this.products.length-1].name === this.productName) && this.products.pop()
        // this.disable()
        // } else {
        //    // Do nothing!
        // }
        this.dialog = true

      },

      exitFromEditMode() {
        this.$refs.productVariant.$data.deletedServerProductVariantSets = []
        this.dialog = false
        !this.editing && this.products && this.products[this.products.length - 1] && (this.products[this.products.length - 1].name === this.productName) && this.products.pop()
        this.disable()
      },

      hideWarningDialog() {
        this.dialog = false
      },


      disable() {

        this.$data.isSaving = false
        this.productCreationModalEnabled = false
        this.activeWindow = 1
        this.editing = false
        this.editingIndex = null
        this.$store.state.title = ''

        // Drop fields
        setTimeout(function () {
          try {
            this.$refs.product.$refs.productForm.reset()
            this.$refs.productVariant.$refs.basicInfoForm.reset()
            if (this.$refs.productVariant.$refs.upchargesForm)
              this.$refs.productVariant.$refs.upchargesForm.reset()
            if (this.$refs.productVariant.$refs.decorationsForm)
              this.$refs.productVariant.$refs.decorationsForm.reset()
            this.$refs.product.editing = false
            this.$refs.productVariant.productAttributes = {}
            this.$refs.productVariant.selectedProductAttributes = {}
            this.$refs.productVariant.productVariantSets = []
            this.$refs.productVariant.upcharges = []
            this.$refs.productVariant.decorations = []
            this.showOptions = false
          } catch
            (e) {

          }

        }.bind(this), 0)
      },

      // Child events

      switchWindow(number) {
        this.$data.activeWindow = number
      },

      showOptionsEvent() {
        this.$data.showOptions = true
        // Preset for decorations
        let product = this.$parent.$refs.products.$data.campaignProducts[
        this.$parent.$refs.products.$data.campaignProducts.length - 1
          ]
        if (product) {
          let pv = product.product_variants[0]
          let decoration = pv.decorations[0]
          /*                this.$refs.productVariant.vendor_name = pv.vendor_name
                          this.$refs.productVariant.vendor_cost = pv.vendor_cost*/
          this.$refs.productVariant.decorator_name = decoration.decorator_name
          this.$refs.productVariant.logo_description = decoration.logo_description
          this.$refs.productVariant.decoration_cost = decoration.decoration_cost
          this.$refs.productVariant.decoration_location = decoration.decoration_location
          this.$refs.productVariant.decoration_id = decoration.decoration_id
        }
        this.$nextTick(function () {
          // DOM updated
          window.dispatchEvent(new Event('resize'))
          setTimeout(function () {
            window.dispatchEvent(new Event('resize'))
          }, 1000)
        });
      },

      addProduct(product) {
        // Add new product to server
        let params = {headers: {'Authorization': this.$store.state.token}}
        axios.post('/products', product, params).then(resp => {
          // Extend with empty resources
          resp.data.resources = []
          // Add to global list
          this.$emit('add-product', resp.data)
          // Set product name in Product Variant window
          this.productName = product.name
          this.productID = resp.data.id
          this.product = product;
          setTimeout(this.$refs.productVariant.init, 300)
        })
      },

      setProductDefaultImage(resource, productName, callback = () => {
      }) {
        let params = {headers: {'Authorization': this.$store.state.token}}
        axios.post(`/data_resources/${resource.uuid}/duplicate`, null, params)
          .then(resp => {
            this.$emit('set-product-default-image', resp.data, productName)
            callback(resp.data)
          })
          .catch(error => {
            console.log(error.response)
          });


      },

      next() {
        let name = this.$refs.product.name
        let itemNumber = this.$refs.product.itemNumber
        let productTypeID = this.$refs.product.productTypeID
        let nameIsExsist = this.$parent.$refs.products.$data.campaignProducts.find(obj => {
          return obj.name.toLowerCase() === name.toLowerCase() &&
            obj.item_number.toLowerCase() === itemNumber.toLowerCase() &&
            obj.product_type_id === productTypeID

        });
        if (nameIsExsist) {
          this.$store.dispatch('raiseError', 'Product with this name is already exsist')
        } else {
          this.$store.state.title = `Product Uploader - ${this.$refs.product.name}`
          this.$refs.productVariant.$data.defaultProductVariantSetsActive = true
          this.$refs.productVariant.$data.defaultDecorationActive = true
          this.$refs.product.next()
        }
      },

      addProductVariants() {
        this.$refs.productVariant.productVariants((variants, removed_variants, all_variants) => {
          // Add variants
          this.$emit(
            'add-product-variants',
            {
              productID: this.productID,
              productVariants: variants,
              removed_variants: removed_variants,
              all_variants: all_variants,
              callback: this.disable,
              product: this.product,
            }
          )
        })
      },

      save() {
        this.$data.isSaved = false
        this.$data.isSaving = true

        // Update product, if editing
        if (this.editing) {
          this.productName = this.$refs.product.name
          this.editing.name = this.$refs.product.name
          this.editing.item_number = this.$refs.product.itemNumber
          this.editing.product_type_id = this.$refs.product.productTypeID
          this.$emit('update-product', this.editing, this.editingIndex)
        }

        // Set product default image
        let res = this.$refs.productVariant.defaultImagePvsIndex !== null && this.$refs.productVariant.productVariantSets[this.$refs.productVariant.defaultImagePvsIndex] ?
          this.$refs.productVariant.productVariantSets[this.$refs.productVariant.defaultImagePvsIndex].resource :
          null;
        if (res) {
          this.setProductDefaultImage(res, this.productName, this.addProductVariants.bind(this))
        } else {
          this.addProductVariants();
        }
      }
    }
  }
</script>
