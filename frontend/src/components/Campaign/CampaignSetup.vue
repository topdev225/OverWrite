<template>
  <v-container grid-list-xs>
  <v-flex xs12 mt-5 mb-5 v-if="possibleDistributorsPending">
      <center>
        <v-progress-circular
          :indeterminate="true"
          color="green"
          size="32"
          width="4"
        />
      </center>
    </v-flex>

    <v-form ref="form" v-model="valid" v-if="!possibleDistributorsPending">
      <div v-on:click="warningDialogShow">
        <v-select
          v-model="distributorId"
          :items="possibleDistributors"
          :disabled="disableDistributorList"
          :rules="[validateNotEmpty]"
          @focus="loadDistributors"
          label="Distributor *"
          browser-autocomplete="new-password"
          item-text="name"
          item-value="_jv.id"
        />
      </div>

      <v-text-field
        v-model="companyName"
        label="Company Name *"
        hint="The company you are creating this campaign for. For example, Samsung"
        class="mb-4"
        :rules="[validateNotEmpty]"
      />

      <v-text-field
        v-model="campaignName"
        label="Campaign name *"
        hint="The reason for this campaign. For example, Samsung Spring 2019 Uniforms"
        :rules="[validateNotEmpty]"
      />

      <v-card class="pa-3 mb-4 mt-4 elevation-3">
        <p style="color: gray">Campaign Message</p>
        <ckeditor
          :editor="editor"
          v-model="campaignMessage"
          :config="editorConfig"
        />
      </v-card>

      <v-card class="pa-3 elevation-3" @click.native="rangePickerDisplayed = true">
        <p style="color: gray">Click on box to change</p>
        <v-text-field
          v-model="campaignStartDateFormatted"
          label="Start date *">
        </v-text-field>
        <v-text-field
          v-model="campaignEndDateFormatted"
          label="End date *">
        </v-text-field>
      </v-card>
    </v-form>

    <v-dialog v-model="rangePickerDisplayed" width="800">
      <v-card>
        <v-card-title class="headline" primary-title>
          Select Range
        </v-card-title>

        <v-card-text>
          <v-daterange
            :options="rangePickerOptions"
            @input="dateRangeChange"
          />
          <div style="padding-left:101px; padding-right:14px">
            <v-layout row wrap class="mt-4">
              <v-flex md12 lg6 class="text-xs-center" style="padding: 0 14px">
                <vue-timepicker
                  hide-clear-button
                  close-on-complete
                  format="hh:mm A"
                  v-model="campaignStartTime"
                  :minute-interval="10"
                />
              </v-flex>
              <v-flex md12 lg6 class="text-xs-center" style="padding: 0 14px">
                <vue-timepicker
                  hide-clear-button
                  close-on-complete
                  format="hh:mm A"
                  v-model="campaignEndTime"
                  :minute-interval="10"
                />
              </v-flex>
            </v-layout>
          </div>
        </v-card-text>

        <v-card-actions class="mt-3">
          <v-spacer />
          <v-btn color="primary" @click="closeRangePicker">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="warningDialogDisplayed" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Warning!</v-card-title>
        <v-card-text>
          If you change the distributor attached to an existing campaign, it will affect your
          ability to display and edit products that have already been added.

          Do you still want change distributor?
        </v-card-text>
        <div class="text-xs-center px-2 py-2">
          <div class="flex-grow-1"></div>
          <v-btn color="error" text @click="warningDialogHide">Cancel</v-btn>
          <v-btn color="success" text @click="warningDialogChange">Change</v-btn>
        </div>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<style>
  .vue__time-picker .dropdown {
    top: auto !important;
    bottom: 100% !important;
  }
</style>

<script>
  import moment from 'moment';
  import VueTimepicker from 'vue2-timepicker/src/vue-timepicker.vue';
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  import rules from '@/mixins/rules';

  export default {
    components: {
      VueTimepicker,
    },

    props: {
      campaign: Object,
      editMode: Boolean,
    },

    mixins: [
      rules
    ],

    data() {
      return {
        distributorId: null,
        possibleDistributors: [],
        possibleDistributorsPending: true,
        disableDistributorList: false,

        campaignName: '',
        companyName: '',

        campaignStartTime: "12:00 AM",
        campaignEndTime: "12:00 AM",
        campaignStartDate: moment().format('YYYY-MM-DD'),
        campaignEndDate: moment().add(7, 'days').format('YYYY-MM-DD'),
        rangePickerDisplayed: false,
        rangePickerOptions: {
          format: 'MM/DD/YYYY',
          startDate: this.$props.campaign && this.$props.campaign.start_date ? moment(this.$props.campaign.start_date).format('YYYY-MM-DD') : null,
          endDate: this.$props.campaign && this.$props.campaign.end_date ? moment(this.$props.campaign.end_date).format('YYYY-MM-DD') : null,
          minDate: moment().subtract(10, 'years').format('YYYY-MM-DD'),
          maxDate: moment().add(100, 'years').format('YYYY-MM-DD'),
          presets: [
            {
              label: '3 days',
              range: [
                moment().format('YYYY-MM-DD'),
                moment().add(2, 'days').format('YYYY-MM-DD'),
              ]
            },
            {
              label: '7 days',
              range: [
                moment().format('YYYY-MM-DD'),
                moment().add(6, 'days').format('YYYY-MM-DD'),
              ],
            },
            {
              label: '30 days',
              range: [
                moment().format('YYYY-MM-DD'),
                moment().add(29, 'days').format('YYYY-MM-DD'),
              ]
            }
          ]
        },

        campaignMessage: '',
        editor: ClassicEditor,
        editorConfig: {
          toolbar: [
            'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'undo', 'redo'
          ],
        },

        warnOnDistributorChange: this.$props.editMode,
        warningDialogDisplayed: false,

        valid: null,
      }
    },

    computed: {
      selectedDistributor() {
        let matchingDistributors = this.possibleDistributors.filter(
          obj => obj._jv.id === this.distributorId
        );

        if (matchingDistributors) {
          return matchingDistributors[0];
        }

        return null;
      },

      campaignStartDateFormatted() {
        return this.$data.campaignStartDate ? moment(
          this.$data.campaignStartDate
        ).format('MM/DD/YYYY') : 'Not selected'
      },

      campaignEndDateFormatted() {
        return this.$data.campaignEndDate ? moment(
          this.$data.campaignEndDate
        ).format('MM/DD/YYYY') : 'Not selected'
      },

    },

    async mounted() {
      if (this.$props.editMode) {
        this.fillPreliminaryData();
      }

      await this.loadDistributors();
    },

    methods: {
      fillPreliminaryData() {
        // if we are editing a campaign, copy its properties into our component to avoid mutating
        // props. we will save them to the original model when we're done.
        this.$data.distributorId = this.$props.campaign.distributor_id;
        this.$data.campaignName = this.$props.campaign.name;
        this.$data.companyName = this.$props.campaign.company_name;
        this.$data.campaignMessage = this.$props.campaign.message;
        this.$data.campaignStartDate = this.$props.campaign.start_date;
        this.$data.campaignEndDate = this.$props.campaign.end_date;
        this.campaignStartTime = (
          this.campaignStartDate ? moment(this.campaignStartDate).format('hh:mm A') : '12:00 AM'
        );
        this.campaignEndTime = (
          this.campaignEndDate ? moment(this.campaignEndDate).format('hh:mm A') : '12:00 AM'
        );
      },
      
      async loadDistributors() {
        this.possibleDistributorsPending = true;

        await this.$store.dispatch('jv/get', 'distributors').then(distributors => {
          // if the user is locked into a particular distributor, make this field non-optional
          let possibleDistributors = Object.values(distributors);
          let userLockedDistributorId = this.$store.state.account.distributor_id;

          if (userLockedDistributorId !== null) {
            possibleDistributors = possibleDistributors.filter(
              obj => obj._jv.id === userLockedDistributorId
            );

            this.disableDistributorList = true;
          }

          this.possibleDistributors = possibleDistributors;
        }).catch(err => {
          console.error(err);
        });

        this.possibleDistributorsPending = false;
      },

      warningDialogShow() {
        console.log(this.warnOnDistributorChange);
        if (!this.disableDistributorList && this.warnOnDistributorChange) {
          this.warningDialogDisplayed = true;
        }
      },

      warningDialogHide() {
        this.warningDialogDisplayed = false;
      },

      warningDialogChange() {
        this.warningDialogHide();
        this.disableDistributorList = false;
        this.warnOnDistributorChange = false;
      },

      dateRangeChange(range) {
        this.campaignStartTime = "12:00 AM";
        this.campaignEndTime = "12:00 AM";

        this.$data.campaignStartDate = range[0];
        this.$data.campaignEndDate = range[1];

        this.$data.rangePickerOptions.presets[0].range = [
          moment(range[0]).format('YYYY-MM-DD'),
          moment(range[0]).add(2, 'days').format('YYYY-MM-DD'),
        ];
        this.$data.rangePickerOptions.presets[1].range = [
          moment(range[0]).format('YYYY-MM-DD'),
          moment(range[0]).add(6, 'days').format('YYYY-MM-DD'),
        ];
        this.$data.rangePickerOptions.presets[2].range = [
          moment(range[0]).format('YYYY-MM-DD'),
          moment(range[0]).add(29, 'days').format('YYYY-MM-DD'),
        ];
      },

      closeRangePicker() {
        if (!this.$data.campaignStartDate && !this.$data.campaignEndDate) {
          this.$data.campaignStartDate = moment().format('YYYY-MM-DD');
          this.$data.campaignEndDate = moment().add(7, 'days').format('YYYY-MM-DD');
        }

        this.rangePickerDisplayed = false;
      },

      updateCampaign(campaign) {
        if (!this.selectedDistributor) {
          throw 'Must select a distributor';
        }

        if (!this.campaignName) {
          throw 'A campaign name is required';
        }

        const data = {
          distributor: this.selectedDistributor,
          distributor_id: this.distributorId,
          name: this.campaignName,
          company_name: this.companyName,
          start_date: this.campaignStartDate,
          end_date: this.campaignEndDate,
          message: this.campaignMessage,
        };

        return {
          ...campaign,
          ...data,
        };
      },
    }
  }
</script>
