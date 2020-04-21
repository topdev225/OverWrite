<template>
  <v-layout justify-center>
    <v-flex xs10 mt-4>
      <v-card>
        <v-card-title class="primary white--text">
          <div>
            <h3 class="headline">
              <span>{{ $route.params.id ? 'Update' : 'Add' }} Vendor</span>
            </h3>
          </div>
        </v-card-title>

        <v-progress-linear
          :active="vendorPending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

        <v-form ref="form" @submit.prevent="submitHandler">
          <v-card-text v-if="!vendorPending">
            <v-text-field
              v-model="vendor.name"
              label="Name *"
              :readonly="!hasAccess"
              required
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <v-text-field
              v-model="vendor.email"
              label="Email *"
              :readonly="!hasAccess"
              required
              :rules="[validateNotEmpty, validateEmail]"
            ></v-text-field>
            <v-text-field
              v-model="vendor.address"
              label="Address *"
              :readonly="!hasAccess"
              required
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <div class="mb-3">Vendor is a:</div>
            <div class="d-flex flex-wrap">
              <v-switch
                v-model="vendor.is_supplier"
                label="Supplier"
                :readonly="!hasAccess"
                class="flex-grow-0 mr-4"
                :rules="[vendorIsCheck]"
              ></v-switch>
              <v-switch
                v-model="vendor.is_decorator"
                label="Decorator"
                :readonly="!hasAccess"
                class="flex-grow-0 mr-4"
                :rules="[vendorIsCheck]"
              ></v-switch>
              <div v-if="$store.getters.isSuperAdmin" class="mb-3">
                <v-switch
                  v-model="vendor.is_pick_pack"
                  label="Pick pack partner"
                  :readonly="!hasAccess"
                  :rules="[vendorIsCheck]"
                ></v-switch>
              </div>
            </div>
            <div>
              <v-autocomplete
                v-model="selectedProductTypes"
                :items="possibleProductTypes"
                auto-select-first
                chips
                deletable-chips
                clearable
                label="Product types specific to vendor *"
                :readonly="!hasAccess"
                @focus="loadProductTypes()"
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

          <v-card-actions class="d-flex justify-end">
            <v-btn
              class="flex-grow-0"
              @click="$router.push('/admin/vendors')"
              :disabled="vendorPending"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="$route.params.id && hasAccess"
              @click="deleteDialogOpened = true"
              color="error"
              class="flex-grow-0"
              :disabled="vendorPending"
            >
              Delete
            </v-btn>
            <v-btn
              v-if="hasAccess"
              type="submit"
              color="primary"
              class="flex-grow-0"
              :disabled="vendorPending"
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
                Delete vendor
              </v-card-title>

              <v-card-text>
                <div class="title" style="line-height:1.4 !important">
                  <p class="mt-2 mb-3">
                    Do you really want to delete vendor <strong>"{{vendor.name || ''}}"?</strong>
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
                  @click="deleteVendor(vendor.id)"
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
  import rules from '@/mixins/rules'
  import axios from '@/axios'
  import Vendor from "../../models/Vendor";

  export default {
    mixins: [
      rules
    ],

    data() {
      return {
        vendor: Vendor.generateEmpty(),
        formIsValid: false,

        selectedProductTypes: [],
        possibleProductTypes: [],

        vendorPending: true,
        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    async mounted() {
      if (this.$route.params.id) {
        await this.loadProductTypes();
        this.loadVendor();
      } else {
        this.vendorPending = false;
      }
    },

    computed: {
      vendorIsCheck() {
        return ~[this.vendor.is_supplier, this.vendor.is_decorator, this.vendor.is_pick_pack].indexOf(true) ? false : 'Please select one';
      },

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
        return () => this.$router.push(`/admin/vendors/`);
      }
    },

    methods: {
      async loadVendor() {
        this.vendorPending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `/vendors/${this.$route.params.id}`,
            {params: {include: 'product_types'}}
          ]
        ).then((vendor) => {
          // convert list of product types from an object into a list (that Vue expects). they have
          // to be literally the same objects as in possibleProductTypes in order for pre-selection
          // in the multi-select dropdown to work.
          let selectedProductTypeIds = Object.values(vendor.product_types).map(obj => obj._jv.id);

          this.selectedProductTypes = Object.values(this.possibleProductTypes).filter(
            obj => selectedProductTypeIds.indexOf(obj._jv.id) > -1
          );

          this.vendor = vendor;
        }).catch(err => {
          console.error(err);
        });

        this.vendorPending = false;
      },

      async loadProductTypes() {
        await this.$store.dispatch('jv/get', 'product_types').then((productTypes) => {
          this.possibleProductTypes = Object.values(productTypes);
        }).catch(err => {
          console.error(err);
        });
      },

      async submitHandler() {
        if (this.$refs.form.validate()) {
          // first, either create or update the model
          if (this.$route.params.id) {
            await this.$store.dispatch(
              'jv/patch', this.vendor
            ).then(vendor => {
              this.vendor = vendor;
              this.updateProductTypes('updated');
            }).catch(err => {
              console.error(err);
            });
          } else {
            await this.$store.dispatch(
              'jv/post', [this.vendor, {url: '/vendors'}]
            ).then(vendor => {
              this.vendor = vendor;
              this.updateProductTypes('created');
            }).catch(err => {
              console.error(err);
            });
          }
        }
      },

      async updateProductTypes(actionVerb) {
        // then, update the product type relationship in a separate call. convert list of selected
        // product types into a list of resource identifiers
        let listOfIdentifers = this.selectedProductTypes.map(obj => {
          return {id: obj._jv.id, type: obj._jv.type};
        });

        await this.$axios.patch(
          `/vendors/${this.vendor._jv.id}/product_types`,
          { data: listOfIdentifers },
        ).then(resp => {
          this.$store.dispatch('raiseSuccess', `Vendor ${this.vendor._jv.id} ${actionVerb}`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });
      },

      async deleteVendor() {
        this.deleteDialogPending = true;

        await this.$store.dispatch('jv/delete', this.vendor).then(resp => {
          this.$store.dispatch('raiseSuccess', `Vendor ${this.vendor._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });

        this.deleteDialogPending = false;
      }
    }
  }
</script>
