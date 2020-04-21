<template>
  <v-container fluid grid-list-xl>
    <v-layout row wrap>
      <v-flex xs9>
        <v-data-table
          :loading="itemsPending"
          :no-data-text="itemsPending ? 'Loading... Please wait' : 'No data available'"
          :headers="headers"
          :items="items"
          class="elevation-1"
          :rows-per-page-items="[25]"
          :hide-actions="items.length < 50"
        >
          <template slot="items" slot-scope="data">
            <tr @click="redirect('/admin/accounts/' + data.item._jv.id)">
              <td>{{ data.item._jv.id }}</td>
              <td>
                <div class="clip">{{ data.item.username }}</div>
              </td>
              <td>
                <div class="clip">{{ data.item.distributor ? data.item.distributor.name || 'N/A' : 'N/A' }}</div>
              </td>
              <td>
                <div class="clip">{{ data.item.campaign_id ? data.item.campaigns[data.item.campaign_id].name || 'N/A' : 'N/A' }}</div>
              </td>
              <td>{{ data.item.role_id ? possibleRolesObject[data.item.role_id].name || 'N/A' : 'N/A' }}</td>
              <td>
                <v-switch
                  class=""
                  v-model="data.item.active"
                  style="height:24px"
                  @click.prevent.stop.capture="updateAccount(data.item)"
                >
                </v-switch>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-flex>
      <v-flex xs3>
        <v-card>
          <v-card-title>
            <div>
              <h3 class="headline mb-2">Filters</h3>
            </div>
          </v-card-title>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="filters.username"
                label="Username"
                v-on:keyup="applyFilter">
              </v-text-field>
              <v-text-field
                v-model="filters.email"
                label="Email"
                v-on:keyup="applyFilter">
              </v-text-field>
              <v-text-field
                v-model="filters.distributor"
                label="Distributor"
                v-on:keyup="applyFilter">
              </v-text-field>
              <v-text-field
                v-model="filters.campaign"
                label="Campaign"
                v-on:keyup="applyFilter">
              </v-text-field>
              <v-select
                v-model="filters.role"
                :loading="possibleRolesPending"
                :items="possibleRoles"
                :clearable="true"
                label="Role"
                v-on:change="applyFilter"
                item-text="name"
                item-value="name"
              >
              </v-select>
              <v-select
                v-model="filters.active"
                :items="[{label: 'Yes', value: true},{label: 'No', value: false}]"
                :clearable="true"
                label="Active"
                item-text="label"
                item-value="value"
                v-on:change="applyFilter">
              </v-select>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-btn
      v-if="['Super Admin', 'Distributor Manager'].includes($store.state.account.role.name)"
      color="primary"
      fab
      fixed
      bottom
      right
      @click="$router.push('/admin/accounts/add')"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
  import _ from 'lodash';

  export default {
    data() {
      return {

        // Table
        headers: [
          { text: 'ID', value: '_jv.id' },
          { text: 'Username', value: 'username' },
          { text: 'Distributor', value: 'distributor.name' },
          { text: 'Campaign', sortable: false, value: 'campaign.name' },
          { text: 'Role', value: 'role.name' },
          { text: 'Active', value: 'active' },
        ],
        items: [],
        itemsPending: true,

        // Filters
        possibleRoles: [],
        possibleRolesObject: {},
        possibleRolesPending: true,

        filters: {
          username: '',
          email: '',
          distributor: '',
          campaign: '',
          role: null,
          active: null
        }

      }
    },

    mounted() {
      this.load()
    },

    methods: {
      redirect(url) {
        // Check role
        if (![
          'Super Admin',
          'Distributor Manager',
          'Sales Executive'].includes(
          this.$store.state.account.role.name))
          return;
        // Redirect
        this.$router.push(url)
      },

      load() {
        this.loadRoles();
        this.loadAccounts();
      },

      async loadAccounts() {
        let filters = [];

        this.filters.username && filters.push({
          field: 'username', op: 'ilike', value: `%${this.filters.username}%`
        });
        this.filters.email && filters.push({
          field: 'email', op: 'ilike', value: `%${this.filters.email}%`
        });
        this.filters.distributor && filters.push({
          field: 'name', op: 'ilike', value: `%${this.filters.distributor}%`, model: 'Distributor'
        });
        this.filters.campaign && filters.push({
          field: 'campaign_name', op: 'ilike', value: `%${this.filters.campaign}%`
        });
        this.filters.role && filters.push({
          field: 'name', op: '==', value: this.filters.role, model: 'Role'
        });
        if ([true, false].indexOf(this.filters.active) !== -1) {
          filters.push({
            field: 'active', op: '==', value: this.filters.active
          })
        }

        this.itemsPending = true;

        await this.$store.dispatch(
          'jv/get',
          ['accounts', {params: {
            filter: JSON.stringify(filters),
            include: 'campaigns,distributor,role'
          }}]
        ).then((accounts) => {
          this.items = Object.values(accounts).filter(acc => !this.isUsernameSystem(acc.username));
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      },

      async loadRoles() {
        this.possibleRolesPending = true;

        this.$store.dispatch('jv/get', 'roles').then((roles) => {
          this.possibleRolesObject = roles;
          this.possibleRoles = Object.values(roles);
        }).catch(err => {
          console.error(err);
        });

        this.possibleRolesPending = false;
      },

      isUsernameSystem(username) {
        return username.match(/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i)
      },

      applyFilter: _.debounce(function () {
        this.load()
      }, 300),

      async updateAccount(account) {
        this.$store.dispatch(
          'jv/patch',
          [account, {params: {include: 'campaigns,distributor,role'}}],
        ).catch(err => {
          console.error(err);
        });
      }
    }
  }
</script>
