<template>
  <v-container mb-5>
    <v-layout row>
      <v-flex xs12>
        <template>
          <v-data-table
            :loading="itemsPending"
            :no-data-text="itemsPending ? 'Loading... Please wait' : 'No data available'"
            :headers="headers"
            :items="items"
            class="elevation-1"
            :rows-per-page-items="[25]"
            :hide-actions="items.length < 50"
          >
            <template slot="items" slot-scope="props">
              <router-link
                data-cy="ProductTypeItem"
                tag="tr"
                style="cursor:pointer"
                :to="'/admin/product_types/' + props.item._jv.id"
              >
                <td>
                  <div class="clip">{{ props.item.name }}</div>
                </td>
                <td>
                  {{ Object.values(props.item.product_attributes).map(x => x.name).join(', ') }}
                </td>
              </router-link>
            </template>
          </v-data-table>
        </template>
      </v-flex>
    </v-layout>
    <v-btn
      color="primary"
      fab
      fixed
      bottom
      right
      @click="$router.push('/admin/product_types/add')"
      data-cy="AddProductTypeItemButton"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
  export default {
    data() {
      return {
        items: [],
        itemsPending: true,
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Variant Attributes', sortable: false, value: 'variant' },
        ]
      }
    },

    mounted() {
      this.loadProductTypes();
    },

    methods: {
      async loadProductTypes() {
        this.itemsPending = true;

        await this.$store.dispatch(
          'jv/get',
          ['product_types', {params: {include: 'product_attributes'}}]
        ).then((product_types) => {
          this.items = Object.values(product_types);
        }).catch(err => {
          console.error(err);
        });

        this.itemsPending = false;
      }
    }
  }
</script>
