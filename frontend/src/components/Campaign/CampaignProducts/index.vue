<template>
  <v-container grid-list-md>
    <v-layout row wrap align-content-space-around>
      <v-flex xs12>
        <ckeditor
          :editor="editor"
          v-model="campaignMessage"
          :config="editorConfig"
          @ready="prefill"
        >
        </ckeditor>
        <v-layout row wrap>
          <v-flex xs12 md4>
            <v-text-field
              name="name"
              label="B/F/L Cost"
              prefix="$"
              v-model="$store.state.campaign.BFLCost"
              @blur="() => ($store.state.campaign.BFLCost = formatCurrency($store.state.campaign.BFLCost))"
            ></v-text-field>
          </v-flex>
          <v-flex xs12 md4>
            <!-- <v-text-field
              label="OW Cost"
              prefix="$"
              :value="formatCurrency($store.state.campaign.distributor ? $store.state.campaign.distributor.ow_cost: 0)"
              disabled
            ></v-text-field> -->
          </v-flex>
          <v-flex xs12 md4>
            <v-autocomplete
              v-model="$store.state.campaign.vendor_partner_id"
              :items="possiblePickPackPartners"
              :loading="possiblePickPackPartnersPending"
              label="Select Pick, Pack, Partner"
              browser-autocomplete="new-password"
              item-text="name"
              item-value="id"
              @focus="loadVendors"
            />
          </v-flex>
          <v-flex xs12>
                 <v-textarea
                  label="Pick Partner Notes"
                  auto-grow
                  dense
                  v-model="$store.state.campaign.vendor_partner_message"
                  :rows="1"
                  hint="How would you like this order grouped? (i.e. by Location, manager, dept)"
                  >
                </v-textarea>
          </v-flex>
        </v-layout>

      </v-flex>
      <v-flex
        v-for="(product, index) in campaignProducts"
        :key=index
        xs3
        class="d-flex flex-column align-stretch"
      >
        <product-card
          class="flex-grow-1 d-flex flex-column"
          style="flex-direction: column"
          :product="product"
          :index="index"
          :key="product.id"
          @remove-product="openDeleteProductDialog"
          @edit-product="enableProductEditModal"
          @remove-product-variant="removeProductVariant"
          @upload-product-image="uploadProductImage"
          @upload-product-variants-image="uploadProductVariantsImage">
        </product-card>
      </v-flex>
      <v-flex xs3 class="add-container" v-if="!complete">
        <v-btn fab @click="enableProductCreationModal">
          <v-icon>add</v-icon>
        </v-btn>
      </v-flex>
      <v-flex xs12 class="mt-3">
        <product-creation-modal
          ref="productCreationModal"
          :products="products"
          @add-product="addProduct"
          @set-product-default-image="setProductDefaultImage"
          @add-product-variants="addProductVariants">
        </product-creation-modal>
      </v-flex>
      <v-flex xs12>
        <v-card class="mt-3 elevation-3">
          <v-card-title primary-title>
            <div>
              <h3 class="headline mb-2">Checkout Preview</h3>
            </div>
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <!-- Predefined fields -->
            <v-text-field
              v-if="$store.state.campaign.firstNameEnabled"
              label="First Name"
            ></v-text-field>
            <v-text-field
              v-if="$store.state.campaign.lastNameEnabled"
              label="Last Name"
            ></v-text-field>
            <v-text-field
              v-if="$store.state.campaign.companyEmailEnabled"
              label="Company Email"
              :rules="[validateEmail]"
            ></v-text-field>
            <v-select
              v-if="$store.state.campaign.departmentsEnabled && departments.length > 0"
              label="Department"
              :items="departments"
              :item-text="d => d.name"
              return-object
            ></v-select>
            <v-select
              v-if="$store.state.campaign.locationsEnabled && locations.length > 0"
              label="Location"
              :items="locations"
              :item-text="l => l.nickname"
              return-object
            ></v-select>
            <v-select
              v-if="$store.state.campaign.managersEnabled && managers.length > 0"
              label="Manager"
              :items="managers"
              :item-text="m => `${m.first_name} ${m.last_name}`"
              return-object
            ></v-select>

            <!-- Custom fields -->
            <v-text-field
              disabled
              v-if="$parent.$parent.$parent.$parent.$refs.checkoutInfo.$data.checkoutFieldsCustomEnabled"
              v-for="field in $store.state.campaign.customFields"
              :key="field"
              :label="field"
            ></v-text-field>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <image-upload-modal
      title="Product default image"
      ref="productImageUploadModal"
      @save="_uploadProductImage">
    </image-upload-modal>
    <image-upload-modal
      title="Product variant image"
      ref="productVariantsImageUploadModal"
      @save="_uploadProductVariantsImage">
    </image-upload-modal>

    <template>
      <v-layout row justify-center>
        <v-dialog
          v-model="deleteProductDialogOpened"
          max-width="800"
        >
          <v-card>
            <v-card-title
              class="headline error white--text"
              primary-title>
              Delete product
            </v-card-title>

            <v-card-text>
              <div class="title" style="line-height:1.4 !important">
                <p class="mt-2 mb-3">
                  Do you really want to delete product <strong>"{{deleteProductData ?
                  deleteProductData.name : ''}}"?</strong> This operation can't be undone.
                </p>
              </div>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions class="py-3 px-3">
              <v-spacer></v-spacer>
              <v-btn
                outline
                color="error"
                @click="deleteProductDialogOpened = false"
              >
                cancel
              </v-btn>
              <v-btn
                :loading="deleteProductPending"
                :disabled="deleteProductPending"
                color="error"
                @click="removeProduct(deleteProductData)"
              >
                Delete
                <template slot="loader">
                  <span>Saving...</span>
                </template>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-layout>
    </template>

  </v-container>
</template>


<script>

    import axios from '@/axios'

    import ProductCard from './ProductCard'
    import ProductCreationModal from './ProductCreationModal'
    import ImageUploadModal from './ImageUploadModal'

    import rules from '@/mixins/rules'
    import helpers from '@/mixins/helpers'
    import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

    export default {

        props: [
            'campaign'
        ],

        mixins: [
            rules,
            helpers
        ],

        components: {
            'product-card': ProductCard,
            'product-creation-modal': ProductCreationModal,
            'image-upload-modal': ImageUploadModal,
        },

        data() {
            return {
                products: [],
                removedProductPV: [],
                campaignProducts: [],
                campaignMessage: '',
                editor: ClassicEditor,
                editorConfig: {
                    toolbar: ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'undo', 'redo'],
                },

                deleteProductDialogOpened: false,
                deleteProductData: null,
                deleteProductPending: false,
                possiblePickPackPartners: [],
                possiblePickPackPartnersPending: true,
            }
        },

        computed: {
            distributor() {
                return this.$store.state.campaign.distributor
            },

            departments() {
                return this.$parent.$parent.$parent.$parent.$refs.departments.departments
            },
            locations() {
                return this.$parent.$parent.$parent.$parent.$refs.locations.locations
            },
            managers() {
                return this.$parent.$parent.$parent.$parent.$refs.managers.managers
            },
            complete() {
                const {campaign} = this.$parent.$parent.$parent.$parent.$parent._data;
                return campaign && campaign.complete;
            },
        },

        watch: {
            // Reload products list on selected distributor change
            distributor(distributor) {
                if (!distributor) {
                    return
                }
                // Request params
                let fields = 'id,name,item_number,product_type_id,distributor_id,resources'
                let filters = [{'field': 'distributor_id', 'op': '==', 'value': distributor.id}]
                let params = {
                    headers: {
                        'Authorization': this.$store.state.token,
                        'X-Fields': fields,
                        'X-Filters': JSON.stringify(filters)
                    }
                }
                // Get products
                axios.get('/products', params).then(resp => {
                    this.$data.products = resp.data
                })
            },
            '$store.state.campaign.BFLCost'(vcost) {
                // Recalculate margins for products
                this.campaignProducts.forEach((p, pIndex) => {
                    p.product_variants.forEach((pv, pvIndex) => {
                        let total = parseFloat(pv.vendor_cost) +
                            (parseFloat(vcost) || 0) +
                            this.$store.state.campaign.distributor.ow_cost
                        pv.decorations.forEach(x => total += parseFloat(x.decoration_cost))
                        let divider = total / pv.price
                        this.campaignProducts[pIndex].product_variants[pvIndex].margin = (1 - divider) * 100
                    })
                })
            }


        },

        mounted() {
            //this.setContent();
            if (this.$props.campaign) {
                this.$store.state.campaign.BFLCost = this.$props.campaign.bfl_cost;
                this.loadCampaignProducts();
                this.loadVendors();
            }
        },


        methods: {
            prefill(editor) {
                if (this.$props.campaign) {
                    this.campaignMessage = this.$props.campaign.message
                }
            },

            async loadVendors() {
                this.possiblePickPackPartnersPending = true;
                try {
                    const {data} = await this.$axios.get(`/vendors?is_pick_pack=true${this.distributor && this.distributor.related_product_types ? '&product_types=' + this.distributor.related_product_types.map(rpt => rpt.product_type.id) : ''}`);
                    this.possiblePickPackPartners = data;
                } catch (e) {
                    console.error(e);
                }
                this.possiblePickPackPartnersPending = false;
            },

            async loadCampaignProducts() {
                let fields = '*,product_variants{*}';
                let params = {
                    headers: {
                        'Authorization': this.$store.state.token,
                        'X-Fields': fields
                    }
                };
                let url = `/storefront/products?campaign_id=${this.$props.campaign.id}`;
                try {
                    const resp = await axios.get(url, params);
                    this.$data.campaignProducts = resp.data;
                } catch (e) {
                    console.error(e);
                    this.$store.dispatch('raiseError', e);
                }
            },

            // Modals

            enableProductCreationModal() {
                this.$parent.$parent.$parent.$parent.$refs.productCreationModal.enable()
            },

            enableProductEditModal(index) {
                this.$parent.$parent.$parent.$parent.$refs.productCreationModal.enable(
                    this.campaignProducts[index], index
                )
            },

            uploadProductImage(index) {
                this.$refs.productImageUploadModal.enable({'index': index})
            },
            _uploadProductImage(resource, meta) {
                this.$data.campaignProducts[meta.index].resources = [resource]
            },
            uploadProductVariantsImage(pIndex, pvIndexes) {
                this.$refs.productVariantsImageUploadModal.enable({'p': pIndex, 'pvs': pvIndexes})
            },
            _uploadProductVariantsImage(resource, meta) {
                meta.pvs.forEach(pvIndex => {
                    this.$data.campaignProducts[meta.p].product_variants[pvIndex].resources = [resource]
                })
            },

            openDeleteProductDialog(product) {
                this.deleteProductData = product;
                this.deleteProductDialogOpened = true;
            },

            /**
             * Removes product by sending ajax and refetching campaign's data
             * @param {Product} product Some product to remove
             * @returns {Promise<void>}
             */
            async removeProduct(product) {
                this.deleteProductPending = true;
                await this.sendProductData(product, true);
                await this.loadCampaignProducts();
                this.$parent.$parent.$parent.$parent.updateCampaign();
                this.deleteProductPending = false;
                this.deleteProductDialogOpened = false;
                this.deleteProductData = null;
            },

            /**
             * Sends product data. To remove some product_variant you have to send {delete: true} flag.
             * @param {Product} product
             * @param {boolean} forceRemove If true removes all product variants of this product (sets delete: true flag)
             * @returns {Promise<AxiosResponse<Product>|void>}
             */
            async sendProductData(product, forceRemove = false) {
                let params = {headers: {'Authorization': this.$store.state.token}};
                const campaignId = this.campaign.id;
                try {
                    const resp = await axios.put(`/campaigns/${campaignId}/product`, {
                        product: {
                            ...product,
                            product_variants: product.product_variants,
                            ...(forceRemove ? {
                                product_variants: product.product_variants.filter(v => v.id).map(v => ({
                                    id: v.id,
                                    delete: true
                                })),
                            } : {}),
                        },
                    }, params);
                    return resp;
                } catch (e) {
                    console.error(e);
                    this.$store.dispatch('raiseError', e);
                }
            },

            removeProductVariant(productIndex, variantIndex) {
                this.$data.campaignProducts[productIndex].product_variants.splice(variantIndex, 1)
            },

            addProduct(product) {
                this.$data.products.push(product)
            },
            updateProduct(product, index) {
                this.$set(this.products, index, product)
                this.$set(this.campaignProducts, index, product)
            },
            setProductDefaultImage(resource, productName) {
                this.products.forEach((p, i) => {
                    if (p.name == productName)
                        this.$set(this.products[i], 'resources', [resource])
                })
                this.campaignProducts.forEach((p, i) => {
                    if (p.name == productName)
                        this.$set(this.campaignProducts[i], 'resources', [resource])
                })
            },


            addProductVariants({productID, productVariants, removed_variants, all_variants, callback}) {
                const productVariantsRemoved = removed_variants && removed_variants.length ? [...removed_variants] : [];
                // Get product index
                let campaignProductIndex = this.campaignProducts.findIndex(campaignProduct => campaignProduct.id === productID)
                // Add product if not at campaign yet and start again
                if (campaignProductIndex === -1) {
                    let product = Object.assign({}, this.$data.products.filter(x => x.id == productID)[0])
                    product.product_variants = []
                    this.$data.campaignProducts.push(product)
                    this.addProductVariants({productID, productVariants, removed_variants, callback});
                    return
                }

                // Add variants if product already added
                let campaign_pv = this.$data.campaignProducts[campaignProductIndex].product_variants
                for (var i = 0, len = campaign_pv.length; i < len; i++) {
                    for (var j = 0, len2 = productVariants.length; j < len2; j++) {
                        if (!!productVariants[j].attributes && !!campaign_pv[i].attributes && _.isEqual(productVariants[j].attributes, campaign_pv[i].attributes)) {
                            productVariants[j].id = campaign_pv[i].id;
                            let removed_pv_index = removed_variants ? removed_variants.indexOf(productVariants[j].id) : -1;
                            if (removed_pv_index != -1) {
                                removed_variants.splice(removed_pv_index, 1)
                            }
                        }
                    }
                }

                this.$data.campaignProducts[campaignProductIndex].product_variants = productVariants
                // Save
                this.$emit('save', () => {
                    callback();
                    this.loadCampaignProducts();
                }, {
                    id: productID,
                    all_variants,
                    product_variants: [
                        ...productVariants,
                        ...productVariantsRemoved.map(v => ({id: v, delete: true}))
                    ],
                });
            },


        }

    }
</script>


<style scoped>
  .campaign-message {
    font-size: 19px;
    font-weight: 100;
  }

  .campaign-message >>> label {
    font-size: 19px;
    font-weight: 100;
  }

  .add-container {
    height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
