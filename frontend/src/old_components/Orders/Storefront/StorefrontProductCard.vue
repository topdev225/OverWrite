<template>
  <v-card class="elevation-3 pcard" data-cy="ProductCard">
    <div>{{images.length}}</div>
    <div class="text-xs-center">
      <!-- <img :src=image height="270"/> -->

      <v-carousel
        class="elevation-0"
        height="270"
        light
        hide-delimiters
        :cycle="false"
        :hide-controls="Object.keys(images).length == 1"
        v-model="slideIndex"
      >
        <v-carousel-item
          height="270"
          v-for="(image, index) in images"
          :key="index"
          :src="image"
        ></v-carousel-item>
      </v-carousel>
    </div>


    <div class="title text-xs-center mt-3">{{ $props.product.name }}</div>

    <div class="attrs">
      <v-form
        ref="form"
        v-model="valid">
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
        <v-text-field
          label="quantity"
          :rules="[validateInteger]"
          type="number"
          step="1"
          min="0"
          v-model.number="quantity"></v-text-field>
      </v-form>
    </div>


    <div class="text-xs-center headline mb-2 price">
      <span v-if="price">${{ price }}</span>
    </div>

    <v-spacer></v-spacer>

    <v-card-actions>
      <v-btn
        block
        large
        @click="addToCart"
        color="primary"
        :disabled="!selectedVariant || !valid || !parseInt(quantity)">add to cart
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>
  import rules from '@/mixins/rules';
  import productVariantSetsMixin from '@/mixins/productVariantSets';

  export default {
    props: [
      'product'
    ],

    mixins: [
      rules,
      productVariantSetsMixin,
    ],

    data() {
      return {
        valid: null,
        carouselIndex: 0,

        selectedAttributes: {},
        quantity: 1,
      }
    },
    computed: {

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
        else if (this.$props.product.resources[0]) {
          return `${process.env.API_BASE_URL}` +
            `/static` +
            `/resources` +
            `/${this.$props.product.resources[0].uuid}` +
            `.${this.$props.product.resources[0].type}`
        }
        // Fallback
        else {
          return `${process.env.API_BASE_URL}/static/default-product.svg`
        }
      },
      slideIndex() {
        // Selected variant
        if (this.selectedVariant && this.selectedVariant.resources[0]) {
          return this.selectedVariant.resources[0].meta.pvsIndex
        }
        // Not complete attributes selection
        // (only in case of pv image is exist)
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
        if (Object.keys(this.selectedAttributes).length && pvs[0] && pvs[0].resources[0]) {
          return pvs[0].resources[0].meta.pvsIndex
        }
        // Default product image
        if (this.product.resources[0]) {
          let hash = this.product.resources[0].hash;
          let index = 0;
          this.product.product_variants.forEach(pv => {
            if (pv.resources[0] && pv.resources[0].hash === hash)
              index = pv.resources[0].meta.pvsIndex
          });
          return index
        }
        return 0
      },
      images() {     // {groupIndex: link}
        let images = {};
        this.product.product_variants.forEach(pv => {
          if (pv.resources.length && !Object.keys(images).includes(pv.resources[0].meta.pvsIndex)) {
            images[pv.resources[0].meta.pvsIndex] = this.getImgUrl(pv.resources[0])

          }
        });


        if (Object.keys(images).length == 0) {
          if (this.$props.product.resources && this.$props.product.resources[0]) {
            images[0] = `${process.env.API_BASE_URL}` +
              `/static` +
              `/resources` +
              `/${this.$props.product.resources[0].uuid}` +
              `.${this.$props.product.resources[0].type}`
          }
        }
        if (Object.keys(images).length == 0) {
          images[0] = `${process.env.API_BASE_URL}/static/default-product.svg`
        }
        return images
      },

      // fast check, need refactor later
      attributesWithSizes() {
        let res = {
          ...this.$props.product.attributes,
        };
        if (!!res['size']) {
          res['size'] = ["XXS", "XS", "S", "SM", "M", "MD", "L", "LG", "XL", "XXL", "2XL",
            "XXXL", "3XL", "XXXXL", "4XL", "XXXXXL", "5XL",
            "XXXXXXL", "6XL"].filter(x => new Set(res['size']).has(x))
        }
        if (!!res['Size']) {
          res['Size'] = ["XXS", "XS", "S", "SM", "M", "MD", "L", "LG", "XL", "XXL", "2XL",
            "XXXL", "3XL", "XXXXL", "4XL", "XXXXXL", "5XL",
            "XXXXXXL", "6XL"].filter(x => new Set(res['Size']).has(x))
        }
        if (!!res['SIZE']) {
          res['SIZE'] = ["XXS", "XS", "S", "SM", "M", "MD", "L", "LG", "XL", "XXL", "2XL",
            "XXXL", "3XL", "XXXXL", "4XL", "XXXXXL", "5XL",
            "XXXXXXL", "6XL"].filter(x => new Set(res['SIZE']).has(x))
        }

        return res;
      },

      decorations() {
        return this.selectedVariant ? this.selectedVariant.decorations : (this.product.product_variants[0].decorations || [])
      },

      selectedVariant() {
        this.recompute; // recomputation hack. Do not remove !
        const selectedAttr = this.$data.selectedAttributes;
        let selectedProductVariant = null;
        this.$props.product.product_variants.forEach(pv => {
          let suitable = true;
          pv.attributes.forEach(attr => {
            if (this.$data.selectedAttributes[attr.name] !== attr.value) {
              suitable = false;
            }
          });
          if (suitable)
            selectedProductVariant = pv
        });
        return selectedProductVariant
      },

      price() {
        if (!this.$store.state.account.campaign.storefront_pricing) {
          return null;
        }
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
        let pv = this.selectedVariant ||
          pvs[0];
        return pv ? (pv.price * (this.quantity || 0)).toFixed(2) : 0
      }
    },

    methods: {

      getImgUrl(resource) {
        return `${process.env.API_BASE_URL}` +
          `/static` +
          `/resources` +
          `/${resource.uuid}` +
          `.${resource.type}`
      },
      addToCart() {
        const cart = JSON.parse(localStorage.getItem('cartProducts'));
        const prodObj = {};
        let quantity = parseInt(this.quantity);
        if (cart && cart[this.selectedVariant.id]) {
          const variantCountAlreadyInCart = parseInt(cart[this.selectedVariant.id]);
          quantity += variantCountAlreadyInCart;
        }
        prodObj[this.selectedVariant.id] = parseInt(quantity);
        this.$emit('add-product', prodObj);
        this.$data.selectedAttributes = {};
        this.$data.quantity = 1;
        this.initDefaultSelectedAttributes();
        this.$store.dispatch('raiseSuccess', 'Cart has been updated');
      }
    }
  }
</script>


<style scoped>
  .pcard {
    position: relative;
    min-height: 545px;
  }

  .pcard .title {
    min-height: 50px;
  }

  .pcard div {
    position: relative;
  }

  .pcard >>> .v-image__image {
    background-size: contain !important;
  }

  .pcard .attrs {
    padding-left: 8px;
    padding-right: 8px;
  }

  .pcard .price {
    padding-bottom: 65px;
  }

  .pcard >>> .v-card__actions {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
  }
</style>
