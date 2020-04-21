<template>
  <v-layout justify-center>
    <v-flex xs10 mt-4 mb-4>
      <v-card>
        <v-form ref="form" lazy-validation @submit.prevent="submitHandler">
          <v-card-title
            class="headline primary white--text"
            primary-title>
            {{$route.params.id ? 'Update' : 'Create' }} Distributor
          </v-card-title>

          <v-progress-linear
          :active="distributorPending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

          <v-card-text v-if="!distributorPending">
            <v-text-field
              v-model="distributor.name"
              label="Distributor Name *"
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <v-text-field
              v-model="distributor.email"
              label="Billing email *"
              :rules="[validateNotEmpty, validateEmail]">
            </v-text-field>
            <v-text-field
              v-model="distributor.address"
              label="Physical address *"
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <v-container fluid grid-list-lg class="pa-0">
              <v-layout row wrap>
                <v-flex lg4>
                  <v-text-field
                    v-model.number="distributor.ow_cost"
                    label="Monthly Order Write fee ($)"
                    type="number"
                    suffix="$"
                  ></v-text-field>
                </v-flex>
                <v-flex lg4>
                  <v-text-field
                    v-model.number="distributor.campaign_cost"
                    label="Campaign % rate"
                    type="number"
                    suffix="%"
                  ></v-text-field>
                </v-flex>
                <v-flex lg4>
                  <v-text-field
                    v-model.number="distributor.transaction_cost"
                    label="Transaction fee"
                    type="number"
                    suffix="$"
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
            <v-text-field
              v-if="$store.getters.isSuperAdmin"
              v-model.number="distributor.max_sales_count"
              label="Max sales executives *"
              type="number"
              :rules="[validateNotEmpty, validateMin(1), validateMax(1000)]"
            ></v-text-field>

            <div>
              <v-autocomplete
                v-model="selectedProductTypes"
                :items="possibleProductTypes"
                chips
                deletable-chips
                clearable
                label="Product types specific to this distributor *"
                :readonly="!hasAccess"
                @focus="loadProductTypes()"
                return-object
                :rules="[validateCount(1)]"
                validate-on-blur
                item-text="name"
                item-value="_jv.id"
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
              @click="$router.push('/admin/distributors')"
              :disabled="distributorPending"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="$route.params.id && hasAccess"
              @click="deleteDialogOpened = true"
              color="error"
              class="flex-grow-0"
              :disabled="distributorPending"
            >
              Delete
            </v-btn>
            <v-btn
              v-if="hasAccess"
              @click="submitHandler(redirectToAccounts)"
              color="primary"
              outline
              class="flex-grow-0"
              :disabled="distributorPending"
            >
              {{$route.params.id ? 'Update' : 'Create'}} and add users
            </v-btn>
            <v-btn
              v-if="hasAccess"
              type="submit"
              color="primary"
              class="flex-grow-0"
              :disabled="distributorPending"
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
                Delete
              </v-card-title>

              <v-card-text>
                <div class="title" style="line-height:1.4 !important">
                  <p class="mt-2 mb-3">
                    Do you really want to delete <strong>"{{distributor.name || ''}}"?</strong>
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
                  @click="deleteDistributor()"
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

  export default {
    data() {
      return {
        distributor: {
          id: this.$route.params.id,
          name: '',
          email: '',
          address: '',
          ow_cost: 0,
          campaign_cost: 0,
          transaction_cost: 0,
          max_sales_count: 1000,
          product_types: {},
          _jv: {
            type: 'Distributor',
          }
        },

        selectedProductTypes: [],
        possibleProductTypes: [],

        distributorPending: true,
        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    computed: {
      hasAccess() {
        let allowedRoles = [];

        if (this.$route.params.id) {
          // has edit access
          allowedRoles = ['Super Admin'];
        } else {
          // has create access
          allowedRoles = ['Super Admin', 'Distributor Manager'];
        }

        const currentRole = this.$store.state.account.role.name;

        return currentRole && !!~allowedRoles.indexOf(currentRole);
      },

      endAction() {
        return () => this.$router.push(`/admin/distributors/`);
      }
    },

    mixins: [
      rules,
    ],

    async mounted() {
      await this.loadProductTypes();

      if (this.$route.params.id) {
        this.loadDistributor();
      } else {
        this.distributorPending = false;
      }
    },

    methods: {
      async loadDistributor() {
        this.distributorPending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `/distributors/${this.$route.params.id}`,
            {params: {include: 'product_types'}}
          ]
        ).then((distributor) => {
          // convert list of product types from an object into a list (that Vue expects). they have
          // to be literally the same objects as in possibleProductTypes in order for pre-selection
          // in the multi-select dropdown to work.
          let selectedProductTypeIds = Object.values(distributor.product_types).map(obj => obj._jv.id);

          this.selectedProductTypes = Object.values(this.possibleProductTypes).filter(
            obj => selectedProductTypeIds.indexOf(obj._jv.id) > -1
          );

          this.distributor = distributor;
        }).catch(err => {
          console.error(err);
        });

        this.distributorPending = false;
      },

      async submitHandler(callback) {
        if (this.$refs.form.validate()) {
          // first, either create or update the model
          if (this.$route.params.id) {
            await this.$store.dispatch(
              'jv/patch', this.distributor
            ).then(distributor => {
              this.distributor = distributor;
              this.updateProductTypes('updated', callback);
            }).catch(err => {
              console.error(err);
            });
          } else {
            await this.$store.dispatch(
              'jv/post', [this.distributor, {url: '/distributors'}]
            ).then(distributor => {
              this.distributor = distributor;
              this.updateProductTypes('created', callback);
            }).catch(err => {
              console.error(err);
            });
          }
        }
      },

      async updateProductTypes(actionVerb, callback) {
        // then, update the product type relationship in a separate call. convert list of selected
        // product types into a list of resource identifiers
        let listOfIdentifers = this.selectedProductTypes.map(obj => {
          return {id: obj._jv.id, type: obj._jv.type};
        });

        await this.$axios.patch(
          `/distributors/${this.distributor._jv.id}/product_types`,
          { data: listOfIdentifers },
        ).then(resp => {
          this.$store.dispatch('raiseSuccess', `Distributor ${this.distributor._jv.id} ${actionVerb}`);
          this.endAction();
          callback && callback();
        }).catch(err => {
          console.error(err);
        });
      },

      async loadProductTypes() {
        await this.$store.dispatch('jv/get', 'product_types').then((productTypes) => {
          this.possibleProductTypes = Object.values(productTypes);
        }).catch(err => {
          console.error(err);
        });
      },

      async deleteDistributor() {
        this.deleteDialogPending = true;

        await this.$store.dispatch('jv/delete', this.distributor).then(resp => {
          this.$store.dispatch('raiseSuccess', `Distributor ${this.distributor._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });

        this.deleteDialogPending = false;
      },

      redirectToAccounts() {
        this.$router.push(`/admin/accounts/add?distributor_id=${this.distributor._jv.id}`);
      }
    }
  }
</script>
