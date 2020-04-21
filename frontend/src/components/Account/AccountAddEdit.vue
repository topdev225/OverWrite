<template>
  <v-layout justify-center>
    <v-flex :class="!componentMode ? 'xs10 mt-4 mb-4' : ''">
      <v-card>
        <v-card-title class="primary white--text">
          <div>
            <h3 class="headline">{{ pageTitle }}</h3>
          </div>
        </v-card-title>

        <v-progress-linear
          :active="accountPending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

        <v-form ref="form" lazy-validation @submit.prevent="submit">
          <v-card-text v-if="!accountPending">
            <v-text-field
              v-model="account.username"
              label="Username *"
              browser-autocomplete="new-password"
              :rules="[validateNotEmpty, validateUsername]"
            ></v-text-field>
            <v-text-field
              v-model="account.password"
              label="Password *"
              type="password"
              browser-autocomplete="new-password"
            ></v-text-field>
            <v-text-field
              v-model="account.email"
              label="Email *"
              browser-autocomplete="new-password"
              type="email"
              :rules="[validateNotEmpty, validateEmail]"
            ></v-text-field>
            <v-text-field
              v-model="account.first_name"
              label="First Name *"
              browser-autocomplete="new-password"
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <v-text-field
              v-model="account.last_name"
              label="Last Name *"
              browser-autocomplete="new-password"
              :rules="[validateNotEmpty]"
            ></v-text-field>
            <v-autocomplete
              v-model="account.role_id"
              :items="allowedRoles ? allowedRoles : possibleRoles"
              :loading="possibleRolesPending"
              label="Role *"
              browser-autocomplete="new-password"
              :rules="[validateNotEmpty]"
              item-text="name"
              item-value="_jv.id"
              validate-on-blur
            />
            <v-select
              v-if="!!~['Distributor Manager', 'Sales Executive'].indexOf(account.role.name)"
              v-model="account.distributor_id"
              :items="possibleDistributors"
              :loading="possibleDistributorsPending"
              label="Distributor *"
              browser-autocomplete="new-password"
              :clearable="true"
              @focus="loadDistributors"
              item-text="name"
              item-value="_jv.id"
              :rules="[validateNotEmpty]"
            ></v-select>
            <v-select
              v-if="!!~['Admin Buyer', 'Shopper'].indexOf(account.role.name)"
              v-model="account.campaign_id"
              :items="possibleCampaigns"
              :loading="possibleCampaignsPending"
              label="Campaign *"
              browser-autocomplete="new-password"
              :clearable="true"
              item-text="name"
              item-value="_jv.id"
              :rules="[validateNotEmpty]"
            ></v-select>
            <v-switch
              label="Active"
              v-model="account.active"
              :rules="[validateNotEmptyCheckbox]"
            >
            </v-switch>
          </v-card-text>
          <v-card-actions class="d-flex justify-end">
            <v-btn
              class="flex-grow-0"
              @click="endAction"
              :disabled="accountPending"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="editMode && account.role.name !== 'Super Admin'"
              @click="remove"
              color="error"
              class="flex-grow-0"
              :disabled="accountPending"
            >
              Delete
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
              class="flex-grow-0"
              :disabled="accountPending"
            >
              {{ editMode ? 'Update' : 'Create' }}
            </v-btn>
          </v-card-actions>
        </v-form>

      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>
  import rules from '@/mixins/rules';
  import Account from '@/models/Account';

  export default {
    data() {
      return {
        account: Account.generateEmpty(),

        accountPending: true,

        possibleRoles: [],
        possibleRolesPending: true,
        possibleDistributors: [],
        possibleDistributorsPending: true,
        possibleCampaigns: [],
        possibleCampaignsPending: true,
      }
    },

    mixins: [
      rules,
    ],

    props: {
      componentMode: {
        type: Boolean,
        required: false,
      },
      accountId: {
        type: Number,
        required: false,
      },
      successCallback: {
        type: Function,
        required: false,
      },
      allowedRoles: {
        type: Array,
        required: false,
      }
    },

    async mounted() {
      if (this.editMode) {
        this.loadAccount().then(() => {
          this.$refs.form.resetValidation();
        });
      }

      const promises = [this.loadDistributors(), this.loadRoles(), this.loadCampaigns()];

      if (!this.editMode) {
        this.accountPending = false;
      }

      await Promise.all(promises);
    },

    computed: {
      editMode() {
        return !!this.currentAccountId;
      },

      pageTitle() {
        let title = 'Create Account';

        if (this.editMode) {
          title = 'Update Account';

          if (this.account && this.account._jv.id) {
            title = `${title} (${this.account._jv.id})`;
          }
        }

        return title;
      },

      currentAccountId() {
        return this.componentMode ? this.accountId : this.$route.params.id;
      },

      endAction() {
        if (this.componentMode && this.successCallback) {
          return this.successCallback;
        } else {
          return () => this.$router.push('/admin/accounts');
        }
      }
    },

    methods: {
      async loadAccount() {
        this.accountPending = true;

        await this.$store.dispatch(
          'jv/get',
          [`/accounts/${this.currentAccountId}`, {params: {include: 'distributor,role'}}]
        ).then(account => {
          this.account = account;
        }).catch(err => {
          console.error(err);
        });

        this.accountPending = false;
      },

      async loadRoles() {
        this.possibleRolesPending = true;

        await this.$store.dispatch('jv/get', 'roles').then(roles => {
          this.possibleRoles = Object.values(roles);

          if (!this.$store.getters.isSuperAdmin) {
            const currentUserRole = (
              this.$store.state.account.role.name || localStorage.getItem('roleName')
            );

            if (currentUserRole === 'Distributor Manager') {
              this.possibleRoles = this.possibleRoles.filter(
                role => !!~['Sales Executive', 'Admin Buyer', 'Shopper'].indexOf(role.name)
              );
            } else if (currentUserRole === 'Sales Executive') {
              this.possibleRoles = this.possibleRoles.filter(
                role => !!~['Admin Buyer', 'Shopper'].indexOf(role.name)
              );
            } else {
              // don't let the user select any roles if we can't determine their permissions
              this.$store.dispatch('raiseError', 'Could not determine permissions of current user');
              this.possibleRoles = [];
            }
          }
        }).catch(err => {
          console.error(err);
        });

        this.possibleRolesPending = false;
      },

      async loadDistributors() {
        this.possibleDistributorsPending = true;

        await this.$store.dispatch('jv/get', 'distributors').then(distributors => {
          this.possibleDistributors = Object.values(distributors);
        }).catch(err => {
          console.error(err);
        });

        this.possibleDistributorsPending = false;
      },

      async loadCampaigns() {
        this.possibleCampaignsPending = true;

        await this.$store.dispatch('jv/get', 'campaigns').then(campaigns => {
          this.possibleCampaigns = Object.values(campaigns);
        }).catch(err => {
          console.error(err);
        });

        this.possibleCampaignsPending = false;
      },

      async submit() {
        if (this.$refs.form.validate()) {
          if (this.currentAccountId) {
            await this.$store.dispatch('jv/patch', this.account).then(resp => {
              this.$store.dispatch('raiseSuccess', `Account ${this.account._jv.id} updated`);
              this.endAction();
            }).catch(err => {
              console.error(err);
            });
          } else {
            await this.$store.dispatch(
              'jv/post', [this.account, {url: '/accounts'}]
            ).then(account => {
              this.$store.dispatch('raiseSuccess', `Account ${account._jv.id} created`);
              this.endAction();
            }).catch(err => {
              console.error(err);
            });
          }
        }
      },

      async remove() {
        await this.$store.dispatch('jv/delete', this.account).then(resp => {
          this.$store.dispatch('raiseSuccess', `Account ${this.account._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });
      }
    }
  }
</script>
