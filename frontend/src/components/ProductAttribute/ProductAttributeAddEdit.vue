<template>
  <v-layout justify-center>
    <v-flex xs10 mt-4>
      <v-card class="mb-4">
        <v-card-title class="primary white--text">
          <div>
            <h3 class="headline">
              <span>{{ this.$route.params.id ? 'Edit' : 'Create' }} Attribute</span>
            </h3>
          </div>
        </v-card-title>

        <v-progress-linear
          :active="attributePending"
          :indeterminate="true"
          class="ma-0"
          height="4"
          style="top: -2px;"
        >
          Loading...
        </v-progress-linear>

        <v-form ref="form" @submit.prevent="submitHandler">
          <v-card-text v-if="!attributePending">
            <v-text-field
              v-model="attribute.name"
              label="Attribute name *"
              :rules="[validateNotEmpty]"
            />

            <div class="mb-3">Who can add values:</div>
            <div class="d-flex flex-wrap">
              <v-switch
                v-model="attribute.distributors_enabled"
                label="Distributors"
                class="flex-grow-0 mr-4"
              />
              <v-switch
                v-model="attribute.sales_execs_enabled"
                label="Sales Executives"
                class="flex-grow-0 mr-4"
              />
            </div>

            <v-divider class="mb-4" />

            <div class="mb-3">Associate attribute with:</div>
            <div class="d-flex flex-wrap">
              <v-switch
                v-model="attribute.assoc_product_image"
                label="Product Image"
                class="flex-grow-0 mr-4"
              />
              <v-switch
                v-model="attribute.assoc_added_costs"
                label="Added Costs"
                class="flex-grow-0 mr-4"
              />
              <v-switch
                v-model="attribute.assoc_bin_id"
                label="Bin Identifier"
                class="flex-grow-0 mr-4"
              />
            </div>

            <v-divider class="mb-3"></v-divider>

            <div class="mb-3">Possible values:</div>
            <div>
              <v-data-table
                :headers="valueHeaders"
                :items="selectedAttributeValues"
                :loading="savePending"
                class="elevation-1"
                :hide-actions="selectedAttributeValues && selectedAttributeValues.length < 20"
                disable-initial-sort
                v-data-table-sortable="move"
                item-key="name"
              >
                <template slot="items" slot-scope="props">
                  <td data-table-sortable-handle style="max-width: 28px">
                    <v-icon style="cursor: pointer">menu</v-icon>
                  </td>
                  <td>
                    {{props.item.name}}
                  </td>
                  <td style="width: 150px;">
                    <v-btn
                      flat
                      color="error"
                      @click="removeValue(props.item, props.index)"
                    >
                      Remove
                    </v-btn>
                  </td>
                </template>
              </v-data-table>
              <div class="d-flex justify-end">
                <v-btn
                  class="flex-grow-0"
                  fab
                  color="primary"
                  @click="$refs.addValueModal.openAddValueModal()"
                >
                  <v-icon>add</v-icon>
                </v-btn>
              </div>
            </div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
              @click="endAction()"
            >
              Cancel
            </v-btn>
            <v-btn
              v-if="$data.attribute && $data.attribute._jv.id"
              @click="removeAttribute()"
              color="error"
            >
              Delete
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
            >
              {{ this.$route.params.id ? 'Update' : 'Create' }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <ProductAttributeAddValue ref="addValueModal" @onAddValue="addValue" />
    </v-flex>
  </v-layout>
</template>

<script>
  import rules from '@/mixins/rules';
  import DataTableSortable from "@/directives/DataTableSortable";
  import ProductAttributeAddValue from "./ProductAttributeAddValue";
  import ProductAttribute from "@/models/ProductAttribute";

  export default {
    components: {
      ProductAttributeAddValue,
    },

    mixins: [
      rules,
    ],

    props: {
      emitOnClose: { required: false, type: Boolean },
      initialAttribute: { required: false, type: Object, },
    },

    directives: {
      DataTableSortable,
    },

    async mounted() {
      if (this.$route.params.id) {
        await this.loadAttribute();
      } else if (this.$props.initialAttribute) {
        this.$data.attribute = this.$props.initialAttribute;
      } else {
        this.attributePending = false;
      }

      this.$data.selectedAttributeValues = Object.values(this.$data.attribute.values).sort(this.sortByPosition);
    },

    computed: {
      endAction() {
        if (this.$props.emitOnClose) {
          return () => this.$emit('onClose', true);
        } else {
          return () => this.$router.push('/admin/product_attributes');
        }
      },
    },

    data() {
      return {
        valueHeaders: [
          { text: '', value: '', sortable: false, },
          { text: 'Name', value: 'name' },
          { text: '', value: '', sortable: false, },
        ],

        attribute: ProductAttribute.generateEmpty(),
        attributePending: !this.$route.params.id,
        savePending: false,
        selectedAttributeValues: [],
      };
    },

    methods: {
      async loadAttribute() {
        this.attributePending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `product_attributes/${this.$route.params.id}`,
            {params: {include: 'product_type,values'}}
          ]
        ).then((attribute) => {
          this.attribute = attribute;
        }).catch(err => {
          console.error(err);
        });

        this.attributePending = false;
      },

      sortByPosition(a, b) {
        let comparison = 0;

        if (a.position > b.position) {
          comparison = 1;
        } else if (a.position < b.position) {
          comparison = -1;
        }

        return comparison;
      },

      async submitHandler() {
        if (this.$refs.form.validate()) {
          this.savePending = true;

          // first, either create or update the model
          if (this.$route.params.id) {
            await this.$store.dispatch(
              'jv/patch', this.attribute
            ).then(attribute => {
              this.$data.attribute = attribute;
              this.updateAttributeValues('updated');
            }).catch(err => {
              console.error(err);
            });
          } else {
            await this.$store.dispatch(
              'jv/post', [this.attribute, {url: '/product_attributes'}]
            ).then(attribute => {
              this.$data.attribute = attribute;
              this.updateAttributeValues('created');
            }).catch(err => {
              console.error(err);
            });
          }

          this.savePending = false;
        }
      },

      async updateAttributeValues(actionVerb) {
        // then, update the product type relationship in a separate call. convert list of selected
        // product types into a list of resource identifiers
        let listOfIdentifers = this.selectedAttributeValues.map(obj => {
          return {id: obj._jv.id, type: obj._jv.type};
        });

        await this.$axios.post(
          `/product_attributes/${this.$data.attribute._jv.id}/set_values_keep_order`,
          { data: listOfIdentifers },
        ).then(resp => {
          this.$store.dispatch('raiseSuccess', `Attribute ${this.$data.attribute._jv.id} ${actionVerb}`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });
      },

      async removeAttribute() {
        await this.$store.dispatch('jv/delete', this.$data.attribute).then(resp => {
          this.$store.dispatch('raiseSuccess', `Attribute ${this.$data.attribute._jv.id} removed`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });
      },

      async removeValue(item, index) {
        this.selectedAttributeValues.splice(index, 1);
      },

      async move(oldIndex, newIndex) {
        const item = this.selectedAttributeValues[oldIndex];
        const rowSelected = this.selectedAttributeValues.splice(oldIndex, 1)[0];
        this.selectedAttributeValues.splice(newIndex, 0, rowSelected);
      },

      async addValue(value) {
        // if it already exists, use the existing model. otherwise, create a new one
        let filters = [{ field: 'name', op: '==', value: value.name }];

        this.savePending = true;

        // try to find an existing model
        await this.$store.dispatch(
          'jv/get',
          [
            'product_attribute_values',
            { params: { filter: JSON.stringify(filters) }}
          ]
        ).then(attribute_value => {
          this.selectedAttributeValues.push(attribute_value);
        }).catch(err => {
          // response was 404, so we have to create a new model and use that
          if (err.response && err.response.status === 404) {
            this.$store.dispatch(
              'jv/post', [value, {url: '/product_attributes_values'}]
            ).then(attribute_value => {
              this.selectedAttributeValues.push(attribute_value);
            }).catch(err => {
              this.$store.dispatch('raiseError', `Failed to create new value '${value.name}'`);
              console.error(err);
            });
          } else {
            this.$store.dispatch('raiseError', err);
            console.error(err);
          }
        });

        this.savePending = false;
      },
    }
  }
</script>
