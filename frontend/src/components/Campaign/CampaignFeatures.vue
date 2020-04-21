<template>
  <v-container grid-list-xs>
    <v-form ref="form" v-model="valid">
      <v-tooltip top>
        <v-switch
          style="width: 250px"
          slot="activator"
          v-model="campaignStorefrontPricingEnabled"
          label="Display storefront pricing">
        </v-switch>
        <span>Click if you would like people to see pricing on storefront. 
          Otherwise, only the admin buyer will see prices</span>
      </v-tooltip>

      <v-tooltip top>
        <v-switch
          style="width: 250px"
          slot="activator"
          v-model="campaignCompanyAllowanceEnabled"
          label="Offer company allowance">
        </v-switch>
        <span>Set a dollar abount that the company will cover for shopper purchases</span>
      </v-tooltip>

      <div class="ml-5" v-if="campaignCompanyAllowanceEnabled">
        <v-text-field
          label="Enter Shopper Allowance"
          prefix="$"
          v-model="campaignCompanyAllowance"
          :rules="[validateNumber]">
        </v-text-field>
        <v-switch
          v-model="campaignCompanyAllowancePersonalPayEnabled"
          label="Allow shoppers to personally pay for allowance overages">
        </v-switch>
        <v-select
          v-if="campaignCompanyAllowancePersonalPayEnabled"
          v-model="campaignCompanyAllowancePersonalPay"
          :items="['Payroll Deductions', 'Individual CC Payment']"
          label="Pay Method"
        ></v-select>
      </div>

      <v-tooltip top>
        <v-switch
          style="width: 280px"
          slot="activator"
          v-model="campaignItemsCountLimitEnabled"
          label="Limit of items in shopping cart">
        </v-switch>
        <span>
          Allow shoppers to purchase a set number of items for their uniform
          or merchandise purchase
        </span>
      </v-tooltip>

      <div class="ml-5" v-if="campaignItemsCountLimitEnabled">
        <v-text-field
          label="Enter number of items allowed per person"
          prefix="#"
          :rules="[validateInteger]"
          v-model="campaignItemsCountLimit">
        </v-text-field>
      </div>

      <v-tooltip top>
        <v-switch
          style="width: 280px"
          slot="activator"
          v-model="campaignPriceLimitEnabled"
          label="Limit shopping cart $ amount">
        </v-switch>
        <span>
          Allow shoppers to spend a specific amount of money
          on their purchases
        </span>
      </v-tooltip>
      
      <div class="ml-5" v-if="campaignPriceLimitEnabled">
        <v-text-field
          label="Enter dollar amount allowed per person"
          prefix="$"
          :rules="[validateNumber]"
          v-model="campaignPriceLimit">
        </v-text-field>
      </div>

      <v-tooltip top>
        <v-switch
          style="width: 280px"
          slot="activator"
          v-model="campaignEmailConfirmationEnabled"
          label="Email confirmation">
        </v-switch>
        <span>
          Click if you would like individual shoppers to receive email
          confirmation after they purchase
        </span>
      </v-tooltip>
    </v-form>
  </v-container>
</template>

<script>
  import rules from '@/mixins/rules'

  export default {
    props: {
      campaign: Object,
      editMode: Boolean,
    },

    mixins: [
      rules
    ],
    
    data () {
      return {
        valid: null,

        campaignStorefrontPricingEnabled: false,
        campaignCompanyAllowanceEnabled: false,
        campaignCompanyAllowancePersonalPayEnabled: false,
        campaignItemsCountLimitEnabled: false,
        campaignPriceLimitEnabled: false,
        campaignEmailConfirmationEnabled: false,

        campaignCompanyAllowance: 0,
        campaignCompanyAllowancePersonalPay: '',
        campaignItemsCountLimit: 0,
        campaignPriceLimit: 0, 
      }
    },

    watch: {
      campaignEmailConfirmationEnabled(val) {
        val && (this.$parent.$parent.$parent.$parent.$refs.checkoutInfo.checkoutFieldsCompanyEmailEnabled = true)
      }
    },

    mounted() {
      if (this.editMode) {
        this.fillPreliminaryData()
      }
    },

    methods: {
      fillPreliminaryData() {
        this.$data.campaignStorefrontPricingEnabled = this.$props.campaign.storefront_pricing;

        this.$data.campaignCompanyAllowanceEnabled = !!this.$props.campaign.company_allowance;
        this.$data.campaignCompanyAllowance = this.$props.campaign.company_allowance;

        this.$data.campaignCompanyAllowancePersonalPayEnabled = !!this.$props.campaign.company_allowance_personal_pay;
        this.$data.campaignCompanyAllowancePersonalPay = this.$props.campaign.company_allowance_personal_pay;

        this.$data.campaignItemsCountLimitEnabled = !!this.$props.campaign.items_count_limit;
        this.$data.campaignItemsCountLimit = this.$props.campaign.items_count_limit;

        this.$data.campaignPriceLimitEnabled = !!this.$props.campaign.price_limit;
        this.$data.campaignPriceLimit = this.$props.campaign.price_limit;

        this.$data.campaignEmailConfirmationEnabled = !!this.$props.campaign.email_shopper;
      },

      updateCampaign(campaign) {
        // we have to manually null out any values that aren't enabled. if the user enables one of
        // these features, fills in a value, and then disabled the feature, the value still exists
        // in the state.
        if (!this.$data.campaignCompanyAllowanceEnabled) {
          this.$data.campaignCompanyAllowance = null;
        }

        if (!this.$data.campaignCompanyAllowancePersonalPayEnabled) {
          this.$data.campaignCompanyAllowancePersonalPay = null;
        }

        if (!this.$data.campaignItemsCountLimitEnabled) {
          this.$data.campaignItemsCountLimit = null;
        }

        if (!this.$data.campaignPriceLimitEnabled) {
          this.$data.campaignPriceLimit = null;
        }

        const data = {
          storefront_pricing: this.$data.campaignStorefrontPricingEnabled,
          company_allowance: this.$data.campaignCompanyAllowance,
          company_allowance_personal_pay: this.$data.campaignCompanyAllowancePersonalPay,
          items_count_limit: this.$data.campaignItemsCountLimit,
          price_limit: this.$data.campaignPriceLimit,
          email_shopper: this.$data.campaignEmailConfirmationEnabled,
        };

        return {
          ...campaign,
          ...data,
        }
      },
    }
  }
</script>
