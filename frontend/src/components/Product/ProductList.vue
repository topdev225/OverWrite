<template>
  <v-container fluid grid-list-xl>
    <v-btn
      color="primary"
      fab
      fixed
      bottom
      right
      @click="$router.push('/admin/products/add')"
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
          :items="products"
          :pagination.sync="pagination"
          :rows-per-page-items="[25]"
          item-key="name"
          class="elevation-1"
        >
          <template slot="items" slot-scope="props">
            <router-link tag="tr" :active="props.selected" :to="'/admin/products/' + props.item._jv.id" class="product_link">
              <td>
                <v-layout>
                  <v-img
                    height="45"
                    contain
                    v-bind:ref="'preview' + parseInt(props.item._jv.id)"
                    :src="getImg(props.item)"
                  />
                </v-layout>
              </td>
              <td>{{ props.item._jv.id }}</td>
              <td>
                <p class="clip"> {{ props.item.name }}</p>
              </td>
              <td>
                <p class="clip"> {{ props.item.product_type.name }}</p>
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
              <v-text-field
                v-model="filters.type"
                label="Type"
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
  import _ from 'lodash';

  export default {
    data() {
      return {
        pagination: {
          page: 1,
          sortBy: 'name'
        },
        products: [],
        selected: [],
        headers: [
          { text: '', sortable: false, value: '' },
          { text: 'ID', value: '_jv.id' },
          { text: 'Name', value: 'name' },
          { text: 'Type', value: 'product_type.name' }
        ],

        itemsPending: true,
        filters: { name: '', type: '' }
      }
    },

    mounted() {
      this.loadProducts()
    },

    methods: {
      async loadProducts() {
        this.itemsPending = true;

        let filters = []

        this.$data.filters.name && filters.push({
          field: 'name', op: 'ilike', value: `%${this.$data.filters.name}%`
        })
        this.$data.filters.type && filters.push({
          field: 'name', op: 'ilike', value: `%${this.$data.filters.type}%`,
          model: 'ProductType'
        })

        await this.$store.dispatch(
          'jv/get',
          ['products', {params: {
            filter: JSON.stringify(filters),
            include: 'product_type',
          }}]
        ).then((products) => {
          this.products = Object.values(products);
          this.pagination.page = 1;
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      },

      getImg(item) {
        // FIXME: handle image uploading, storage, and delivery
        let defaultImg = `${process.env.API_BASE_URL}/static/default-product.svg`;

        return defaultImg;
      },

      applyFilter: _.debounce(function () {
        this.loadProducts()
      }, 300)
    },
  }
</script>
<style>
  .product_link {
    cursor: pointer;
  }
  .checkbox{
    padding-left: 11px;
  }
</style>
