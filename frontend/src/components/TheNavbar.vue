<template>
  <v-navigation-drawer
    clipped
    app
    :value="drawer"
    @input="updateDrawer"
  >
    <v-list>

      <div v-if="navbarRoles.full.includes(roleName)">
        <v-list-tile active-class="" :to="'/admin'">
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-group prepend-icon="" no-action>
          <v-list-tile slot="activator">
            <v-list-tile-title>Reports</v-list-tile-title>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Campaign Product List'">
            <v-list-tile-content>
              <v-list-tile-title>Campaign Product List</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Sales Executives\' Shopper'">
            <v-list-tile-content>
              <v-list-tile-title>Sales Executives' Shopper</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Payroll Deduction'">
            <v-list-tile-content>
              <v-list-tile-title>Payroll Deduction</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Shopper Summary'">
            <v-list-tile-content>
              <v-list-tile-title>Shopper Summary</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Itemized Shopper'">
            <v-list-tile-content>
              <v-list-tile-title>Itemized Shopper</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Bin'">
            <v-list-tile-content>
              <v-list-tile-title>Bin</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Label Report'">
            <v-list-tile-content>
              <v-list-tile-title>Label Report</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Pick, Pack and Bag'">
            <v-list-tile-content>
              <v-list-tile-title>Pick, Pack and Bag</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Decorator PO'">
            <v-list-tile-content>
              <v-list-tile-title>Decorator PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Vendor PO'">
            <v-list-tile-content>
              <v-list-tile-title>Vendor PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Location PO'">
            <v-list-tile-content>
              <v-list-tile-title>Location PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>

        <v-divider></v-divider>
        <v-subheader class="text--lighten-1">Catalog</v-subheader>
        <v-list-tile active-class="" :to="'/admin/products'">
          <v-list-tile-content>
            <v-list-tile-title>Products</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/product_types'"
                     v-if="roleName === 'Super Admin'">
          <v-list-tile-content>
            <v-list-tile-title>Product types</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/product_attributes'"
                     v-if="roleName === 'Super Admin'">
          <v-list-tile-content>
            <v-list-tile-title>Attributes</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/campaigns'">
          <v-list-tile-content>
            <v-list-tile-title>Campaigns</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          active-class=""
          :to="'/admin/vendors'"
          v-if="~['Super Admin','Distributor Manager'].indexOf(roleName)"
        >
          <v-list-tile-content>
            <v-list-tile-title>Vendors</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>People Management</v-subheader>
        <v-list-tile active-class="" :to="'/admin/distributors'"
                     v-if="~['Super Admin', 'Distributor Manager'].indexOf(roleName)">
          <v-list-tile-content>
            <v-list-tile-title>Distributors</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/accounts'">
          <v-list-tile-content>
            <v-list-tile-title>User Accounts</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>Order Management</v-subheader>
        <v-list-tile active-class="" :to="'/admin/orders'">
          <v-list-tile-content>
            <v-list-tile-title>Orders</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>Controls</v-subheader>
        <v-list-tile active-class="" @click="logout">
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </div>

      <div v-if="navbarRoles.salesExecutive.includes(roleName)">
        <v-list-tile active-class="" :to="'/admin'">
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-group
          prepend-icon=""
          no-action>
          <v-list-tile slot="activator">
            <v-list-tile-title>Reports</v-list-tile-title>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Campaign Product List'">
            <v-list-tile-content>
              <v-list-tile-title>Campaign Product List</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Sales Executives\' Shopper'">
            <v-list-tile-content>
              <v-list-tile-title>Sales Executives\' Shopper</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Payroll Deduction'">
            <v-list-tile-content>
              <v-list-tile-title>Payroll Deduction</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Shopper Summary'">
            <v-list-tile-content>
              <v-list-tile-title>Shopper Summary</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Itemized Shopper'">
            <v-list-tile-content>
              <v-list-tile-title>Itemized Shopper</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Bin'">
            <v-list-tile-content>
              <v-list-tile-title>Bin</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Label Report'">
            <v-list-tile-content>
              <v-list-tile-title>Label Report</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Pick, Pack and Bag'">
            <v-list-tile-content>
              <v-list-tile-title>Pick, Pack and Bag</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Decorator PO'">
            <v-list-tile-content>
              <v-list-tile-title>Decorator PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Vendor PO'">
            <v-list-tile-content>
              <v-list-tile-title>Vendor PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Location PO'">
            <v-list-tile-content>
              <v-list-tile-title>Location PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>

        <v-divider></v-divider>
        <v-subheader>Catalog</v-subheader>
        <v-list-tile active-class="" :to="'/admin/products'">
          <v-list-tile-content>
            <v-list-tile-title>Products</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/campaigns'">
          <v-list-tile-content>
            <v-list-tile-title>Campaigns</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>People Management</v-subheader>
        <v-list-tile active-class="" :to="'/admin/distributors'" v-if="roleName == 'Super Admin'">
          <v-list-tile-content>
            <v-list-tile-title>Distributors</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/admin/accounts'">
          <v-list-tile-content>
            <v-list-tile-title>User Accounts</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>Order Management</v-subheader>
        <v-list-tile active-class="" :to="'/admin/orders'">
          <v-list-tile-content>
            <v-list-tile-title>Orders</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider></v-divider>
        <v-subheader>Controls</v-subheader>
        <v-list-tile active-class="" @click="logout">
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </div>

      <div v-else-if="navbarRoles.adminBuyer.includes(roleName)">
        <v-list-tile active-class="" :to="'/'">
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-group
          prepend-icon=""
          no-action>
          <v-list-tile slot="activator">
            <v-list-tile-title>Reports</v-list-tile-title>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Payroll Deduction'">
            <v-list-tile-content>
              <v-list-tile-title>Payroll Deduction</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Shopper Summary'">
            <v-list-tile-content>
              <v-list-tile-title>Shopper Summary</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Itemized Shopper'">
            <v-list-tile-content>
              <v-list-tile-title>Itemized Shopper</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile active-class="" @click="reportClick" :to="'/admin/report?report=Location PO'">
            <v-list-tile-content>
              <v-list-tile-title>Location PO</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>
        <v-list-tile active-class="" @click="logout">
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </div>

      <div v-else-if="navbarRoles.shopper.includes(roleName)">
        <v-list-tile active-class="" :to="'/'">
          <v-list-tile-content>
            <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" :to="'/cart'">
          <v-list-tile-content>
            <v-list-tile-title>Cart</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile active-class="" @click="logout">
          <v-list-tile-content>
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </div>


    </v-list>
  </v-navigation-drawer>
</template>


<script>
  export default {
    props: {
      'drawer': Boolean,
      'updateDrawer': Function,
    },

    computed: {
      roleName() {
        return this.$store.state.account.role.name;
      },
    },

    data() {
      return {
        navbarRoles: {
          full: ['Super Admin', 'Distributor Manager'],
          salesExecutive: ['Sales Executive'],
          adminBuyer: ['Admin Buyer'],
          shopper: ['Shopper']
        }
      }
    },

    methods: {
      reportClick() {
        // dirty fix for reload report tabs
        this.$parent.$children[2].$children[0].campaign = null
        this.$parent.$children[2].$children[0].report = {
          meta: null,
          data: null
        }

      },
      async logout() {
        try {
          this.$store.dispatch('logout');
          this.$router.push('/login');
        } catch (err) {
          console.log(err);
        }
      }
    }
  }
</script>
