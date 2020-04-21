<template>
  <v-layout justify-center>
    <v-flex xs10 mt-4 mb-4>
      <v-card>
        <v-card-title class="primary white--text">
          <div>
            <h3 class="headline">
              <span>{{ $route.params.id ? 'Edit' : 'Create' }} Product Type</span>
            </h3>
          </div>
        </v-card-title>

        <v-progress-linear
          :active="productTypePending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

        <v-form ref="form" @submit.prevent="submitHandler">
          <v-card-text v-if="!productTypePending">
            <v-text-field
              v-model="productType.name"
              label="Name *"
              :rules="[validateNotEmpty]"
              :readonly="!$store.getters.isSuperAdmin"
              data-cy="ProductTypeName"
            />

            <div>
              <v-autocomplete
                v-model="selectedAttributes"
                :items="possibleAttributes"
                auto-select-first
                chips
                deletable-chips
                clearable
                label="Attributes associated with this product type *"
                @focus="loadAttributes()"
                :rules="[validateCount(1)]"
                validate-on-blur
                item-text="name"
                item-value="_jv.id"
                return-object
                multiple
              >
                <template slot="selection" slot-scope="data">
                  {{ data.item.name }}
                </template>
                <template slot="item" slot-scope="data">
                  {{ data.item.name }}
                </template>
              </v-autocomplete>
            </div>
          </v-card-text>

          <v-card-actions class="justify-end">
            <div class="d-flex justify-end">
              <v-btn
                class="grow-0" @click="$router.push('/admin/product_types')"
                data-cy="goToProductTypesWithoutSavingButton"
              >
                Cancel
              </v-btn>
              <v-btn
                v-if="productType._jv.id"
                @click="deleteDialogOpened = true"
                color="error"
                class="grow-0"
              >
                Delete
              </v-btn>
              <v-btn
                v-if="$store.getters.isSuperAdmin"
                type="submit"
                color="primary"
                class="grow-0"
                data-cy="createProductTypeButton"
              >
                {{ $route.params.id ? 'Update' : 'Create' }}
              </v-btn>
            </div>
          </v-card-actions>
        </v-form>
      </v-card>

      <template>
        <v-layout row justify-center>
          <v-dialog
            v-model="deleteDialogOpened"
            max-width="800"
          >
            <v-card>
              <v-card-title
                class="headline error white--text"
                primary-title>
                Delete Product Type
              </v-card-title>

              <v-card-text>
                <div class="title" style="line-height:1.4 !important">
                  <p class="mt-2 mb-3">
                    Do you really want to delete <strong>"{{productType.name || ''}}"?</strong>
                  </p>
                </div>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="py-3 px-3">
                <v-spacer></v-spacer>
                <v-btn
                  outline
                  color="error"
                  @click="deleteDialogOpened = false"
                >
                  cancel
                </v-btn>
                <v-btn
                  :loading="deleteDialogPending"
                  :disabled="deleteDialogPending"
                  color="error"
                  @click="deleteProductType()"
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
    </v-flex>
  </v-layout>
</template>

<script>
  import rules from '@/mixins/rules';
  import ProductType from '@/models/ProductType';
  import ProductAttribute from '@/models/ProductAttribute';

  const MAX_ATTRIBUTES_PER_PRODUCT_TYPE = 2;

  export default {
    data() {
      return {
        step: this.$route.query.step || 1,

        productType: ProductType.generateEmpty(),
        productTypePending: this.$route.params.id ? true : false,

        attribute: ProductAttribute.generateEmpty(),
        attributes: [],
        attributesPending: true,

        selectedAttributes: [],
        possibleAttributes: [],
        possibleDistributors: [],
        possibleVendors: [],

        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    mixins: [
      rules,
    ],

    async mounted() {
      await this.loadAttributes();

      if (this.$route.params.id) {
        this.loadProductType();
      }
    },

    watch: {
      '$route.query'() {
        if (this.$route.query && this.$route.query.step) {
          this.step = this.$route.query.step;
        }
      }
    },

    methods: {
      endAction() {
        this.$router.push('/admin/product_types/');
      },

      async loadAttributes() {
        await this.$store.dispatch('jv/get', 'product_attributes').then(attributes => {
          this.possibleAttributes = Object.values(attributes);
        }).catch(err => {
          console.error(err);
        });
      },

      async loadProductType(id) {
        this.productTypePending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `product_types/${this.$route.params.id}`,
            {params: {include: 'product_attributes,vendors,distributors'}}
          ]
        ).then(productType => {
          // convert list of attributes from an object into a list (that Vue expects). they have to
          // be literally the same objects as in possibleAttributes in order for pre-selection in
          // the multi-select dropdown to work.
          let selectedAttributeIds = Object.values(productType.product_attributes).map(obj => obj._jv.id);

          this.selectedAttributes = Object.values(this.possibleAttributes).filter(
            obj => selectedAttributeIds.indexOf(obj._jv.id) > -1
          );

          this.productType = productType;
        }).catch(err => {
          console.error(err);
        });

        this.productTypePending = false;
      },

      async submitHandler() {
        if (this.$refs.form.validate()) {
          // first, either create or update the model
          let actionVerb = '';

          if (this.$route.params.id) {
            await this.$store.dispatch(
              'jv/patch', this.productType
            ).then(productType => {
              this.productType = productType;
            }).catch(err => {
              console.error(err);
            });

            actionVerb = 'updated';
          } else {
            await this.$store.dispatch(
              'jv/post', [this.productType, {url: '/product_types'}]
            ).then(productType => {
              this.productType = productType;
            }).catch(err => {
              console.error(err);
            });

            actionVerb = 'created';
          }

          // then, update the product attribute relationship in a separate call. convert list of
          // selected product attributes into a list of resource identifiers
          let listOfIdentifers = this.selectedAttributes.map(obj => {
            return {id: obj._jv.id, type: obj._jv.type};
          });

          await this.$axios.patch(
            `/product_types/${this.productType._jv.id}/product_attributes`,
            { data: listOfIdentifers },
          ).then(resp => {
            this.$store.dispatch('raiseSuccess', `Attribute ${this.productType._jv.id} ${actionVerb}`);
            this.endAction();
          }).catch(err => {
            console.error(err);
          });
        }
      },

      async deleteProductType() {
        this.deleteDialogPending = true;

        await this.$store.dispatch('jv/delete', this.productType).then(resp => {
          this.$store.dispatch('raiseSuccess', `Product type ${this.productType._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });

        this.deleteDialogPending = false;
      },
    }
  }
</script>
