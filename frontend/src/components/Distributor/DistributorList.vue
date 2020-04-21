<template>
  <v-container fluid grid-list-xl>
    <v-layout row wrap>
      <v-flex xs9>
        <template>
          <v-data-table
            :loading="itemsPending"
            :no-data-text="itemsPending ? 'Loading... Please wait':'No data available'"
            :headers="headers"
            :items="items"
            class="elevation-1"
            :rows-per-page-items="[25]"
            :hide-actions="items.length < 50"
            :pagination.sync="pagination"
          >
            <template slot="items" slot-scope="props">
              <tr @click="isSuperAdmin && $router.push('/admin/distributors/' + props.item._jv.id)">
                <td>
                  <div class="clip">{{ props.item._jv.id }}</div>
                </td>
                <td>
                  <div class="clip">{{ props.item.name }}</div>
                </td>
                <td>
                  <div class="clip">{{ props.item.email }}</div>
                </td>
                <td>
                  <div class="clip">{{ Object.values(props.item.product_types).map(p => p.name).join(', ') }}
                  </div>
                </td>
              </tr>
            </template>
          </v-data-table>
        </template>
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
    <v-btn
      v-if="isSuperAdmin"
      color="primary"
      fab
      fixed
      bottom
      right
      @click="$router.push('/admin/distributors/add')"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
  import _ from 'lodash';
  import {mapGetters} from "vuex";

  export default {
    computed: {
      ...mapGetters(['isSuperAdmin']),
    },

    data() {
      return {
        headers: [
          { text: 'Id', value: '_jv.id' },
          { text: 'Name', value: 'name' },
          { text: 'Email', value: 'email' },
          { text: 'Product types', sortable: false, value: 'product_types' },
        ],
        pagination: {
          page: 1,
          sortBy: 'name',
        },
        items: [],
        itemsPending: true,
        filters: {
          name: '',
          email: '',
        }
      }
    },

    mounted() {
      this.loadDistributors();
    },

    methods: {
      async loadDistributors() {
        let filters = [];

        this.filters.name && filters.push({
          field: 'name', op: 'ilike', value: `%${this.filters.name}%`
        });

        this.itemsPending = true;

        await this.$store.dispatch(
          'jv/get',
          ['distributors', {params: {filter: JSON.stringify(filters), include: 'product_types'}}]
        ).then((distributors) => {
          this.items = Object.values(distributors);
          this.pagination.page = 1;
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      },

      applyFilter: _.debounce(function () {
        this.loadDistributors();
      }, 300),
    }
  }
</script>
