<template>
  <v-container grid-list-xs>
    <v-form ref="form">
      <blockquote
        class="blockquote text-xs-left ml-4 mr-4"
      >
        Select 3-4 details you need to collect from shoppers before they check out.
        <br />
        <small>
          These details will be printed on each packaged order, helping you identify who
          placed the order and where it should be delivered to.
        </small>
      </blockquote>

      <v-switch
        v-model="fieldFirstNameEnabled"
        label="First Name"
      />

      <v-switch
        v-model="fieldLastNameEnabled"
        label="Last Name"
      />

      <v-switch
        v-model="fieldCompanyEmailEnabled"
        label="Company Email"
        :disabled="$props.campaign.email_shopper"
      />

      <v-switch
        v-model="fieldDepartmentEnabled"
        label="Department"
        :disabled="$props.campaign.departments && JSON.parse($props.campaign.departments).length > 0"
      />

      <v-switch
        v-model="fieldLocationEnabled"
        label="Ship to location/branch"
        :disabled="$props.campaign.locations && $props.campaign.locations.length > 0"
      />

      <v-switch
        v-model="fieldManagerEnabled"
        label="Manager"
        :disabled="$props.campaign.managers && JSON.parse($props.campaign.managers).length > 0"
      />

      <v-switch
        v-model="fieldCustomEnabled"
        label="Unique Employee Identifier/Other"
      />

      <div v-if="fieldCustomEnabled">
        <v-card
          class="mb-2 mt-2 elevation-2"
          style="width: 50%"
          v-for="field in fieldCustom"
          :key=field>
          <v-container class="pa-1" fill-height grid-list-md>
            <v-layout row wrap align-center justify-space-between>
              <v-flex xs8 class="subheading pl-3">
                {{field}}
              </v-flex>
              <v-flex xs4 class="text-xs-right">
                <v-btn color="error" @click="removeCustomField(field)">delete</v-btn>
              </v-flex>
            </v-layout>
          </v-container>

        </v-card>
        <v-text-field
          label="Field name"
          v-model="fieldName"
        />
        </v-text-field>
        <v-btn @click="addCustomField">add</v-btn>
      </div>

    </v-form>
  </v-container>
</template>

<script>
  const PREDEFINED_CHECKOUT_FIELDS = [
    'First Name', 'Last Name', 'Company Email', 'Department', 'Location', 'Manager'
  ];

  export default {
    props: {
      campaign: Object,
      editMode: Boolean,
    },

    data () {
      return {
        valid: true,  // there is no way a bunch of checkboxes can be invalid

        fieldFirstNameEnabled: false,
        fieldLastNameEnabled: false,
        fieldCompanyEmailEnabled: false,
        fieldDepartmentEnabled: false,
        fieldLocationEnabled: false,
        fieldManagerEnabled: false,
        fieldCustomEnabled: false,

        fieldCustom: [],

        fieldName: '',
      }
    },

    computed: {
      checkoutFieldsJSON() {
        let fields = []

        this.fieldFirstNameEnabled && fields.push('First Name');
        this.fieldLastNameEnabled && fields.push('Last Name');
        this.fieldCompanyEmailEnabled && fields.push('Company Email');
        this.fieldDepartmentEnabled && fields.push('Department');
        this.fieldLocationEnabled && fields.push('Location');
        this.fieldManagerEnabled && fields.push('Manager');

        if (this.fieldCustomEnabled) {
          fields = fields.concat(this.fieldCustom);
        }

        return JSON.stringify(fields);
      }
    },

    mounted() {
      if (this.editMode) {
        this.fillPreliminaryData();
      }
    },

    watch: {
      campaign: function(newVal, oldVal) {
        // this field should be enabled if one of the selected features is to email shoppers a
        // confirmation email. if we don't collect their emails, how can we email them?
        if (newVal.email_shopper) {
          this.fieldCompanyEmailEnabled = true;
        }
      },

      fieldDepartmentEnabled: function(newVal, oldVal) {
        if (newVal === true) {
          this.$emit('enable-department');
        } else {
          this.$emit('disable-department');
        }
      },

      fieldLocationEnabled: function(newVal, oldVal) {
        if (newVal === true) {
          this.$emit('enable-location');
        } else {
          this.$emit('disable-location');
        }
      },

      fieldManagerEnabled: function(newVal, oldVal) {
        if (newVal === true) {
          this.$emit('enable-manager');
        } else {
          this.$emit('disable-manager');
        }
      },
    },

    methods: {
      fillPreliminaryData() {
        let existingFields = JSON.parse(this.$props.campaign.checkout_fields);

        this.fieldFirstNameEnabled = !!~existingFields.indexOf('First Name');
        this.fieldLastNameEnabled = !!~existingFields.indexOf('Last Name');
        this.fieldCompanyEmailEnabled = !!~existingFields.indexOf('Company Email');
        this.fieldDepartmentEnabled = !!~existingFields.indexOf('Department');
        this.fieldLocationEnabled = !!~existingFields.indexOf('Location');
        this.fieldManagerEnabled = !!~existingFields.indexOf('Manager');

        existingFields.forEach(property => {
          if (PREDEFINED_CHECKOUT_FIELDS.indexOf(property) === -1) {
            this.fieldCustom.push(property);
          }
        })
      },

      addCustomField() {
        if (!this.fieldName) {
          this.$store.dispatch('raiseError', 'Field name cannot be blank');
        } else {
          this.fieldCustom.push(this.fieldName);
          this.fieldName = '';
        }
      },

      removeCustomField(field) {
        this.fieldCustom = this.fieldCustom.filter(
          x => x !== field
        )
      },

      updateCampaign(campaign) {
        campaign.checkout_fields = this.checkoutFieldsJSON;

        return campaign;
      },
    }
  }
</script>
