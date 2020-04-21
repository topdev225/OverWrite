<template>
  <v-layout justify-center row wrap mb-5>
    <v-flex xs6 mt-5 v-if="productPending">
      <center>
        <v-progress-circular
          :indeterminate="true"
          color="green"
          size="32"
          width="4"
        />
      </center>
    </v-flex>

    <v-flex xs6 mt-5 v-if="!productPending">
      <v-card>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2 word-break-all">{{product.name}}</h3>
            <div class="word-break-all">{{product.product_type.name}}</div>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn flat color="primary" @click="$router.push('/admin/products/edit/'+ product._jv.id)">Edit Product</v-btn>
          <v-btn flat color="primary" @click="deleteDialogOpened = true">Remove Product</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <v-flex xs3 offset-xs1 mt-5 v-if="!productPending">
      <v-card>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2">Image</h3>
          </div>
        </v-card-title>
        <v-layout align-center justify-space-around row fill-height>
          <v-img class="image-sample" :src="getImg()" />
        </v-layout>
      </v-card>
    </v-flex>

    <v-flex xs10 mt-5 v-if="!productPending">
      <v-card>
        <v-card-title primary-title>
          <div>
            <h3 class="headline mb-2">Variants</h3>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-data-table
          :headers="productVariantHeaders"
          :items="productVariants"
          class="elevation-1"
          hide-actions
        >
          <template slot="items" slot-scope="props">
            <td>{{ props.item.sku }}</td>
            <td>{{ props.item.description }}</td>
            <td>{{ props.item.supplier && props.item.supplier.name }}</td>
            <td class="justify-center text-md-center">
              <!-- FIXME: implement the actions for these buttons -->
              <v-icon small>edit</v-icon>
              <v-icon small>delete</v-icon>
            </td>
          </template>
        </v-data-table>
      </v-card>
    </v-flex>

    <template>
      <v-dialog
        v-model="deleteDialogOpened"
        max-width="800"
      >
        <v-card>
          <v-card-title
            class="headline error white--text"
            primary-title>
            Delete Product
          </v-card-title>

          <v-card-text>
            <div class="title" style="line-height:1.4 !important">
              <p class="mt-2 mb-3">
                Do you really want to delete <strong>"{{product.name || ''}}"?</strong>
              </p>
            </div>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="py-3 px-3">
            <v-spacer></v-spacer>
            <v-btn
              outline
              color="error"
              @click="deleteDialogOpened = false"
            >
              Cancel
            </v-btn>
            <v-btn
              :loading="deleteDialogPending"
              :disabled="deleteDialogPending"
              color="error"
              @click="deleteProduct()"
            >
              Delete
              <template slot="loader">
                <span>Saving...</span>
              </template>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </v-layout>
</template>

<script>
  export default {
    data () {
      return {
        product: {},
        productPending: true,
        productVariants: [],

        productVariantHeaders: [
          { text: 'SKU', sortable: false, value: 'sku' },
          { text: 'Description', sortable: false, value: 'description' },
          { text: 'Supplier', sortable: false, value: 'supplier.name' },
          { text: 'Actions', sortable: false, value: '', align: 'center' },
        ],

        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    mounted () {
      this.loadProduct();
      this.loadProductVariants();
    },

    methods: {
      endAction() {
        this.$router.push('/admin/products');
      },

      getImg() {
        // FIXME: handle image uploading, storage, and delivery
        let defaultImg = `${process.env.API_BASE_URL}/static/default-product.svg`;

        return defaultImg;
      },

      async loadProduct() {
        this.productPending = true;

        await this.$store.dispatch(
          'jv/get',
          [`products/${this.$route.params.id}`, {params: {
            include: 'product_type',
          }}]
        ).then(product => {
          this.$data.product = product;
        }).catch(err => {
          console.error(err);
        });

        this.productPending = false;
      },

      async loadProductVariants() {
        await this.$store.dispatch(
          'jv/get',
          [`products/${this.$route.params.id}/product_variants`, {params: {
            include: 'supplier',
          }}]
        ).then(productVariants => {
          this.$data.productVariants = Object.values(productVariants);
        }).catch(err => {
          console.error(err);
        });
      },

      async deleteProduct() {
        await this.$store.dispatch('jv/delete', this.product).then(resp => {
          this.$store.dispatch('raiseSuccess', `Product ${this.product._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });
      }
    }
  }
</script>
<style scoped>
  .image-sample{
    width: 50px;
  }
</style>
