<template>
  <v-container grid-list-xs>
    <v-card class="elevation-3">
      <v-tabs
        v-model="activeTab"
        color="white"
        slider-color="primary"
        :show-arrows="$vuetify.breakpoint.mdAndDown"
      >
        <v-tab :disabled="isSaving" class="m-0">
          Campaign Setup
          <div data-value="0" @click.prevent.stop="nextTab(0)"/>
        </v-tab>
        <v-tab :disabled="isSaving">
          Shopper
          <div data-value="1" @click.prevent.stop="nextTab(1)"/>
        </v-tab>
        <v-tab :disabled="isSaving">
          Admin Buyer
          <div data-value="2" @click.prevent.stop="nextTab(2)"/>
        </v-tab>
        <v-tab :disabled="isSaving">
          Features
          <div data-value="3" @click.prevent.stop="nextTab(3)"/>
        </v-tab>
        <v-tab :disabled="isSaving">
          Checkout Info
          <div data-value="4" @click.prevent.stop="nextTab(4)"/>
        </v-tab>
        <v-tab :disabled="!departmentsEnabled || isSaving">
          Departments
          <div data-value="5" @click.prevent.stop="nextTab(5)"/>
        </v-tab>
        <v-tab :disabled="!locationsEnabled || isSaving">
          Locations
          <div data-value="6" @click.prevent.stop="nextTab(6)"/>
        </v-tab>
        <v-tab :disabled="!managersEnabled || isSaving">
          Managers
          <div data-value="7" @click.prevent.stop="nextTab(7)"/>
        </v-tab>
        <v-tab :disabled="!campaign.distributor || isSaving">
          Products
          <div data-value="8" @click.prevent.stop="nextTab(8)"/>
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="activeTab" v-if="isMounted">
        <v-tab-item :value="0">
          <campaign-setup
            ref="campaignSetup"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item>
        <v-tab-item :value="1">
          <campaign-accounts
            ref="shopper"
            :campaign="campaign"
            :editMode="editMode"
            :targetRole="roles['Shopper']"
            :otherRole="roles['Admin Buyer']"
            :nameDisabled="true"
            :emailDisabled="true"
            :reportsDisabled="true"
          >
            What the shopper will use to login
          </campaign-accounts>
        </v-tab-item>
        <v-tab-item :value="2">
          <campaign-accounts
            ref="adminBuyer"
            :campaign="campaign"
            :editMode="editMode"
            :targetRole="roles['Admin Buyer']"
            :otherRole="roles['Shopper']"
          >
            Purchaser/main point of contact
          </campaign-accounts>
        </v-tab-item>
        <v-tab-item :value="3">
          <campaign-features
            ref="features"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item>
        <v-tab-item :value="4">
          <campaign-checkout-info
            ref="checkoutInfo"
            :campaign="campaign"
            :editMode="editMode"
            @enable-department="departmentsEnabled = true"
            @disable-department="departmentsEnabled = false"
            @enable-location="locationsEnabled = true"
            @disable-location="locationsEnabled = false"
            @enable-manager="managersEnabled = true"
            @disable-manager="managersEnabled = false"
          />
        </v-tab-item>
        <v-tab-item :value="5">
          <campaign-departments
            ref="departments"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item>
        <v-tab-item :value="6">
          <campaign-locations
            ref="locations"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item>
        <v-tab-item :value="7">
          <campaign-managers
            ref="managers"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item>
<!--         <v-tab-item :value="8">
          <campaign-products
            ref="products"
            :campaign="campaign"
            :editMode="editMode"
          />
        </v-tab-item> -->
      </v-tabs-items>

      <v-divider></v-divider>

      <v-progress-linear
        v-if="isSaving"
        indeterminate
        color="green"
      />

      <v-card-actions>
        <v-spacer />
        <v-btn
          class="white--text"
          :disabled="backButtonDisabled"
          color="#0A0B0A"
          @click="prevTab()"
        >
          Back
        </v-btn>
        <v-btn
          :disabled="nextButtonDisabled"
          color="primary"
          @click="nextTab()"
        >
          Next
        </v-btn>
        <v-btn
          color="error"
          @click="saveCampaign"
          :disabled="saveButtonDisabled"
        >
          Save And Exit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>


<script>
  import moment from 'moment';

  import CampaignSetup from './CampaignSetup';
  import CampaignAccounts from './CampaignAccounts';
  import CampaignFeatures from './CampaignFeatures';
  import CampaignCheckoutInfo from './CampaignCheckoutInfo';
  import CampaignDepartments from './CampaignDepartments';
  import CampaignLocations from './CampaignLocations';
  import CampaignManagers from './CampaignManagers';
  // import CampaignProducts from './CampaignProducts';

  export default {
    name: 'Campaign',

    components: {
      'campaign-setup': CampaignSetup,
      'campaign-accounts': CampaignAccounts,
      'campaign-features': CampaignFeatures,
      'campaign-checkout-info': CampaignCheckoutInfo,
      'campaign-departments': CampaignDepartments,
      'campaign-locations': CampaignLocations,
      'campaign-managers': CampaignManagers,
      // 'campaign-products': CampaignProducts,
    },

    data() {
      return {
        isMounted: false,
        isSaving: false,
        activeTab: 0,

        roles: {},
        // campaign: {},

        // FIXME: remove this when done testing
        campaign: {
          "name": "My Campaign",
          "company_name": "Dickbutt Pizzeria",
          "start_date": "2020-02-23",
          "end_date": "2020-03-01",

          "storefront_pricing": false,
          "company_allowance": null,
          "company_allowance_personal_pay": null,
          "items_count_limit": null,
          "price_limit": null,
          "email_shopper": true,

          "checkout_fields": "[\"Department\",\"Location\",\"Manager\"]",
          "departments": "[\"Foo Fighting Department\"]",
          "managers": "[{\"first_name\":\"Andrew\",\"last_name\":\"Sczesnak\",\"email\":\"andrewscz@gmail.com\"}]",

          "message": "",
          "bfl_cost": 0.00,
          "distribtor_po": null,
          "pick_pack_partner_message": "Have a wonderful day!",

          "distributor_id": 2,
          "distributor": {
            "_jv": {
              "id": 2,
              "links": {
                "self": "http://localhost:5000/distributors/2/"
              },
              "relationships": {
                "accounts": {
                  "data": null,
                  "links": {
                    "self": "http://localhost:5000/distributors/2/accounts"
                  }
                },
                "campaigns": {
                  "data": null,
                  "links": {
                    "self": "http://localhost:5000/distributors/2/campaigns"
                  }
                },
                "product_types": {
                  "data": null,
                  "links": {
                    "self": "http://localhost:5000/distributors/2/product_types"
                  }
                },
                "products": {
                  "data": null,
                  "links": {
                    "self": "http://localhost:5000/distributors/2/products"
                  }
                }
              },
              "type": "Distributor",
            },
            "address": "130 Grove Cove",
            "campaign_cost": 4.603346706542224,
            "created_at": "2020-02-22 00:50:36.804765-07:00",
            "email": "unirritableness1838@yahoo.com",
            "is_deleted": false,
            "max_sales_count": 3,
            "modified_at": "2020-02-22 00:50:36.804765-07:00",
            "name": "Cartoon Network Studios",
            "ow_cost": 6.422156892625295,
            "transaction_cost": 0,
            "accounts": {},
            "campaigns": {},
            "product_types": {},
            "products": {}
          },
          "accounts": [
            {
              "id": null,
              "username": "shopper1",
              "password": "password",
              "email": "",
              "first_name": "",
              "last_name": "",
              "role_id": 5,
              "reports_enabled": false,
              "_jv": {
                "type": "Account"
              },
              "role": {
                "_jv": {
                  "id": 5,
                  "links": {
                    "self": "http://localhost:5000/roles/5/"
                  },
                  "relationships": {
                    "accounts": {
                      "data": null,
                      "links": {
                        "self": "http://localhost:5000/roles/5/accounts"
                      }
                    }
                  },
                  "type": "Role",
                },
                "name": "Shopper",
                "accounts": {}
              }
            },
            {
              "id": null,
              "username": "adminbuyer1",
              "password": "password",
              "email": "",
              "first_name": "",
              "last_name": "",
              "role_id": 4,
              "reports_enabled": false,
              "_jv": {
                "type": "Account"
              },
              "role": {
                "_jv": {
                  "id": 4,
                  "links": {
                    "self": "http://localhost:5000/roles/4/"
                  },
                  "relationships": {
                    "accounts": {
                      "data": null,
                      "links": {
                        "self": "http://localhost:5000/roles/4/accounts"
                      }
                    }
                  },
                  "type": "Role",
                },
                "name": "Admin Buyer",
                "accounts": {}
              }
            }
          ],
          "locations": [
            {
              "id": null,
              "nickname": "Home",
              "company_name": "India Block Arts, Inc.",
              "street_and_number": "1825 Ashby Ave",
              "city": "Berkeley",
              "zip_code": "94703",
              "delivery_contact": null,
              "suite_unit_etc": null,
              "region": "California",
              "country": "United States",
              "campaign_id": null,
              "_jv": {
                "type": "Location"
              }
            }
          ]
        },

        departmentsEnabled: false,
        locationsEnabled: false,
        managersEnabled: false,

        tabRefs: {},
      }
    },

    computed: {
      editMode() {
        // FIXME: remove this when done testing
        return true;
        // return this.$route.params.id ? true : false;
      },

      availableTabs() {
        // the first several tabs are always enabled
        let tabList = [0, 1, 2, 3, 4];

        // these three tabs can be enabled in the features tab
        if (this.departmentsEnabled) {
          tabList.push(5);
        }

        if (this.locationsEnabled) {
          tabList.push(6);
        }

        if (this.managersEnabled) {
          tabList.push(7);
        }

        // // the products tab is only enabled if a distributor has been selected
        // if (this.campaign.distributor) {
        //   tabList.push(8);
        // }

        return tabList;
      },

      formsAreValid() {
        // check if forms are valid, up until the currently active tab
        let tabsUntilActive = this.availableTabs.slice(
          0, this.availableTabs.indexOf(this.activeTab) + 1
        );

        for (const tabNumber in tabsUntilActive) {
          if (this.tabRefs[tabNumber] && !this.tabRefs[tabNumber].valid) {
            return false;
          }
        }

        return true;
      },

      nextButtonDisabled() {
        if (this.isSaving || !this.formsAreValid) {
          return true;
        }

        if (this.activeTab === Math.max(...this.availableTabs)) {
          return true;
        }

        return false;
      },

      backButtonDisabled() {
        if (this.isSaving) {
          return true;
        }

        if (this.activeTab === 0) {
          return true;
        }

        return false;
      },

      // FIXME: refactor or remove
      isDraft() {
        return true;
      },

      // FIXME: refactor or remove
      saveButtonDisabled() {
        return false;
      },
    },

    async mounted() {
      await this.loadRoles();

      // allow the destination tab to be specified in the query string
      if (this.$route.query.tab) {
        this.activeTab = parseInt(this.$route.query.tab)
      }

      this.$data.isMounted = true;

      // we have to wait for all the child components to render before we can collate their refs
      this.$nextTick(() => {
        this.tabRefs = {
          0: this.$refs.campaignSetup,
          1: this.$refs.shopper,
          2: this.$refs.adminBuyer,
          3: this.$refs.features,
          4: this.$refs.checkoutInfo,
          5: this.$refs.departments,
          6: this.$refs.locations,
          7: this.$refs.managers,
          // 8: this.$refs.products,
        };
      });
    },

    methods: {
      saveCampaign() {

      },

      checkCheckoutArrayIsFilled() {
        let outputMessage = '';
        if (this.$refs.checkoutInfo.$data.checkoutFieldsDepartmentEnabled &&
          this.$refs.departments.$data.departments.length === 0) {
          outputMessage += 'No Department selected. ';
        }

        if (this.$refs.checkoutInfo.$data.checkoutFieldsLocationEnabled &&
          this.$refs.locations.$data.locations.length === 0) {
          outputMessage += 'No Location selected. ';
        }

        if (this.$refs.checkoutInfo.$data.checkoutFieldsManagerEnabled &&
          this.$refs.managers.$data.managers.length === 0) {
          outputMessage += 'No Manager selected. ';
        }

        outputMessage.length > 0 && this.$store.dispatch('raiseInfo', outputMessage)
      },

      async loadRoles() {
        // this.possibleRolesPending = true;

        await this.$store.dispatch('jv/get', 'roles').then(roles => {
          Object.values(roles).forEach(role => {
            this.$data.roles[role.name] = role;
          });
        }).catch(err => {
          console.error(err);
        });

        // this.possibleRolesPending = false;
      },

      saveTab() {
        // have the current tab update our campaign model
        let result;

        // if the update throws an exception, catch it and pop a toaster message
        try {
          result = this.tabRefs[this.activeTab].updateCampaign(this.campaign);
        } catch(err) {
          console.log(err);
          this.$store.dispatch('raiseError', err);

          return false;
        }

        this.campaign = result;

        return true;
      },

      nextTab(tabId) {
        if (this.saveTab()) {
          // if tabId was specified, jump to that tab--otherwise, move to the next tab
          if (tabId !== undefined) {
            this.activeTab = tabId;
          } else {
            this.activeTab = this.availableTabs[this.availableTabs.indexOf(this.activeTab) + 1];
          }
        }
      },

      prevTab() {
        if (this.saveTab()) {
          // move to the previous tab
          this.activeTab = this.availableTabs[this.availableTabs.indexOf(this.activeTab) - 1];
        }
      },
    }
  }
</script>

<style scoped>
  .v-tabs__div {
    position: relative;
  }

  .v-tabs__div > .v-tabs__item > div {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 1;
  }
</style>
