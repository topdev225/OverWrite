import Vue from 'vue';

export default {
  created() {
    this.initDefaultSelectedAttributes();
  },
  data() {
    return {
      recompute: '',
    };
  },
  computed: {
    productMajorAttributeIndex() {
      const pr = this.$props.product;
      if (!pr || !pr.id || !pr.product_variants.length) return -1;
      const attrWithColorIndex = pr.product_variants[0].attributes.findIndex(attr => ~attr.name.toLowerCase().indexOf('color'));
      if(~attrWithColorIndex) {
        return attrWithColorIndex;
      } else {
        return -1
      }
    },

    productMajorAttribute() {
      const pr = this.$props.product;
      if (!pr || !pr.id || !pr.product_variants.length) {
        return {};
      }
      if(~this.productMajorAttributeIndex) {
        return pr.product_variants[0].attributes[this.productMajorAttributeIndex];
      }
      return {name: this.$props.product && this.$props.product.attributes ? Object.keys(this.$props.product.attributes).sort()[0] : '' };
    },
    productMinorAttribute() {
      const pr = this.$props.product;
      if (!pr || !pr.id || !pr.product_variants.length) {
        return {};
      }
      if(~this.productMajorAttributeIndex) {
        return pr.product_variants[0].attributes[this.productMajorAttributeIndex ? 0 : 1];
      }
      return {name: this.$props.product && this.$props.product.attributes ? Object.keys(this.$props.product.attributes).sort()[1] : '' };
    },
    productAttributeItems() {
      const res = {};
      this.$props.product.product_variants.forEach(variant => {
        const majorAttribute = variant.attributes.find(attr => attr.name === this.productMajorAttribute.name) || variant.attributes[0];
        const minorAttribute = variant.attributes.find(attr => attr.name === this.productMinorAttribute.name) || variant.attributes[1];

        if (!res[majorAttribute.value]) {
          res[majorAttribute.value] = [];
        }

        res[majorAttribute.value].push(minorAttribute.value);
      });
      return res;
    },
  },
  methods: {
    /**
     * Selects first minor item from major: [minor,minor] set on major update
     */
    updateMajor() {
      const major = this.productMajorAttribute.name;
      const minor = this.productMinorAttribute.name;
      /* only if there are minors */
      if (minor) {
        Vue.set(this.selectedAttributes, minor, this.productAttributeItems[this.selectedAttributes[major]][0]);
      }
    },

    /**
     * forces "computed" refresh. Do not remove !
     */
    updateSelectedVariant() {
      this.recompute = Math.random();
    },

    showOptionTitle(value) {
      if (Array.isArray(value)) {
        return value.map(v => {
          try {
            let str = v;
            str = str.replace(/\'/g, '"');
            const parsed = JSON.parse(str);
            return parsed.name ? parsed.name : parsed;
          } catch (e) {
            return v;
          }
        });
      }
      return value;
    },

    initDefaultSelectedAttributes() {
      if (this.product.resources && this.product.resources.length) {
        const {hash} = this.product.resources && this.product.resources.length ? this.product.resources[0] : {};
        const variant = this.product.product_variants.find(v => {
          return v.resources && v.resources.length && v.resources[0].hash === hash;
        });
        const clonedVariantAttributes = JSON.parse(JSON.stringify(variant.attributes));
        this.$data.selectedAttributes = clonedVariantAttributes.reduce((acc, cur) => {
          acc[cur.name] = cur.value;
          return acc;
        }, {});
      } else {
        this.product.product_variants[0].attributes.forEach(attr => {
          Vue.set(this.$data.selectedAttributes, attr.name, attr.value);
        });
      }
    },
  },

  watch: {
    product: {
      handler() {
        this.updateSelectedVariant();
        this.initDefaultSelectedAttributes();
      },
      deep: true,
    },
  }
}
