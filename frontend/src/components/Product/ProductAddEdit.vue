<template>
  <v-layout justify-center>
    <v-flex xs10 mt-4>
      <v-card>
        <v-card-title class="primary white--text">
          <div>
            <h3 class="headline">
              <span>{{ $route.params.id ? 'Update' : 'Add' }} Product</span>
            </h3>
          </div>
        </v-card-title>

        <v-progress-linear
          :active="productPending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

        <v-form ref="form" @submit.prevent="submitHandler" lazy-validation v-if="!productPending">
          <v-card-text>
            <v-text-field
              v-model="product.name"
              label="Name *"
              required
            />
            <v-text-field
              v-model="product.item_number"
              label="Item #"
              required
            />
            <v-select
              v-model="selectedDistributor"
              :items="possibleDistributors"
              :loading="possibleDistributorsPending"
              item-text="name"
              item-value="_jv.id"
              label="Distributor *"
              return-object
            />
            <v-tooltip
              top
              :disabled="!productTypeDisabled"
            >
              <v-select
                slot="activator"
                v-model="selectedProductType"
                :items="possibleProductTypes"
                :loading="possibleProductTypesPending"
                :disabled="productTypeDisabled"
                item-text="name"
                item-value="_jv.id"
                label="Product Type *"
                return-object
              />
              <span>
                Can't change type while variants of this product exist.
              </span>
            </v-tooltip>
          </v-card-text>

          <v-card-actions class="d-flex justify-end">
            <v-btn
              class="flex-grow-0"
              @click="endAction()"
              :disabled="productPending"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="$route.params.id && hasAccess"
              @click="deleteDialogOpened = true"
              color="error"
              class="flex-grow-0"
              :disabled="productPending"
            >
              Delete
            </v-btn>
            <v-btn
              v-if="hasAccess"
              type="submit"
              color="primary"
              class="flex-grow-0"
              :disabled="productPending"
            >
              {{$route.params.id ? 'Update' : 'Create'}}
            </v-btn>
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
                Delete Product
              </v-card-title>

              <v-card-text>
                <div class="title" style="line-height:1.4 !important">
                  <p class="mt-2 mb-3">
                    Do you really want to delete <strong>"{{product.name || ''}}"?</strong>
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
                  Cancel
                </v-btn>
                <v-btn
                  :loading="deleteDialogPending"
                  :disabled="deleteDialogPending"
                  color="error"
                  @click="deleteProduct()"
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
  import Product from "@/models/Product";

  export default {
    data () {
      return {
        product: Product.generateEmpty(),

        selectedProductType: {},
        possibleProductTypes: [],
        possibleProductTypesPending: true,
        productTypeDisabled: false,

        selectedDistributor: {},
        possibleDistributors: [],
        possibleDistributorsPending: true,

        productPending: true,

        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    computed: {
      hasAccess() {
        let allowedRoles = [];

        if (this.$route.params.id) {
          allowedRoles = ['Super Admin'];
        } else {
          allowedRoles = ['Super Admin', 'Distributor Manager'];
        }

        const currentRole = this.$store.state.account.role.name;

        return !!(currentRole && ~allowedRoles.indexOf(currentRole));
      },

      endAction() {
        return () => this.$router.push(`/admin/products`);
      }
    },

    mounted () {
      this.loadProductTypes();
      this.loadDistributors();

      if (this.$route.params.id) {
        this.loadProduct();
      } else {
        this.productPending = false;
      }
    },

    methods: {
      async loadProduct() {
        this.productPending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `/products/${this.$route.params.id}`,
            {params: {include: 'distributor,product_type,product_variants'}}
          ]
        ).then(product => {
          this.product = product;
          this.selectedDistributor = product.distributor;
          this.selectedProductType = product.product_type;

          if (Object.values(product.product_variants).length > 0) {
            this.productTypeDisabled = true;
          }
        }).catch(err => {
          console.error(err);
        });

        this.productPending = false;
      },

      async loadProductTypes() {
        this.possibleProductTypesPending = true;

        await this.$store.dispatch('jv/get', 'product_types').then(productTypes => {
          this.possibleProductTypes = Object.values(productTypes);
        }).catch(err => {
          console.error(err);
        });

        this.possibleProductTypesPending = false;
      },

      async loadDistributors() {
        this.possibleDistributorsPending = true;

        this.$store.dispatch('jv/get', 'distributors').then(distributors => {
          this.possibleDistributors = Object.values(distributors);
        }).catch(err => {
          console.error(err);
        });

        this.possibleDistributorsPending = false;
      },

      async submitHandler() {
        if (this.$refs.form.validate()) {
          // set product_type_id and distributor_id, since we can't set relationships directly
          this.product.product_type_id = this.selectedProductType._jv.id;
          this.product.distributor_id = this.selectedDistributor._jv.id;

          // either create or update the model
          if (this.$route.params.id) {
            await this.$store.dispatch(
              'jv/patch', this.product
            ).then(product => {
              this.product = product;
              this.$store.dispatch('raiseSuccess', `Product ${this.product._jv.id} updated`);
              this.endAction();
            }).catch(err => {
              console.error(err);
            });
          } else {
            await this.$store.dispatch(
              'jv/post', [this.product, {url: '/products'}]
            ).then(product => {
              this.product = product;
              this.$store.dispatch('raiseSuccess', `Product ${this.product._jv.id} created`);
              this.endAction();
            }).catch(err => {
              console.error(err);
            });
          }
        }
      },

      async deleteProduct() {
        this.deleteDialogPending = true;

        await this.$store.dispatch('jv/delete', this.product).then(resp => {
          this.$store.dispatch('raiseSuccess', `Product ${this.product._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });

        this.deleteDialogPending = false;
      }
    }
  }
</script>
