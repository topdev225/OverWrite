<template>
  <v-card class="elevation-3">

    <v-img class="product-card__img" :src=image style="flex-grow: 0 !important;cursor: pointer;"
           @click="editProduct"></v-img>

    <div
      class="title text-xs-center mt-3 overflow-hidden px-2"
      style="height: 2em; flex-grow: 0 !important; cursor: pointer;"
      @click="editProduct"
    >
      {{
      $props.product.name }}
    </div>

    <div
      class="text-xs-center overflow-hidden px-2"
      style="height: 3em; flex-grow: 0 !important;"
      v-for="decoration in decorations"
      :key=decoration.logo_description
    >
      {{ decoration.logo_description }} on {{ decoration.decoration_location }}
    </div>

    <div class="pa-2">
      <v-select
        key="major"
        :label="productMajorAttribute.name"
        :items="Object.keys(productAttributeItems)"
        @change="updateMajor(),updateSelectedVariant()"
        v-model="selectedAttributes[productMajorAttribute.name]"
      >
      </v-select>
      <v-select
        v-if="productMinorAttribute.name && selectedAttributes[productMajorAttribute.name] && productAttributeItems[selectedAttributes[productMajorAttribute.name]]"
        key="minor"
        :label="productMinorAttribute.name"
        :items="productAttributeItems[selectedAttributes[productMajorAttribute.name]]"
        @change="updateSelectedVariant"
        v-model="selectedAttributes[productMinorAttribute.name]"
      >
      </v-select>
    </div>

    <div v-if="selectedVariant" class="text-xs-center headline mb-2" style="flex-grow: 0 !important;">
      ${{ selectedVariantPrice && selectedVariantPrice.toFixed && selectedVariantPrice.toFixed(2) }}
    </div>


    <v-card-actions v-if="!($props.product.is_ordered === 1)" style="flex-grow: 0 !important;">
      <v-layout row wrap>
        <v-flex xs6>
          <v-btn block flat color="success" @click="editProduct" v-if="!complete">
            <v-icon>edit</v-icon>
          </v-btn>
        </v-flex>
        <v-flex xs6>
          <v-btn block flat color="error" @click="removeProduct" v-if="!complete">
            <v-icon>delete</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-card-actions>
    <div v-else class="pt-1 pb-3 text-xs-center" style="flex-grow: 0 !important;">
      <span class="font-italic">Product is ordered</span>
    </div>

  </v-card>
</template>


<script>
  import productVariantSetsMixin from '@/mixins/productVariantSets';

  export default {

    props: [
      'product',
      'index'
    ],

    mixins: [productVariantSetsMixin],

    data() {
      return {
        selectedAttributes: {},
      }
    },
    computed: {
      owCost() {
        return this.$store.state.campaign.distributor ? this.$store.state.campaign.distributor.ow_cost : 0
      },
      bflCost() {
        try {
          return parseFloat(this.$store.state.campaign.BFLCost)
        } catch (e) {
          return 0
        }
        //return this.$store.state.campaign.id ? this.$store.state.campaign.bfl_cost : 0
      },
      complete() {
        return this.$parent.$parent.$parent.$parent.$parent.$parent._data.campaign.complete
      },

      image() {
        // Filter product variants with selected attributes
        let pvs = this.product.product_variants.filter(p => {
          let found = true;
          p.attributes.forEach(attr => {
            if (!this.selectedAttributes[attr.name])
              return;
            if (attr.value != this.selectedAttributes[attr.name])
              found = false
          });
          return found
        });

        // Selected variant image
        if (this.selectedVariant && this.selectedVariant.resources[0]) {
          return `${process.env.API_BASE_URL}` +
            `/static` +
            `/resources` +
            `/${this.selectedVariant.resources[0].uuid}` +
            `.${this.selectedVariant.resources[0].type}`
        }
          // Not complete attributes selection
        // (only in case of pv image is exist)
        else if (Object.keys(this.selectedAttributes).length && pvs[0] && pvs[0].resources[0]) {
          let pv = pvs[0];
          return `${process.env.API_BASE_URL}` +
            `/static` +
            `/resources` +
            `/${pv.resources[0].uuid}` +
            `.${pv.resources[0].type}`
        }
        // Product image
        else if (this.$props.product.resources && this.$props.product.resources[0]) {
          return `${process.env.API_BASE_URL}` +
            `/static` +
            `/resources` +
            `/${this.$props.product.resources[0].uuid}` +
            `.${this.$props.product.resources[0].type}`
        }
        // First variant image
        else if (this.$props.product.product_variants[0].resources[0]) {
          let res = this.$props.product.product_variants[0].resources[0];
          return `${process.env.API_BASE_URL}` +
            `/static` +
            `/resources` +
            `/${res.uuid}` +
            `.${res.type}`
        }
        // Fallback
        else {
          return `${process.env.API_BASE_URL}/static/default-product.svg`
        }
      },

      attributes() {
        let res = {};
        this.$props.product.product_variants.forEach(variant => {
          variant.attributes.forEach(attr => {
            if (!res[attr.name]) {
              res[attr.name] = []
            }
            res[attr.name].push(attr.value);
            if (attr.name.toLowerCase() === 'size') {
              let size_cloth = res[attr.name];
              res[attr.name] = ["XXS", "XS", "S", "SM", "M", "MD", "L", "LG", "XL", "XXL", "2XL",
                "XXXL", "3XL", "XXXXL", "4XL", "XXXXXL", "5XL",
                "XXXXXXL", "6XL"].filter(x => new Set(size_cloth).has(x))
            }
          })
        });

        return res
      },

      productVariantAttributes() {
        let res = {};
        this.$props.product.product_variants.forEach(variant => {
          variant.attributes.forEach(attr => {
            if (!res[attr.name]) {
              res[attr.name] = []
            }
            res[attr.name].push(attr.value);
          })
        });

        return res
      },

      decorations() {
        return this.selectedVariant ? this.selectedVariant.decorations : []
      },

      selectedVariant() {
        this.recompute; // recomputation hack. Do not remove !
        let selectedProductVariant = null;
        this.product.product_variants.forEach(pv => {
          let suitable = true;
          pv.attributes.forEach(attr => {
            if (this.selectedAttributes[attr.name] !== attr.value)
              suitable = false
          });
          if (suitable)
            selectedProductVariant = pv
        });
        return selectedProductVariant
      },
      selectedVariants() {
        this.recompute; // recomputation hack. Do not remove !
        let filteredVariants = this.$props.product.product_variants;
        Object.keys(this.$data.selectedAttributes).forEach(attrName => {
          if (!this.$data.selectedAttributes[attrName])
            return;
          filteredVariants = filteredVariants.filter(pv => {
            let attrs = {};
            pv.attributes.forEach(attr => {
              attrs[attr.name] = attr.value
            });
            return attrs[attrName] == this.$data.selectedAttributes[attrName]
          })
        });
        return filteredVariants
      },

      selectedVariantPrice() {
        this.recompute; // recomputation hack. Do not remove !
        // Pass if not selected
        if (!this.selectedVariant)
          return 0;
        // Calculate total
        let total = this.selectedVariant.vendor_cost +
          this.bflCost +
          this.owCost;
        this.selectedVariant.decorations.forEach(x => total += x.decoration_cost);
        // Determine divider
        let divider = (1 - (this.selectedVariant.margin / 100));
        return total / divider
      }
    },

    methods: {

      removeProduct() {
        // Emit removal of product
        this.$emit(
          'remove-product',
          this.$props.product,
        )
      },

      removeProductVariant() {
        // Raise error if variant is not selected
        if (!this.selectedVariant) {
          this.$store.dispatch('raiseError', 'Variant is not selected');
          return
        }
        // Emit removal of product variant
        this.$emit(
          'remove-product-variant',
          this.$props.index,
          this.$props.product.product_variants.indexOf(this.selectedVariant))
      },

      editProduct() {
        this.$emit('edit-product', this.$props.index)
      },

      uploadProductImage() {
        this.$emit('upload-product-image', this.$props.index)
      },

      uploadProductVariantImage() {
        if (!this.selectedVariants) {
          this.$store.dispatch('raiseError', 'No variants available');
          return
        }
        let pvIndexes = [];
        this.selectedVariants.forEach(pv => {
          pvIndexes.push(
            this.$props.product.product_variants.indexOf(pv))
        });
        this.$emit(
          'upload-product-variants-image',
          this.$props.index,
          pvIndexes)
      }
    },
  }
</script>


<style scoped>
  .product-card__img >>> .v-responsive__sizer {
    padding-bottom: 100% !important;
  }

  .v-btn {
    min-width: 0px;
    width: 100%;
  }

  .v-menu {
    width: 100%;
  }

  .remove-button {
  }
</style>
