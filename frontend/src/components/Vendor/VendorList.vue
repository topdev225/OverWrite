<template>
  <v-container fluid grid-list-xl>
    <v-btn
      color="primary"
      fab
      fixed
      bottom
      right
      @click="$router.push('/admin/vendors/add')"
    >
      <v-icon>add</v-icon>
    </v-btn>
    <v-layout row wrap>
      <v-flex xs9>
        <v-data-table
          :loading="itemsPending"
          :no-data-text="itemsPending ? 'Loading... Please wait' : 'No data available'"
          v-model="selected"
          :headers="headers"
          :items="items"
          :pagination.sync="pagination"
          :rows-per-page-items="[25]"
          :hide-actions="items.length < 50"
          item-key="name"
          class="elevation-1"
        >
          <template slot="items" slot-scope="props">
            <router-link tag="tr" :active="props.selected" :to="'/admin/vendors/' + props.item._jv.id" class="product_link">
              <td class="text-xs-left">{{ props.item._jv.id }}</td>
              <td class="text-xs-left">
                <span class="clip"> {{ props.item.name }}</span>
              </td>
              <td class="text-xs-left">
                <span class="clip"> {{ props.item.email }}</span>
              </td>
              <td>
                <div class="clip">{{ Object.values(props.item.product_types).map(p => p.name).join(', ') }}</div>
              </td>
            </router-link>
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
                v-model="filters.name"
                label="Name"
                v-on:keyup="applyFilter">
              </v-text-field>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import _ from 'lodash'

  export default {

    data() {
      return {
        items: [],
        itemsPending: true,
        pagination: {
          page: 1,
          sortBy: 'name'
        },
        selected: [],
        headers: [
          { text: 'ID', value: '_jv.id' },
          { text: 'Name', value: 'name' },
          { text: 'Email', value: 'email' },
          { text: 'Product types', sortable: false, value: 'product_types' },
        ],

        filters: {
          name: ''
        }
      }
    },

    mounted() {
      this.loadVendors();
    },

    methods: {
      async loadVendors() {
        let filters = [];

        this.filters.name && filters.push({
          field: 'name', op: 'ilike', value: `%${this.filters.name}%`
        });

        this.itemsPending = true;

        await this.$store.dispatch(
          'jv/get',
          ['vendors', {params: {filter: JSON.stringify(filters), include: 'product_types'}}]
        ).then((vendors) => {
          this.items = Object.values(vendors);
          this.pagination.page = 1;
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      },

      applyFilter: _.debounce(function () {
        this.loadVendors();
      }, 300)
    }
  }
</script>
