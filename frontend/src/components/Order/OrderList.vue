<template>
  <v-container fluid grid-list-xl>
    <v-layout row wrap mb-5>
      <v-flex xs9>
        <template>
          <v-data-table
            :loading="itemsPending"
            :no-data-text="itemsPending ? 'Loading... Please wait' : 'No data available'"
            :headers="headers"
            :items="orders"
            class="elevation-1"
            :rows-per-page-items="[25]"
            hide-actions
          >
            <template slot="items" slot-scope="props">
              <router-link tag="tr" :to="'/admin/orders/' + props.item._jv.id">
                <td>{{ props.item._jv.id }}</td>
                <td>{{ props.item.account.username }} ({{ get_fl_name(props.item.checkout_fields) }})</td>
                <td>{{ props.item.campaign.name }}</td>
                <td>{{ props.item.created_at }}</td>
                <td>{{ props.item.status }}</td>
              </router-link>
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
                  v-model="filters.customer"
                  label="Customer"
                  v-on:keyup="applyFilter">
              </v-text-field>
              <v-text-field
                  v-model="filters.campaign"
                  label="Campaign"
                  v-on:keyup="applyFilter">
              </v-text-field>
              <div @click="filter_range_picker_modal = true">
                <v-text-field
                  disabled
                  v-model="filters.date_from"
                  label="From">
                </v-text-field>
                <v-text-field
                    disabled
                    v-model="filters.date_to"
                    label="To">
                </v-text-field>
              </div>

              <v-select
                  :items="['processing', 'canceled', 'shipped']"
                  :clearable="true"
                  v-model="filters.status"
                  v-on:change="applyFilter"
                  label="Order status">
              </v-select>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-dialog
      v-model="filter_range_picker_modal"
      width="800">
      <v-card>
        <v-card-title
          class="headline"
          primary-title>
          Select range
        </v-card-title>
        <v-card-text>
          <v-daterange
              :options="filter_range_picker_options"
              @input="filterDateRangeChange"></v-daterange>
        </v-card-text>
        <v-card-actions class="mt-3">
          <v-spacer></v-spacer>
          <v-btn
            @click="filterDateRangeClear">
          clear
          </v-btn>
          <v-btn
            color="primary"
            @click="filter_range_picker_modal = false">
          ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  import moment from 'moment';
  import _ from 'lodash';

  export default {
    data() {
      return {
        itemsPending: true,

        orders: [],
        headers: [
          { text: 'ID', value: '_jv.id' },
          { text: 'Username (Full Name)', value: 'account.username' },
          { text: 'Campaign', value: 'campaign.name' },
          { text: 'Placed on', value: 'created_at' },
          { text: 'Status', value: 'status' }
        ],

        filters: {
          customer: '',
          campaign: '',
          date_from: null,
          date_to: null,
          status: null
        },

        filter_range_picker_modal: false,
        filter_range_picker_options: {
          format: 'YYYY-MM-DD',
          startDate: moment().subtract(7,'d').format('YYYY-MM-DD'),
          endDate: moment().format('YYYY-MM-DD'),
          presets: [
            {
              label: '2 days',
              range: [
                moment().subtract(2,'d').format('YYYY-MM-DD'),
                moment().format('YYYY-MM-DD'),
              ]
            },
            {
              label: '7 days',
              range: [
                moment().subtract(7,'d').format('YYYY-MM-DD'),
                moment().format('YYYY-MM-DD'),
              ],
            },
            {
              label: '30 days',
              range: [
                moment().subtract(30,'d').format('YYYY-MM-DD'),
                moment().format('YYYY-MM-DD'),
              ]
            }
          ]
        }
      }
    },

    mounted() {
      this.load()
    },

    methods: {
      get_fl_name(val) {
        let f_name = ''
        try {
          f_name = Object.values(val)[0];
        }catch (e) {
          f_name = 'No first name'
        }

        let l_name = ''
        try {
          l_name = Object.values(val)[1];
        }catch (e) {
          l_name = 'No last name'
        }

        return f_name + " " + l_name
      },

      async load() {
        this.itemsPending = true;

        let filters = []

        this.$data.filters.customer && filters.push({
          field: 'username', op: 'ilike', value: `%${this.$data.filters.customer}%`, model: 'Account'
        })
        this.$data.filters.campaign && filters.push({
          field: 'name', op: 'ilike', value: `%${this.$data.filters.campaign}%`, model: 'Campaign'
        })
        this.$data.filters.date_from && filters.push({
          field: 'created_at', op: '>=', value: this.$data.filters.date_from
        })
        this.$data.filters.date_to && filters.push({
          field: 'created_at', op: '<=', value: this.$data.filters.date_to
        })
        this.$data.filters.status && filters.push({
          field: 'status', op: '==', value: this.$data.filters.status
        })

        await this.$store.dispatch(
          'jv/get',
          ['orders', {params: {filter: JSON.stringify(filters), include: 'account,campaign'}}]
        ).then(orders => {
          let dateFormattedOrders = Object.values(orders).map(obj => {
            obj.created_at = moment(obj.created_at).format('YYYY-MM-DD hh:mm A');
            return obj;
          });

          this.orders = dateFormattedOrders;
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      },

      filterDateRangeClear() {
        this.$data.filters.date_from = ''
        this.$data.filters.date_to = ''
        this.$data.filter_range_picker_modal = false
        this.applyFilter()
      },

      filterDateRangeChange(range) {
        this.$data.filters.date_from = range[0]
        this.$data.filters.date_to = range[1]
        this.applyFilter()
      },

      applyFilter: _.debounce(function() {
        this.load()
      }, 300)
    }
  }
</script>
