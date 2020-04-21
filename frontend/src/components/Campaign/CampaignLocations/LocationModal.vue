<template>
    <v-layout row justify-center>
      <v-dialog v-model="modalPopped" persistent max-width="800">
        <v-card>
          <v-card-title class="headline">
            {{ editMode !== false ? 'Edit Location' : 'Create Location' }}
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text>
            <v-form class="ml-5 mr-5"
              ref="form"
              v-model="valid"
            >
              <v-container grid-list-md class="pa-0">
                <v-layout row wrap>
                  <v-flex xs6>
                    <v-tooltip top>
                      <v-text-field
                        slot="activator"
                        label="Location Nickname *"
                        v-model="location.nickname"
                        :rules="[validateNotEmpty]"
                      ></v-text-field>
                      <span>
                        Package delivery location nickname selected by the shopper at checkout
                      </span>
                    </v-tooltip>
                    <v-text-field
                      label="Company Name *"
                      v-model="location.company_name"
                      :rules="[validateNotEmpty]"
                    ></v-text-field>
                    <blockquote>Please, fill in the remaining information for reporting purposes</blockquote>
                    <v-text-field
                      label="Street and number *"
                      v-model="location.street_and_number"
                      :rules="[validateNotEmpty]"
                    ></v-text-field>
                    <v-text-field
                      label="City *"
                      v-model="location.city"
                      :rules="[validateNotEmpty]"
                    ></v-text-field>
                    <v-text-field
                      label="Postal Code *"
                      v-model="location.zip_code"
                      :rules="[validateZipCode]"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6>
                    <v-text-field
                      label="Attention/Delivery Contact"
                      v-model="location.delivery_contact"
                    ></v-text-field>
                    <v-text-field
                      label="Suite, Unit, Building, Floor, etc."
                      v-model="location.suite_unit_etc"
                    ></v-text-field>
                    <v-combobox
                      hide-no-data
                      browser-autocomplete="disabled"
                      label="Country *"
                      v-model="location.country"
                      :items="countryNames"
                    ></v-combobox>
                    <v-combobox
                      hide-no-data
                      browser-autocomplete="disabled"
                      label="State/Province *"
                      v-model="location.region"
                      :items="provinceNames"
                      :rules="[validateNotEmpty]"
                    ></v-combobox>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-form>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" @click="hide">Cancel</v-btn>
            <v-btn color="success" @click="save" :disabled="!valid">Save Location</v-btn>
          </v-card-actions>  
        </v-card>
      </v-dialog>
    </v-layout>
</template>

<script>
  import rules from '@/mixins/rules';
  import countriesProvinces from 'countries-provinces';
  import Location from '@/models/Location';

  export default {
    name: 'LocationModal',

    mixins: [
      rules
    ],

    data () {
      return {
        modalPopped: false,
        editMode: false,
        editIndex: null,
        
        valid: true,
        location: Location.generateEmpty(),

        countryNames: [],
        countryObjects: [],
        provinceNames: [],
      }
    },

    watch: {
      // https://github.com/vuetifyjs/vuetify/issues/4663
      'location.country'(oldVal, newVal) {
        if (oldVal !== newVal) {
          let country = this.countryObjects.filter(
            obj => obj.name === this.location.country
          )[0];

          if (country && country.short) {
            this.provinceNames = countriesProvinces.fromCountryCode(country.short).map(obj => obj.name);
            this.location.region = null;
          } else {
            this.provinceNames = [];
          }
        }
      },
    },

    mounted() {
      this.countryNames = countriesProvinces.countries.en.map(obj => obj.name);
      this.countryObjects = countriesProvinces.countries.en;
      this.provinceNames = countriesProvinces.fromCountryCode('US').map(obj => obj.name);
    },

    methods: {
      show(location, index) {
        this.modalPopped = true;

        if (location && index !== undefined) {
          this.location = JSON.parse(JSON.stringify(location));
          this.editMode = true;
          this.editIndex = index;
        } else {
          this.drop();
        }
      },

      async save() {
        let location = JSON.parse(JSON.stringify(this.location));
        let action = this.editMode !== false ? 'update' : 'save';

        this.$emit(action, location, this.editIndex);
        this.drop();
        this.modalPopped = false;
      },

      hide() {
        this.drop();
        this.modalPopped = false;
      },

      drop() {
        this.location = Location.generateEmpty();
        this.editMode = false;
        this.editIndex = null;
      }
    }
  }
</script>
