<template>
  <v-stepper v-model="e1" non-linear>
    <v-stepper-header style="height: 100%">
      <template v-for="(item, index) in stepArr">
        <v-stepper-step :complete="e1 > index + 1" :step="index + 1" editable>{{item.name}}</v-stepper-step>
        <v-divider></v-divider>
      </template>
    </v-stepper-header>

    <v-stepper-items>
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
          <v-text-field v-model="companyName" :rules="companyRules" label="Company Name" required></v-text-field>
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
                label="Start Date"
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
                label="End Date"
                prepend-icon="event"
                readonly
                :rules="dateTimeRules"
                required
              ></v-text-field>
              <v-date-picker v-model="endDate" @input="endDateInput = false"></v-date-picker>
            </v-menu>
          </v-flex>
        </v-form>
        <v-btn color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn color="primary" @click="submit">Save Changes</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>
      <v-stepper-content step="2">
        <h2>Shopper Account</h2>
        <v-form px-2 v-model="validShopperAccount">
          <v-text-field v-model="shopperAccount.username" :rules="loginRules" label="Login" required></v-text-field>
          <v-text-field v-model="password" label="New Password"
                        type="password" ></v-text-field>

        </v-form>
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="saveShopperAccount" :disabled="!validShopperAccount">Save Account Changes</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn color="primary" @click="submit">Save Changes</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>
      <v-stepper-content step="3">
        <h2>Admin Buyer Edit</h2>
        <v-form px-2 v-model="validAdminAccount">
          <v-text-field v-model="adminAccount.first_name" :rules="nameRules" label="First Name" required></v-text-field>
          <v-text-field v-model="adminAccount.last_name" :rules="nameRules" label="Last Name" required></v-text-field>
          <v-text-field v-model="adminAccount.username" :rules="adminLoginRules" label="User Name" required></v-text-field>
          <v-text-field v-model="adminAccount.email" :rules="emailRules" label="E-mail" required></v-text-field>
          <v-switch label="Allow buyer to see reports" v-model="switchPassword"></v-switch>
          <v-text-field v-model="adminPassword" v-if="switchPassword" label="New Password" type="password"
                         required></v-text-field>
        </v-form>
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="saveAdminAccount" :disabled="!validAdminAccount">Save Account Changes</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)">Next</v-btn>


        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>



      <v-stepper-content step="4">
        <h2>Campaign Setup</h2>
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
                    <div>Enter Shopper Allowance</div>
                    <v-text-field
                      v-model="companyAllowanceData"
                      :rules="nameRules"
                      label="$"
                    ></v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-checkbox label="Allow shoppers to personally pay for allowance overages" v-model="companyAllowanceCheckbox"></v-checkbox>
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
                <div>Enter number of items allowed per person</div>
                <v-text-field
                  v-model="numberAllowedItems"
                  label="#"
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
                  label="$"
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
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content step="5">
        <h2>Shopper Checkout Information</h2>
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
                <v-btn @click="createAdditionalField('')">
                  add new field
                </v-btn>
                <div v-for="(item, index) in formFieldsArr" px-2 v-model="valid" :key="item.index">
                  <h2>Additional Field N{{index + 1}}</h2>
                  <v-text-field v-model="item.name" :rules="nameRules" label="New Field" required></v-text-field>
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
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn color="primary" @click="submit">Save Changes</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsDepartment" :step="stepArr.findIndex(x => x.name === 'Departments')+1">
        <v-btn @click="createDepartment">Add Department</v-btn>
        <v-form v-for="(item, index) in departments" px-2 v-model="valid" :key="item.index">
          <h2>Department N{{index + 1}}</h2>
          <v-text-field v-model="item.name" :rules="nameRules" label="Department" required></v-text-field>
          <v-btn @click="saveDepartment(item)">Save</v-btn>
          <v-btn @click="removeDepartment(item, index)">Remove</v-btn>
        </v-form>
        <v-form v-for="(item, index) in newDepartments" px-2 v-model="valid" :key="item.index">
          <h2>New Department N{{index + 1}}</h2>
          <v-text-field v-model="item.name" :rules="nameRules" label="Department" required></v-text-field>
          <v-btn @click="saveNewDepartment(item)">Save New Department</v-btn>
          <v-btn @click="removeNewDepartment(index)">Cancel</v-btn>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn color="primary" @click="submit">Save Changes</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsLocation" :step="stepArr.findIndex(x => x.name === 'Location')+1">
        <v-btn @click="createLocation">Add New Location</v-btn>
        <v-form v-for="(item, index) in locations" px-2 v-model="valid" :key="item.index">
          <h2>Location N{{index + 1}}</h2>
          <v-layout>
            <v-flex mr-2>
              <v-text-field
                v-model="item.nickname"
                :rules="nameRules"
                label="Location Name"
                required
              ></v-text-field>
              <v-text-field v-model="companyName" :rules="nameRules" label="Company Name" required></v-text-field>
              <v-text-field
                v-model="item.street_and_number"
                :rules="addressRules"
                label="Street and number"
                required
              ></v-text-field>
              <v-text-field v-model="item.city" :rules="nameRules" label="City" required></v-text-field>
              <v-text-field v-model="item.zip_code" :rules="nameRules" label="Zip Code" required></v-text-field>
            </v-flex>
            <v-flex>
              <v-text-field
                v-model="item.delivery_contact"
                :rules="nameRules"
                label="Attention/Delivery Contact"
                required
              ></v-text-field>
              <v-text-field
                v-model="item.suite_unit_etc"
                :rules="nameRules"
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
          <v-btn @click="saveLocation(item)">Save</v-btn>
          <v-btn @click="removeLocation(item, index)">Remove</v-btn>
        </v-form>
        <v-form v-for="(item, index) in newLocations" px-2 v-model="valid" :key="item.index">
          <h2>New Location N{{index + 1}}</h2>
          <v-layout>
            <v-flex mr-2>
              <v-text-field
                v-model="item.nickname"
                :rules="nameRules"
                label="Location Name"
                required
              ></v-text-field>
              <v-text-field v-model="companyName" :rules="nameRules" label="Company Name" required></v-text-field>
              <v-text-field
                v-model="item.street_and_number"
                :rules="nameRules"
                label="Street and number"
                required
              ></v-text-field>
              <v-text-field v-model="item.city" :rules="nameRules" label="City" required></v-text-field>
              <v-text-field v-model="item.zip_code" :rules="nameRules" label="Zip Code" required></v-text-field>
            </v-flex>
            <v-flex>
              <v-text-field
                v-model="item.delivery_contact"
                :rules="nameRules"
                label="Attention/Delivery Contact"
                required
              ></v-text-field>
              <v-text-field
                v-model="item.suite_unit_etc"
                :rules="nameRules"
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
          <v-btn @click="saveNewLocation(item)">Save</v-btn>
          <v-btn @click="removeNewLocation(index)">Cancel</v-btn>
        </v-form>


        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <v-btn color="primary" @click="submit">Save Changes</v-btn>
        <v-btn flat @click="$router.push('/campaigns')">Cancel</v-btn>
        <v-btn @click="$router.push(`/product_setup/${$route.params.id}`)">Add Product</v-btn>
      </v-stepper-content>

      <v-stepper-content v-if="formFieldsManager" :step="stepArr.findIndex(x => x.name === 'Managers')+1">
        <v-btn @click="createManager" v-if="!managers[0]">Add Manager</v-btn>

        <v-form v-for="(item, index) in managersAccounts" px-2 :key="item.index">
          <h2>Manager N {{index + 1}}</h2>
          <v-text-field v-model="item.first_name" :rules="nameRules" label="First Name" required></v-text-field>
          <v-text-field v-model="item.email" :rules="emailRules" label="Email" required></v-text-field>
          <v-btn @click="deleteExistingManagerAccount(item.id, index)">Remove</v-btn>
          <v-btn @click="saveExistingManagerAccount(item)">Save Changes</v-btn>
          <v-btn @click="createManager">Add Manager</v-btn>
        </v-form>

        <v-form v-for="(item, index) in managers" px-2 v-model="valid" :key="item.index">
          <h2>New Manager N {{index + 1}}</h2>
          <v-text-field v-model="item.first_name" :rules="nameRules" label="First Name" required></v-text-field>
          <v-text-field v-model="item.email" :rules="emailRules" label="Email" required></v-text-field>
          <v-btn @click="removeManager(index)">Remove</v-btn>
          <v-btn @click="saveNewManagerAccount(item, index)">Save New Account</v-btn>
          <v-btn @click="createManager">Add Manager</v-btn>
        </v-form>

        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
      </v-stepper-content>

      <v-stepper-content :step="stepArr.findIndex(x => x.name === 'Products')+1">
        <v-btn @click="showAddExistingProduct = !showAddExistingProduct">Add Existing Product</v-btn>
        <v-btn @click="showAddNewProduct = !showAddNewProduct">Add New Product</v-btn>
        <v-btn @click="showProducts = !showProducts">show/hide products</v-btn>
        <v-btn @click="deleteAllVariants"> Delete all Products</v-btn>
        <v-btn @click="$router.push(`/storefront_preview/${$route.params.id}`)"> Storefront Preview</v-btn>
        <v-btn color="#0A0B0A" dark @click="e1 -= 1">Back</v-btn>
        <v-btn v-if="e1 < stepArr.length" color="primary" @click="e1 = nextElement(e1)">Next</v-btn>
        <div v-if="showAddNewProduct">
          <ProductSetup/>
        </div>
        <div v-if="showAddExistingProduct">
          <ProductSetUpNew/>
        </div>
      </v-stepper-content>
    </v-stepper-items>
    <v-layout align-start justify-center row fill-height wrap
    v-if="showProducts">
      <v-flex v-for="(item, index) in productVariants" :key='index' ma-2 xs3>
        <v-card>
          <v-card-text>
            <v-img
              contain
              :src="getImg(item)"
            ></v-img>
            <v-card-title primary-title>
              <v-layout align-start justify-center column fill-height>
                <div>
                  <h3>{{item.product.name}} ({{item.price.toFixed(2)}}$)</h3>
                </div>
                <h3
                  v-for="(attribute) in item.attributes"
                >
                  {{attribute.name}}: {{attribute.value}}
                </h3>
              </v-layout>
            </v-card-title>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="deleteProductVariant(item.id, index)">
              Delete
            </v-btn>
            <v-btn @click="$router.push('/edit_images_variant/'+ item.id)">
              Custom Img
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-stepper>
</template>

<script>
  import axios from "@/axios";
  import moment from 'moment'
  import ProductSetup from './ProductSetup.vue'
  import ProductSetUpNew from './ProductSetUpNew.vue'
  const emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
  const usernameRegex =/^[A-Za-z0-9]+(?:[ ._-][A-Za-z0-9]+)*$/
  const companyRegex =/^([a-zA-Z0-9]|[- @\.#&!'])*$/
  const addressRegex =/^([a-zA-Z0-9]|[/№ #.])*$/
  const nameRegex =/^[a-z A-Z0-9]+$/
  const numberNameRegexZip =/^[a-z A-Z0-9-]+$/
  const numberNameRegex =/^[a-z A-Z0-9]+$/
  const numberRegex =/^[0-9]+$/

  export default {
    data() {
      return {
        messageToUsers: '',
        adminAccount: {},
        managers: [],
        managersAccounts: [],
        shopperAccount: {
          role_id: 5
        },
        showAddNewProduct: false,
        showAddExistingProduct: false,
        stepArr: [
          {
            name: 'Campaign'
          },
          {
            name: 'Shopper'
          },
          {
            name: 'Admin Buyer'
          },
          {
            name: 'Features'
          },
          {
            name: 'Checkout Info'
          },
          {
            name: 'Products'
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

        checkout_fields: null,

        token:
          "Bearer" + " " + localStorage.getItem("user").replace(/['"]+/g, ""),
        validExtraFeatures: false,
        validAdminAccount: false,
        validShopperAccount: false,
        e1: 0,
        valid: false,
        distributor_id: '',
        adminAccountId: '',
        shopperAccountId: '',
        accounts: [],
        departments: [],
        newDepartments: [],
        locations: [],
        newLocations: [],
        switchPassword: false,
        startDate: "",
        endDate: "",
        startDateInput: false,
        endDateInput: false,
        campaignName: "",
        login: "",
        password: "",
        adminUserName: "",
        adminPassword: "",
        firstName: "",
        lastName: "",
        companyName: "",
        email: "",
        productVariants: [],
        showProducts: false,
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
        ]
      };
    },
    mounted () {
      axios.get(`/campaigns/${this.$route.params.id}`, {
        headers: {
          'Authorization': 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, ''),
          'X-Fields': '*,product_variants{*,product{*}}'
        }
      }).then(resp => {
        this.$data.e1 = this.$route.params.tab
        this.accountsFilter(resp.data.accounts)
        this.$data.messageToUsers = resp.data.message
        this.$data.productVariants = resp.data.product_variants
        this.$data.campaignName = resp.data.name
        this.$data.companyName = resp.data.company_name
        this.$data.startDate = resp.data.start_date
        this.$data.endDate = resp.data.end_date
        this.$data.storefrontPricing = resp.data.storefront_pricing
        this.$data.distributor_id = resp.data.distributor_id
        if (resp.data.company_allowance){
          this.$data.companyAllowance = true
          this.$data.companyAllowanceData = resp.data.company_allowance
        }
        if (resp.data.items_count_limit){
          this.$data.limitShoppingCart = true
          this.$data.numberAllowedItems = resp.data.items_count_limit
        }
        if (resp.data.price_limit){
          this.$data.cartAmount = true
          this.$data.allowedLimit = resp.data.price_limit
        }
        this.$data.emailConfirmation = resp.data.email_shopper
        this.$data.accounts = resp.data.accounts
        if (resp.data.departments.length > 0) {
          this.$data.formFieldsDepartment = true
          this.$data.departments = resp.data.departments
        }
        if (resp.data.locations.length > 0) {
          this.$data.formFieldsLocation = true
          this.$data.locations = resp.data.locations
        }
        if (this.$data.managersAccounts.length > 0) {
          this.$data.formFieldsManager = true
        }
        this.$data.checkout_fields = resp.data.checkout_fields
        if (this.$data.checkout_fields.required.indexOf('First Name') >= 0) {
          this.$data.formFieldsFirstName = true
        }
        if (this.$data.checkout_fields.required.indexOf('Last Name') >= 0) {
          this.$data.formFieldsLastName = true
        }
        if (this.$data.checkout_fields.required.indexOf('Company Email') >= 0) {
          this.$data.formFieldsCompanyEmail = true
        }
        if (this.$data.checkout_fields.required.indexOf('Manager') >= 0) {
          this.$data.formFieldsManager = true
        }
        // Determine custom fields
        let customFields = Object.keys(this.$data.checkout_fields.properties)
        let predefinedFields = ['First Name', 'Last Name', 'Company Email', 'Manager']
        customFields = customFields.filter(x => predefinedFields.indexOf(x) === -1)
        // Add custom fields to list
        customFields.forEach(x => {
          this.createAdditionalField(x)
        })
        // Enable custom fields trigger if exist
        if (customFields.length !== 0) {
          this.$data.formFieldsIdentifier = true
        }
        this.$data.e1 = this.$route.params.tab
      }).catch(err => {
        this.errors.push(err)
      })
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
      e1: function (){
        if (this.$data.e1 === 6){
          this.$router.push(`/campaign_edit/${this.$route.params.id}/${this.$data.e1}`)
          this.$data.showProducts = true
        } else {
          this.$data.showProducts = false
        }
      },
      startDate: function (){
        this.$data.startDate = moment(this.$data.startDate).format('YYYY-MM-DD')
      },
      endDate: function (){
        this.$data.endDate = moment(this.$data.endDate).format('YYYY-MM-DD')
      },
      adminPassword: function () {
        if (this.$data.adminPassword) {
          this.$data.switchPassword = true
        }
      },

      formFieldsFirstName: function (){
        if (this.formFieldsFirstName){
          this.addFirstNameField()
        } else {
          this.removeFirstNameField()
        }
      },
      formFieldsLastName: function (){
        if (this.formFieldsLastName){
          this.addLastNameField()
        } else {
          this.removeLastNameField()
        }
      },
      formFieldsCompanyEmail: function (){
        if (this.formFieldsCompanyEmail){
          this.addCompanyEmailField()
        } else {
          this.removeCompanyEmailField()
        }
      },
      // formFieldsManager: function (){
      //   if (this.formFieldsManager){
      //     this.addManagerField()
      //   } else {
      //     this.removeManagerField()
      //   }
      // },

      formFieldsDepartment: function (){
        if (this.formFieldsDepartment){
          this.addDepartmentStep()
        } else {
          this.removeDepartmentStep()
        }
      },

      formFieldsLocation: function (){
        if (this.formFieldsLocation){
          this.addLocationStep()
        } else {
          this.removeLocationStep()
        }
      },
      formFieldsManager: function () {
        if (this.formFieldsManager) {
          this.addManagerStep()
        } else {
          this.removeManagerStep()
        }
      },
    },

    methods: {
      deleteAllVariants () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = {
          product_variants: []
        };
        axios
          .put(`/campaigns/${this.$route.params.id}`, data, params)
          .then(resp => {
            this.$data.productVariants = []
          })
          .catch(err => {
            console.log(err);
          });
      },
      deleteExistingManagerAccount (id, index) {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        axios
          .delete(`/accounts/${id}`, params)
          .then(resp => {
            this.$data.managersAccounts.splice(index, 1);
          })
          .catch(err => {
            console.log(err);
          });
      },
      saveNewManagerAccount (manager, index) {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = {}
        data.first_name = manager.first_name
        data.email = manager.email
        data.campaign_id = parseFloat(this.$route.params.id)
        data.role_id = 6
        axios
          .post(`/accounts`, data, params)
          .then(resp => {
            this.$data.managersAccounts.push(resp.data)
            this.$data.managers.splice(index, 1);
          })
          .catch(err => {
            console.log(err);
          });
      },
      saveExistingManagerAccount (manager) {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = {}
        data.first_name = manager.first_name
        data.email = manager.email
        axios
          .put(`/accounts/${manager.id}`, data, params)
          .then(resp => {
          })
          .catch(err => {
            console.log(err);
          });
      },
      removeManager(index) {
        this.$data.managers.splice(index, 1);
      },
      createManager() {
        function ManagerConstructor() {
          this.first_name = ''
          this.email = ''
          this.role_id = 6
        }

        let manager = new ManagerConstructor();
        this.$data.managers.push(manager);
      },
      addManagerStep() {
        function MnagerStepConstructor() {
          this.name = 'Managers'
        }

        let managerStep = new MnagerStepConstructor()
        this.$data.stepArr.splice(this.$data.stepArr.length-1, 0, managerStep)
      },
      removeManagerStep() {
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Managers');
        if (stepIndex) {
          this.$data.stepArr.splice(stepIndex, 1);
        }
      },
      accountsFilter (accounts) {
        accounts.forEach((val) => {
          if (val.role_id === 4) {
            this.$data.adminAccount.first_name = val.first_name
            this.$data.adminAccount.last_name = val.last_name
            this.$data.adminAccount.username = val.username
            this.$data.adminAccount.id = val.id
            this.$data.adminAccount.email = val.email
            this.$data.adminAccount.role_id = val.role_id
            this.$data.adminAccount.campaign_id = val.campaign_id
          }
          if (val.role_id === 5) {
            this.$data.shopperAccount.username = val.username
            this.$data.shopperAccount.id = val.id
            this.$data.shopperAccount.role_id = val.role_id
            this.$data.shopperAccount.campaign_id = val.campaign_id
          }
          if (val.role_id === 6) {
            this.$data.managersAccounts.push(val)
          }
        })
      },
      deleteProductVariant(id, index){
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        axios.delete(`/products/variants/${id}`, params).then(resp => {
          this.$data.productVariants.splice(index, 1)
        }).catch(err => {
          console.log(err)
        })
      },
      saveAdminAccount() {
        if (this.$data.adminAccount.id) {
          this.saveExistingAdminAccount()
        } else {
          this.saveNewAdminAccount()
        }
      },
      saveExistingAdminAccount () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = this.$data.adminAccount
        data.password = this.$data.adminPassword
        axios
          .put(`/accounts/${this.$data.adminAccount.id}`, data, params)
          .then(resp => {
          })
          .catch(err => {
            console.log(err);
          });
      },
      saveNewAdminAccount () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = this.$data.adminAccount
        data.password = this.$data.adminPassword
        data.campaign_id = parseFloat(this.$route.params.id)
        data.role_id = 4
        axios
          .post(`/accounts`, data, params)
          .then(resp => {
          })
          .catch(err => {
            console.log(err);
          });
      },
      saveShopperAccount() {
        if (this.$data.shopperAccount.id) {
          this.saveExistingShopperAccount()
        } else {
          this.saveNewShopperAccount()
        }
      },
      saveExistingShopperAccount () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = this.$data.shopperAccount
        data.password = this.$data.password
        axios
          .put(`/accounts/${this.$data.shopperAccount.id}`, data, params)
          .then(resp => {
          })
          .catch(err => {
            console.log(err);
          });
      },
      saveNewShopperAccount () {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = this.$data.shopperAccount
        data.password = this.$data.password
        data.campaign_id = parseFloat(this.$route.params.id)
        axios
          .post(`/accounts`, data, params)
          .then(resp => {
          })
          .catch(err => {
            console.log(err);
          });
      },
      submit() {

        // Extend default fields with custom
        this.$data.formFieldsArr.forEach(f => {
          if (this.$data.fields.indexOf(f.name) === -1) {
            this.$data.fields.push(f.name)
          }
        })

        function generateSchema(fields) {
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
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        };
        let data = {
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
          message: this.$data.messageToUsers
        };
        axios
          .put(`/campaigns/${this.$route.params.id}`, data, params)
          .then(resp => {
            this.$router.push(`/campaigns`);
          })
          .catch(err => {
            console.log(err);
          });
      },

      addDepartmentStep() {
        function DepartmentStepConstructor() {
          this.name = 'Departments';
        }
        let departmentStep = new DepartmentStepConstructor();
        this.$data.stepArr.splice(this.$data.stepArr.length-1, 0, departmentStep)
      },

      removeDepartmentStep(){
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Departments');
        if (stepIndex){
          this.$data.stepArr.splice(stepIndex, 1);
        }
      },


      addLocationStep() {
        function LocationStepConstructor() {
          this.name = 'Location';
        }
        let locationStep = new LocationStepConstructor();
        this.$data.stepArr.splice(this.$data.stepArr.length-1, 0, locationStep)
      },

      removeLocationStep(){
        let stepIndex = this.stepArr.findIndex(x => x.name === 'Location');
        if (stepIndex){
          this.$data.stepArr.splice(stepIndex, 1);
        }
      },

      setAccounts() {
        let account = {
          username: this.$data.login,
          password: this.$data.password,
          email: this.$data.email,
          first_name: this.$data.firstName,
          last_name: this.$data.lastName,
          role_id: 4
        };
        this.$data.accounts = []
        this.$data.accounts.push(account);
      },
      nextElement(i){
        let stepArrLength = this.$data.stepArr.length
        if (stepArrLength > i){
          return i + 1
        } else {
          return 1
        }
      },
      saveDepartment(department){
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        let data = {
          name: department.name
        }
        axios.put(`/departments/${department.id}`, data, params).then(resp => {
        }).catch(err => {
          console.log(err)
        })
      },

      removeDepartment(department, index) {
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        axios.delete(`/departments/${department.id}`, params).then(resp => {
          this.$data.departments.splice(index, 1);
        }).catch(err => {
          console.log(err)
        })
      },
      saveLocation(location){
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        let data = {
          nickname: location.nickname,
          company_name: location.company_name,
          street_and_number: location.street_and_number,
          city: location.city,
          zip_code: location.zip_code,
          delivery_contact: location.delivery_contact,
          suite_unit_etc: location.suite_unit_etc,
          region: location.region,
          country: location.country,
          campaign_id: location.campaign_id
        }
        axios.put(`/locations/${location.id}`, data, params).then(resp => {
        }).catch(err => {
          console.log(err)
        })
      },
      removeLocation(location, index) {
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        axios.delete(`/locations/${location.id}`, params).then(resp => {
          this.$data.locations.splice(index, 1);
        }).catch(err => {
          console.log(err)
        })
      },

      saveNewLocation(newLocation){
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        let data = {
          nickname: newLocation.nickname,
          company_name: newLocation.company_name,
          street_and_number: newLocation.street_and_number,
          city: newLocation.city,
          zip_code: newLocation.zip_code,
          delivery_contact: newLocation.delivery_contact,
          suite_unit_etc: newLocation.suite_unit_etc,
          region: newLocation.region,
          country: newLocation.country,
          campaign_id: parseInt(this.$route.params.id)
        }
        axios.post(`/locations`, data, params).then(resp => {
        }).catch(err => {
          console.log(err)
        })
      },

      removeNewLocation(index) {
        this.$data.newLocations.splice(index, 1);
      },

      removeAdditionalField(index) {
        this.$data.formFieldsArr.splice(index, 1);
      },
      createDepartment() {
        function DepartmentConstructor() {
          this.name = "";
        }

        let department = new DepartmentConstructor();
        this.$data.newDepartments.push(department);
      },

      removeNewDepartment(index) {
        this.$data.newDepartments.splice(index, 1);
      },

      saveNewDepartment(newDepartment){
        let params = { headers: {
            'Authorization': this.$data.token,
          }}
        let data = {
          name: newDepartment.name,
          campaign_id: parseInt(this.$route.params.id)
        }
        axios.post(`/departments`, data, params).then(resp => {
        }).catch(err => {
          console.log(err)
        })
      },

      createAdditionalField(name) {
        function AdditionalFiledConstructor() {
          this.name = name || "";
        }

        let additionalField = new AdditionalFiledConstructor();
        this.$data.formFieldsArr.push(additionalField);
      },
      createLocation() {
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
        this.$data.newLocations.push(location);
      },
      setLocations() {
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

      addFirstNameField() {
        let name = 'First Name';
        this.$data.fields.push(name);
      },
      removeFirstNameField(){
        let fieldIndex = this.fields.indexOf('First Name');
        this.$data.fields.splice(fieldIndex, 1);
      },
      addLastNameField() {
        let name = 'Last Name';
        this.$data.fields.push(name);
      },
      removeLastNameField(){
        let fieldIndex = this.fields.indexOf('Last Name');
        this.$data.fields.splice(fieldIndex, 1);
      },
      addCompanyEmailField() {
        let name = 'Company Email';
        this.$data.fields.push(name);
      },
      removeCompanyEmailField(){
        let fieldIndex = this.fields.indexOf('Company Email');
        this.$data.fields.splice(fieldIndex, 1);
      },
      addManagerField() {
        let name = 'Manager';
        this.$data.fields.push(name);
      },
      removeManagerField(){
        let fieldIndex = this.fields.indexOf('Manager');
        this.$data.fields.splice(fieldIndex, 1);
      },
      getImg (item) {
        let defaultImg = `${process.env.API_BASE_URL}/static/default-product.svg`
        if (item.resources[0])
          return `${process.env.API_BASE_URL}/static/resources/${item.resources[0].uuid}.${item.resources[0].type}`
          else if (item.product.resources[0]){
          return `${process.env.API_BASE_URL}/static/resources/${item.product.resources[0].uuid}.${item.product.resources[0].type}`
          }
        else
          return defaultImg
      }
    },
    components: {
      ProductSetup,
      ProductSetUpNew
    }
  }
</script>


<style>
.file-select {
  width: 0.1px;
	height: 0.1px;
	opacity: 0;
	overflow: hidden;
	position: absolute;
	z-index: -1;
}
</style>
