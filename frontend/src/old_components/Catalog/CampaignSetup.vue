<template>
  <v-stepper v-model="e1">
    <v-stepper-header style="height: 100%">
      <template v-for="(item, index) in stepArr">
        <v-stepper-step :complete="e1 > index + 1" :step="index + 1">{{item.name}}</v-stepper-step>
        <v-divider>

        </v-divider>
      </template>
    </v-stepper-header>
    <v-stepper-items>
      <v-stepper-content step="2">
        <h2>Admin Buyer Setup</h2>
        <v-form px-2 v-model="validAdminAccount">
          <v-text-field v-model="firstName" :rules="nameRules" label="First Name" required></v-text-field>
          <v-text-field v-model="lastName" :rules="nameRules" label="Last Name" required></v-text-field>
          <v-text-field v-model="adminUserName" :rules="adminLoginRules" label="User Name" required></v-text-field>
          <v-text-field v-model="email" :rules="emailRules" label="E-mail" required></v-text-field>
          <v-switch label="Allow buyer to see reports" v-model="switchPassword"></v-switch>
          <v-text-field v-model="adminPassword" v-if="switchPassword" label="Password" type="password"
                        :rules="passwordRules" required></v-text-field>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)">Next</v-btn>



      </v-stepper-content>

      <v-stepper-content step="1">
        <h2>Campaign Setup</h2>
        <v-form px-2 v-model="validShopperAccount">
          <v-text-field v-model="campaignName" :rules="companyRules" label="Campaign Name" required></v-text-field>
          <v-textarea
            box
            label="Message to User"
            auto-grow
            v-model="messageToUsers"
          ></v-textarea>
          <v-select
            v-model="selectedDistributor"
            :items="possibleDistributors"
            item-text="name"
            item-value="id"
            label="Distributor"
            return-object
          >
          </v-select>
          <v-text-field v-model="login" :rules="shopperLoginRules" label="Login" required></v-text-field>
          <v-text-field v-model="companyName" :rules="companyRules" label="Company Name" required></v-text-field>
          <v-text-field v-model="password" :rules="passwordRules" label="Password"
                        type="password" required></v-text-field>
          <v-flex xs12 sm6 md4>
            <v-menu
              :close-on-content-click="false"
              v-model="startDateInput"
              :nudge-right="40"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              min-width="290px"
            >
              <v-text-field
                slot="activator"
                v-model="startDateFormatted"
                label="Start Date (MM/DD/YYYY)"
                prepend-icon="event"
                readonly
                :rules="dateTimeRules"
                required
              ></v-text-field>
              <v-date-picker v-model="startDate" @input="startDateInput = false"></v-date-picker>
            </v-menu>
          </v-flex>
          <v-flex xs12 sm6 md4>
            <v-menu
              :close-on-content-click="false"
              v-model="endDateInput"
              :nudge-right="40"
              lazy
              transition="scale-transition"
              offset-y
              full-width
              min-width="290px"
            >
              <v-text-field
                slot="activator"
                v-model="endDateFormatted"
                label="End Date (MM/DD/YYYY)"
                prepend-icon="event"
                readonly
                :rules="dateTimeRules"
                required
              ></v-text-field>
              <v-date-picker v-model="endDate" @input="endDateInput = false"></v-date-picker>
            </v-menu>
          </v-flex>
        </v-form>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)" :disabled="!campaignName">Next</v-btn>

      </v-stepper-content>

      <v-stepper-content step="3">
        <h2>Campaign Features</h2>
        <v-form v-model="validExtraFeatures">
          <v-card>
            <v-card-title>
              <v-switch label="Display Storefront Pricing" v-model="storefrontPricing"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-layout align-start justify-center column fill-height>
                <v-flex>
                  <v-switch label="Offer Company Allowance" v-model="companyAllowance"></v-switch>
                </v-flex>
                <v-flex v-if="companyAllowance">
                  <v-layout align-start justify-center column fill-height>
                    <v-flex>
                      <div>Enter Shopper Allowance $</div>
                      <v-text-field
                        v-model="companyAllowanceData"
                        :rules="numberRules"
                      ></v-text-field>
                    </v-flex>
                    <v-flex>
                      <v-checkbox label="Allow shoppers to personally pay for allowance overages"
                                  v-model="companyAllowanceCheckbox"></v-checkbox>
                    </v-flex>
                    <v-flex v-if="companyAllowanceCheckbox">
                      <v-select
                        :items="companyAllowancePayMethods"
                        label="Pay Method"
                      ></v-select>
                    </v-flex>
                  </v-layout>
                </v-flex>
              </v-layout>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-layout align-start justify-center column fill-height>
                <v-flex>
                  <v-switch label="Limit of items in shopping cart" v-model="limitShoppingCart"></v-switch>
                </v-flex>
                <v-flex v-if="limitShoppingCart">
                  <div>Enter number of items allowed per person #</div>
                  <v-text-field
                    v-model="numberAllowedItems"
                    :rules="numberRules"
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-layout align-start justify-center column fill-height>
                <v-flex>
                  <v-switch label="Limit Shopping Cart $ Amount" v-model="cartAmount"></v-switch>
                </v-flex>
                <v-flex v-if="cartAmount">
                  <div>Enter Shopping Cart $ Limit</div>
                  <v-text-field
                    v-model="allowedLimit"
                    :rules="numberRules"
                    required
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Email confirmation" v-model="emailConfirmation"></v-switch>
            </v-card-title>
          </v-card>
        </v-form>
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)" :disabled="!validExtraFeatures">Next</v-btn>

      </v-stepper-content>

      <v-stepper-content step="4">
        <h2>Shopper Checkout Information</h2>
        <v-form>
          <v-card>
            <v-card-title>
              <v-switch label="First Name" v-model="formFieldsFirstName"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Last Name" v-model="formFieldsLastName"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Company Email" v-model="formFieldsCompanyEmail"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-layout align-start justify-center column fill-height>
                <v-flex>
                  <v-switch label="Unique Employee Identifier/Other" v-model="formFieldsIdentifier"></v-switch>
                </v-flex>
                <v-flex v-if="formFieldsIdentifier">
                  <v-btn @click="createAdditionalField">
                    add new field
                  </v-btn>
                  <div v-for="(item, index) in formFieldsArr" px-2 v-model="valid" :key="item.index">
                    <h2>Additional Field N{{index + 1}}</h2>
                    <v-text-field v-model="item.name" :rules="numberNameRules" label="New Field"
                                  required></v-text-field>
                    <v-btn @click="removeAdditionalField(item.index)">Remove</v-btn>
                  </div>
                </v-flex>
              </v-layout>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Ship to location/branch" v-model="formFieldsLocation"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Department" v-model="formFieldsDepartment"></v-switch>
            </v-card-title>
          </v-card>
          <v-card>
            <v-card-title>
              <v-switch label="Manager" v-model="formFieldsManager"></v-switch>
            </v-card-title>
          </v-card>
        </v-form>
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="save">Add OrderWrite</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="submitAndCreateProducts">Add OrderWrite and Create Products</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsDepartment" :step="stepArr.findIndex(x => x.name === 'Departments')+1">
        <v-btn @click="createDepartment" v-if="!departments[0]">Add Department</v-btn>
        <v-form v-for="(item, index) in departments" px-2 v-model="valid" :key="item.index">
          <h2>Department N{{index + 1}}</h2>
          <v-text-field v-model="item.name" :rules="numberNameRules" label="Department" required></v-text-field>
          <v-btn @click="removeDepartment(index)">Remove</v-btn>
          <v-btn @click="createDepartment">Add Department</v-btn>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="save">Add OrderWrite</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="submitAndCreateProducts">Add OrderWrite and Create Products</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsLocation" :step="stepArr.findIndex(x => x.name === 'Locations')+1">
        <v-btn @click="createLocation" v-if="!locations[0]">Add Location</v-btn>
        <v-form v-for="(item, index) in locations" px-2 v-model="valid" :key="item.index">
          <h2>Location N{{index + 1}}</h2>
          <v-layout>
            <v-flex mr-2>
              <v-text-field
                v-model="item.nickname"
                :rules="numberNameRules"
                label="Location Name"
                required
              ></v-text-field>
              <v-text-field v-model="companyName" :rules="numberNameRules" label="Company Name" required></v-text-field>
              <v-text-field
                v-model="item.street_and_number"
                :rules="addressRules"
                label="Street and number"
                required
              ></v-text-field>
              <v-text-field v-model="item.city" :rules="nameRules" label="City" required></v-text-field>
              <v-text-field v-model="item.zip_code" :rules="zipRules" label="Zip Code" required></v-text-field>
            </v-flex>
            <v-flex>
              <v-text-field
                v-model="item.delivery_contact"
                :rules="numberNameRulesAttention"
                label="Attention/Delivery Contact"
              ></v-text-field>
              <v-text-field
                v-model="item.suite_unit_etc"
                :rules="numberNameRules"
                label="Suite, Unit, Building, Floor, etc."
                required
              ></v-text-field>
              <v-text-field
                v-model="item.region"
                :rules="nameRules"
                label="State/Province/Region"
                required
              ></v-text-field>
              <v-text-field v-model="item.country" :rules="nameRules" label="Country" required></v-text-field>
            </v-flex>
          </v-layout>
          <v-btn @click="removeLocation(index)">Remove</v-btn>
          <v-btn @click="createLocation">Add Location</v-btn>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="save">Add OrderWrite</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="submitAndCreateProducts">Add OrderWrite and Create Products</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsManager" :step="stepArr.findIndex(x => x.name === 'Managers')+1">
        <v-btn @click="createManager" v-if="!managers[0]">Add Manager</v-btn>
        <v-form v-for="(item, index) in managers" px-2 v-model="valid" :key="item.index">
          <h2>Manager N {{index + 1}}</h2>
          <v-text-field v-model="item.first_name" :rules="nameRules" label="First Name" required></v-text-field>
          <v-text-field v-model="item.email" :rules="emailRules" label="Email" required></v-text-field>
          <v-btn @click="removeManager(index)">Remove</v-btn>
          <v-btn @click="createManager">Add Manager</v-btn>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="save">Add OrderWrite</v-btn>
        <v-btn v-if="e1 === stepArr.length" color="primary" @click="submitAndCreateProducts">Add OrderWrite and Create Products</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
  import axios from "@/axios";

  const emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
  const usernameRegex = /^[A-Za-z0-9]+(?:[ ._-][A-Za-z0-9]+)*$/
  const companyRegex = /^([a-zA-Z0-9]|[- @\.#&!])*$/
  const nameRegex = /^[a-z A-Z0-9]+$/
  const addressRegex =/^([a-zA-Z0-9]|[/№ #.])*$/
  const numberNameRegex = /^[a-z A-Z0-9]+$/
  const numberNameRegexZip = /^[a-z A-Z0-9-]+$/
  const numberRegex = /^[0-9]+$/
  export default {
    data() {
      return {
        managers: [],
        selectedDistributor: null,
        possibleDistributors: null,
        messageToUsers: '',
        stepArr: [
          {
            name: 'Campaign Setup'
          },
          {
            name: 'Admin Buyer Setup'
          },
          {
            name: 'Features'
          },
          {
            name: 'Checkout Info'
          }
        ],
        //Campaign Setup

        storefrontPricing: false,
        companyAllowance: false,
        limitShoppingCart: false,
        cartAmount: false,
        emailConfirmation: false,
        companyAllowanceData: 0,
        companyAllowanceCheckbox: false,
        companyAllowancePayMethods: ['payroll deductions',
          'individual CC Payment'
        ],
        numberAllowedItems: 0,
        allowedLimit: 0,

        //Form Fields

        formFieldsFirstName: '',
        formFieldsLastName: '',
        formFieldsCompanyEmail: '',
        formFieldsIdentifier: '',
        formFieldsLocation: false,
        formFieldsDepartment: false,
        formFieldsManager: false,
        formFieldsArr: [],

        fields: [],

        token:
          "Bearer" + " " + localStorage.getItem("user").replace(/['"]+/g, ""),
        e1: 0,
        validExtraFeatures: false,
        validAdminAccount: false,
        validShopperAccount: false,
        valid: false,
        accounts: [],
        departments: [],
        locations: [],
        switchPassword: false,
        startDate: "2019-01-01",
        endDate: "2019-01-01",
        startDateInput: false,
        endDateInput: false,
        campaignName: "",
        login: "",
        password: "",
        adminUserName: "",
        adminPassword: "",
        firstName: "",
        lastName: "",
        // Data validations
        numberRules: [
          v => !!v || 'Is required',
          v => numberRegex.test(v) || 'Type the number'
        ],
        loginRules: [
          v => !!v || 'Login is required',
          v => usernameRegex.test(v) || 'Username must be valid'
        ],
        companyRules: [
          v => !!v || 'Is required',
          v => companyRegex.test(v) || 'Must be valid'
        ],
        adminLoginRules: [
          v => !!v || 'Login is required',
          v => !(v === this.login) || 'Type another login',
          v => usernameRegex.test(v) || 'Username must be valid'
        ],
        shopperLoginRules: [
          v => !!v || 'Login is required',
          v => !(v === this.adminUserName) || 'Type another login',
          v => usernameRegex.test(v) || 'Username must be valid'
        ],
        dateTimeRules: [
          v => !!v || 'Is required',
        ],
        passwordRules: [
          v => !!v || 'Password is required'
        ],
        emailRules: [
          v => !!v || 'E-mail is required',
          v => emailRegex.test(v) || 'E-mail must be valid'
        ],
        nameRules: [
          v => !!v || 'Is required',
          v => nameRegex.test(v) || 'Must be valid'
        ],
        addressRules: [
          v => !!v || 'Is required',
          v => addressRegex.test(v) || 'Must be valid'
        ],
        numberNameRules: [
          v => !!v || 'Is required',
          v => numberNameRegex.test(v) || 'Must be valid'
        ],
        numberNameRulesAttention: [
          v => numberNameRegex.test(v) || 'Must be valid'
        ],
        zipRules: [
          v => !!v || 'Is required',
          v => numberNameRegexZip.test(v) || 'Must be valid'
        ],
        companyName: '',
        email: ''
      }
    },

    computed: {
      startDateFormatted () {
        const [year, month, day] = this.$data.startDate.split('-')
        return `${month}/${day}/${year}`
      },
      endDateFormatted () {
        const [year, month, day] = this.$data.endDate.split('-')
        return `${month}/${day}/${year}`
      }
    },

    watch: {

      formFieldsFirstName: function () {
        if (this.formFieldsFirstName) {
          this.addFirstNameField()
        } else {
          this.removeFirstNameField()
        }
      },
      formFieldsLastName: function () {
        if (this.formFieldsLastName) {
          this.addLastNameField()
        } else {
          this.removeLastNameField()
        }
      },
      formFieldsCompanyEmail: function () {
        if (this.formFieldsCompanyEmail) {
          this.addCompanyEmailField()
        } else {
          this.removeCompanyEmailField()
        }
      },
      // formFieldsManager: function () {
      //   if (this.formFieldsManager) {
      //     this.addManagerField()
      //   } else {
      //     this.removeManagerField()
      //   }
      // },

      formFieldsDepartment: function () {
        if (this.formFieldsDepartment) {
          this.addDepartmentStep()
        } else {
          this.removeDepartmentStep()
        }
      },

      formFieldsManager: function () {
        if (this.formFieldsManager) {
          this.addManagerStep()
        } else {
          this.removeManagerStep()
        }
      },

      formFieldsLocation: function () {
        if (this.formFieldsLocation) {
          this.addLocationStep()
        } else {
          this.removeLocationStep()
        }
      }
    },

    mounted () {
      axios.get(`/distributors`, {
        headers: {
          'Authorization': this.$data.token,
          'X-Fields': 'id, name'
        }
      }).then(resp => {
        this.$data.possibleDistributors = resp.data
      })
    },

    methods: {

      createManager() {
        function ManagerConstructor() {
          this.first_name = ''
          this.email = ''
          this.role_id = 6
        }

        let manager = new ManagerConstructor();
        this.$data.managers.push(manager);
        console.log(this.$data.managers);
      },
      pushManagersAccounts () {
        this.$data.managers.forEach((val) => {
          this.$data.accounts.push(val)
        })
      },

      save () {
        // Extend default fields with custom
        this.$data.formFieldsArr.forEach(f => {
          if (this.$data.fields.indexOf(f.name) === -1) {
            this.$data.fields.push(f.name)
          }
        })

        function generateSchema (fields) {
          let template = {
            'type': 'object',
            'properties': {},
            'required': fields
          }
          fields.forEach(field => {
            template.properties[field] = {'type': 'string'}
          })

          return template
        }
        this.pushManagersAccounts();
        this.setAccount();
        this.setAdminAccount();
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        let data = {
          distributor_id: this.$data.selectedDistributor.id,
          name: this.$data.campaignName,
          company_name: this.$data.companyName,
          start_date: this.$data.startDate,
          end_date: this.$data.endDate,
          storefront_pricing: this.$data.storefrontPricing,
          company_allowance: parseInt(this.$data.companyAllowanceData),
          items_count_limit: parseInt(this.$data.numberAllowedItems),
          price_limit: parseInt(this.$data.allowedLimit),
          email_shopper: this.$data.emailConfirmation,
          email_campaign: true,
          checkout_fields: generateSchema(this.$data.fields),
          message: this.$data.messageToUsers,
          departments: this.$data.departments,
          locations: this.$data.locations
        };
        if (this.$data.accounts.length > 0) {
          data.accounts = this.$data.accounts
        }
        axios
          .post(`/campaigns`, data, params)
          .then(resp => {
            this.$router.push(`/campaigns`);
          })
          .catch(err => {
            this.$store.dispatch('raiseError', err.response.data.message)
          });
      },
      submitAndCreateProducts () {
        // Extract custom fields



        function generateSchema (fields) {
          let template = {
            'type': 'object',
            'properties': {},
            'required': fields
          }
          fields.forEach(field => {
            template.properties[field] = {'type': 'string'}
          })

          return template
        }
        this.pushManagersAccounts();
        this.setAccount();
        this.setAdminAccount();
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        let data = {
          distributor_id: this.$data.selectedDistributor.id,
          name: this.$data.campaignName,
          company_name: this.$data.companyName,
          start_date: this.$data.startDate,
          end_date: this.$data.endDate,
          storefront_pricing: this.$data.storefrontPricing,
          company_allowance: parseInt(this.$data.companyAllowanceData),
          items_count_limit: parseInt(this.$data.numberAllowedItems),
          price_limit: parseInt(this.$data.allowedLimit),
          email_shopper: this.$data.emailConfirmation,
          email_campaign: true,
          checkout_fields: generateSchema(this.$data.fields),
          accounts: this.$data.accounts,
          message: this.$data.messageToUsers,
          departments: this.$data.departments,
          locations: this.$data.locations
        };
        axios
          .post(`/campaigns`, data, params)
          .then(resp => {
            this.$router.push(`/campaign_edit/${resp.data.id}/6`)
          })
          .catch(err => {
            console.log(err)
          })
      },

      addDepartmentStep() {
        function DepartmentStepConstructor() {
          this.name = 'Departments';
        }

        let departmentStep = new DepartmentStepConstructor();
        this.$data.stepArr.push(departmentStep);
        console.log(this.$data.stepArr);
      },

      addManagerStep() {
        function MnagerStepConstructor() {
          this.name = 'Managers'
        }

        let managerStep = new MnagerStepConstructor()
        this.$data.stepArr.push(managerStep)
      },

      removeDepartmentStep() {
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Departments');
        if (stepIndex) {
          this.$data.stepArr.splice(stepIndex, 1);
          console.log(this.$data.stepArr);
        }
      },
      removeManagerStep() {
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Managers');
        if (stepIndex) {
          this.$data.stepArr.splice(stepIndex, 1);
          console.log(this.$data.stepArr);
        }
      },
      addLocationStep() {
        function LocationStepConstructor() {
          this.name = 'Locations';
        }

        let locationStep = new LocationStepConstructor();
        this.$data.stepArr.push(locationStep);
        console.log(this.$data.stepArr);
      },

      removeLocationStep() {
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Locations');
        if (stepIndex) {
          this.$data.stepArr.splice(stepIndex, 1);
          console.log(this.$data.stepArr);
        }
      },

      setAdminAccount() {
        let account = {
          password: this.$data.adminPassword,
          role_id: 4
        };
        if (this.$data.adminUserName) {
          account.username = this.$data.adminUserName
        }
        if (this.$data.firstName) {
          account.first_name = this.$data.firstName
        }
        if (this.$data.lastName) {
          account.last_name = this.$data.lastName
        }
        if (this.$data.email) {
          account.email = this.$data.email
        }
        if (Object.keys(account).length > 2) {
          this.$data.accounts.push(account);
        }
      },

      setAccount () {
        let account = {
          password: this.$data.password,
          role_id: 5
        }
        if (this.$data.login) {
          account.username = this.$data.login
        }
        if (this.$data.password) {
          account.password = this.$data.password
        }
        if (Object.keys(account).length > 2) {
          this.$data.accounts.push(account)
        }
      },
      nextElement(i) {
        let stepArrLength = this.$data.stepArr.length
        if (stepArrLength > i) {
          return i + 1
        } else {
          return 1
        }
      },
      removeDepartment(index) {
        this.$data.departments.splice(index, 1);
      },
      removeManager(index) {
        this.$data.managers.splice(index, 1);
      },
      removeAdditionalField(index) {
        this.$data.formFieldsArr.splice(index, 1);
      },
      removeLocation(index) {
        this.$data.locations.splice(index, 1);
      },
      createDepartment() {
        function DepartmentConstructor() {
          this.name = "";
        }

        let department = new DepartmentConstructor();
        this.$data.departments.push(department);
        console.log(this.$data.departments);
      },
      createAdditionalField() {
        function AdditionalFiledConstructor() {
          this.name = "";
        }

        let additionalField = new AdditionalFiledConstructor();
        this.$data.formFieldsArr.push(additionalField);
        console.log(this.$data.formFieldsArr);
      },
      createLocation () {
        function LocationConstructor() {
          (this.nickname = ""),
            (this.company_name = ""),
            (this.street_and_number = ""),
            (this.city = ""),
            (this.zip_code = ""),
            (this.delivery_contact = ""),
            (this.suite_unit_etc = ""),
            (this.region = ""),
            (this.country = "");
        }

        let location = new LocationConstructor();
        this.$data.locations.push(location);
        console.log(this.$data.locations);
      },
      setLocations () {
        let location = {
          nickname: this.$data.locationName,
          company_name: this.$data.companyName,
          street_and_number: this.$data.street,
          city: this.$data.city,
          zip_code: this.$data.zipCode,
          delivery_contact: this.$data.delivery,
          suite_unit_etc: this.$data.building,
          region: this.$data.region,
          country: this.$data.country
        };
        this.$data.locations.push(location);
      },

      addFirstNameField () {
        let name = 'First Name';
        this.$data.fields.push(name);
        console.log(this.$data.fields)
      },
      removeFirstNameField () {
        let fieldIndex = this.fields.indexOf('First Name');
        this.$data.fields.splice(fieldIndex, 1);
        console.log(this.$data.fields);
      },
      addLastNameField () {
        let name = 'Last Name';
        this.$data.fields.push(name);
        console.log(this.$data.fields)
      },
      removeLastNameField() {
        let fieldIndex = this.fields.indexOf('Last Name');
        this.$data.fields.splice(fieldIndex, 1);
        console.log(this.$data.fields);
      },
      addCompanyEmailField () {
        let name = 'Company Email';
        this.$data.fields.push(name);
        console.log(this.$data.fields)
      },
      removeCompanyEmailField () {
        let fieldIndex = this.fields.indexOf('Company Email');
        this.$data.fields.splice(fieldIndex, 1);
        console.log(this.$data.fields);
      }
    }
  };
</script>
