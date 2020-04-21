<template>
  <v-container class="mb-5">
    <v-layout row>
      <v-flex xs12>
        <template>
          <v-data-table
            :loading="attributesPending"
            :no-data-text="attributesPending ? 'Loading... Please wait' : 'No data available'"
            :headers="headers"
            :items="attributes"
            class="elevation-1"
            :rows-per-page-items="[25]"
            :hide-actions="attributes.length < 50"
          >
            <template slot="items" slot-scope="props">
              <router-link tag="tr" :to="'/admin/product_attributes/' + props.item._jv.id">
                <td>{{ props.item.name }}</td>
                <td>
                  <div class="clip">
                    {{ Object.values(props.item.product_types).map(p => p.name).join(', ') }}
                </div>
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
      @click="$router.push('/admin/product_attributes/add')"
      data-cy="AddProductAttributeItemButton"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
  export default {
    data() {
      return {
        attributes: [],
        attributesPending: true,
        headers: [
          { text: 'Name', value: 'name' },
          { text: 'Product Types', sortable: false, value: '' },
        ]
      }
    },

    mounted() {
      this.loadAttributes();
    },

    methods: {
      async loadAttributes() {
        this.attributesPending = true;

        await this.$store.dispatch(
          'jv/get',
          ['product_attributes', {params: {include: 'product_types'}}]
        ).then((attributes) => {
          this.attributes = Object.values(attributes);
        }).catch(err => {
          console.error(err);
        });

        this.attributesPending = false;
      }
    },
  }
</script>
