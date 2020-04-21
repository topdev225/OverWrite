<template>
  <v-container fluid grid-list-xl>
    <v-layout row wrap mb-5>
      <v-flex xs12 mt-5 v-if="orderPending">
        <center>
          <v-progress-circular
            :indeterminate="true"
            color="green"
            size="32"
            width="4"
          />
        </center>
      </v-flex>

      <v-flex xs8 v-if="!orderPending">
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline">Shopping Cart</h3>
            </div>
          </v-card-title>

          <v-card-text>
            <v-data-table
              :headers="shoppingCartHeaders"
              :loading="orderItemsPending"
              :items="orderItems"
              class="elevation-1"
              :rows-per-page-items="[25]"
              hide-actions
            >
              <template slot="items" slot-scope="props">
                <tr>
                  <td>{{ props.item._jv.id }}</td>
                  <td>{{ props.item.campaign_product_variant.product_name }}</td>
                  <td>{{ props.item.campaign_product_variant.sku }}</td>
                  <td>{{ props.item.quantity }}</td>
                  <td class="justify-center text-md-center">
                    <v-icon
                      small
                      @click="openItemUpdateModal(props.item)"
                      :disabled="orderItemEditDisabled"
                    >
                      edit
                    </v-icon>
                    <v-icon
                      small
                      @click="deleteItem(props.item)"
                      :disabled="orderItemEditDisabled"
                    >
                      delete
                    </v-icon>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs4 v-if="!orderPending">
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline">Order Summary</h3>
            </div>
          </v-card-title>

          <v-card-text>
            <!-- Checkout fields -->
            <div v-for="(value, name) in order.checkout_fields" :key="name">
              <div class="subheading mt-2"> {{ name }}</div>
              <div> {{ value }}</div>
            </div>

            <!-- Other info -->
            <div class="subheading mt-2">Campaign</div>
            <div> {{ order.campaign ? order.campaign.name : '(No data)' }}</div>

            <div class="subheading mt-2">Status</div>
            <div> {{ order.status }}</div>

            <div class="subheading mt-2">Total</div>
            <div> ${{ order.total.toFixed(2) }}</div>
          </v-card-text>

          <v-card-actions>
            <v-flex text-xs-center>
              <v-btn v-if="shippedButtonEnabled" @click="updateStatus('shipped')" color="primary">
                Shipped
              </v-btn>
              <v-btn v-if="processingButtonEnabled" @click="updateStatus('processing')" color="primary" outline>
                Processing
              </v-btn>
              <v-btn v-if="cancelButtonEnabled" @click="updateStatus('canceled')" color="error">
                Cancel
              </v-btn>
              <v-btn v-if="uncancelButtonEnabled" @click="updateStatus('processing')" color="error" outline>
                Uncancel
              </v-btn>
              <v-btn v-if="deleteButtonEnabled" @click="deleteDialogOpened = true" color="error">
                Delete
              </v-btn>
            </v-flex>
          </v-card-actions>
        </v-card>
      </v-flex>

      <v-flex xs8 v-if="!orderPending">
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline">Order Notes</h3>
            </div>
          </v-card-title>

          <v-card-text>
            <v-divider class="mb-2" />
            <div v-for="note in orderNotes" :key="note._jv.id">
              <div class="caption">
                <span><b>
                  {{ note.account.username }} on {{ datetimeFormatter(note.created_at) }}
                </b></span>
              </div>
              <div class="body-1">
                {{ note.note }}
              </div>
              <v-divider class="mb-2 mt-2" />
            </div>
          </v-card-text>

          <v-card-actions>
            <v-dialog v-model="addNoteModalIsOpen" width="500">
              <v-btn color="primary" slot="activator">
                Add
              </v-btn>
              <v-card>
                <v-card-title class="headline" primary-title>
                  Add Note
                </v-card-title>

                <v-card-text>
                  <v-textarea solo name="input-7-4" label="Note" v-model="newNote.note" />
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn outline color="error" @click="addNoteModalIsOpen = false">
                    Cancel
                  </v-btn>
                  <v-btn color="primary" @click="addNote">
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card-actions>
        </v-card>
      </v-flex>

      <v-flex xs4 v-if="!orderPending">
        <v-card>
          <v-card-title primary-title>
            <div>
              <h3 class="headline">History</h3>
            </div>
          </v-card-title>

          <v-card-text>
            <v-divider class="mb-2" />
            <div v-for="event in orderEvents" :key="event._jv.id">
              <div class="caption">
                <span><b>{{ datetimeFormatter(event.created_at) }}</b></span>
              </div>
              <div class="body-1">
                {{ event.note }}
              </div>
              <v-divider class="mb-2 mt-2" />
            </div>
          </v-card-text>

        </v-card>
      </v-flex>

    </v-layout>

    <v-dialog v-model="updateItemModalIsOpen" width="500">
      <v-card>
        <v-card-title class="headline" primary-title>
          Update item in order
        </v-card-title>

        <v-card-text>
          <v-form>
            <v-select
              v-model="updateItemSelectedVariant"
              :items="updateItemPossibleVariants"
              item-text="sku"
              item-value="_jv.id"
              label="Select a different SKU"
              return-object
            />
            <v-text-field
              v-model.number="updateItemQuantity"
              type="number"
              label="Quantity"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="error" outline @click="updateItemModalIsOpen = false">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="saveItem"
            :disabled="validateQuantity(updateItemQuantity)"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialogOpened" max-width="800">
      <v-card>
        <v-card-title
          class="headline error white--text"
          primary-title>
          Delete Order
        </v-card-title>

        <v-card-text>
          <div class="title" style="line-height:1.4 !important">
            <p class="mt-2 mb-3">
              Do you really want to delete order <strong>{{ order._jv.id }}?</strong>
            </p>
            <div class="caption">{{ extraDeleteModalText }}</div>
          </div>
        </v-card-text>

        <v-divider />

        <v-card-actions class="py-3 px-3">
          <v-spacer />
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
            @click="deleteOrder()"
          >
            Delete
            <template slot="loader">
              <span>Saving...</span>
            </template>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>


<script>
  import Order from '@/models/Order';
  import OrderNote from '@/models/OrderNote';
  import moment from 'moment';

  export default {
    data() {
      return {
        shoppingCartHeaders: [
          {text: 'ID', value: '_jv.id'},
          {text: 'Name', value: 'campaign_product_variant.product.name'},
          {text: 'SKU', value: 'campaign_product_variant.sku'},
          {text: 'Quantity', value: 'quantity'},
          {text: 'Actions', sortable: false, value: 'actions', align: 'center'},
        ],

        order: Order.generateEmpty(),
        orderEvents: [],
        orderItems: [],
        orderNotes: [],

        orderPending: true,
        orderItemsPending: true,

        updateItemId: null,
        updateItemModalIsOpen: false,
        updateItemPossibleVariants: [],
        updateItemQuantity: null,
        updateItemSelectedVariant: null,

        addNoteModalIsOpen: false,
        newNote: OrderNote.generateEmpty(),

        deleteDialogOpened: false,
        deleteDialogPending: false,
      }
    },

    computed: {
      shippedButtonEnabled() {
        return (
          !this.$store.getters.isShopper &&
          this.order.status != 'shipped' &&
          this.order.status != 'canceled'
        );
      },

      processingButtonEnabled() {
        return (
          !this.$store.getters.isShopper &&
          this.order.status != 'canceled' &&
          this.order.status != 'processing'
        );
      },

      cancelButtonEnabled() {
        return (this.order.status != 'shipped' && this.order.status != 'canceled')
      },

      uncancelButtonEnabled() {
        return (
          !this.$store.getters.isShopper &&
          this.order.status === 'canceled'
        );
      },

      deleteButtonEnabled() {
        return (
          this.$store.state.account.role.name === 'Super Admin' ||
          this.$store.state.account.role.name === 'Sales Executive' ||
          this.$store.state.account.role.name === 'Distributor Manager'
        );
      },

      extraDeleteModalText() {
        if (this.orderItems.length === 1) {
          return 'NOTE: Removing the last item in an order will delete the entire order.';
        }
      },

      orderItemEditDisabled() {
        return this.order.status !== 'processing';
      }
    },

    mounted() {
      this.loadOrder();
      this.loadOrderItems();
      this.loadOrderNotes();
      this.loadOrderEvents();
    },

    methods: {
      validateQuantity(quantity) {
        return !quantity || parseInt(quantity) < 1;
      },

      endAction() {
        this.$router.push(`/admin/orders`);
      },

      datetimeFormatter(datetime) {
        return moment(datetime).format('MMMM Do, YYYY [at] h:mm a');
      },

      sortByMostRecent(a, b) {
        if (a.created_at > b.created_at) {
          return -1;
        } else if (a.created_at < b.created_at) {
          return 1;
        } else {
          return 0;
        }
      },

      async loadOrder() {
        this.orderPending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `/orders/${this.$route.params.id}`,
            {params: {include: 'order_items'}}
          ]
        ).then(order => {
          this.order = order;
        }).catch(err => {
          console.error(err);
        });

        this.orderPending = false;
      },

      async loadOrderItems() {
        this.orderItemsPending = true;

        await this.$store.dispatch(
          'jv/get',
          [
            `/orders/${this.$route.params.id}/order_items`,
            {params: {include: 'campaign_product_variant'}}
          ]
        ).then(orderItems => {
          this.orderItems = Object.values(orderItems);
        }).catch(err => {
          console.error(err);
        });

        this.orderItemsPending = false;
      },

      async loadOrderNotes() {
        await this.$store.dispatch(
          'jv/get',
          [
            `/orders/${this.$route.params.id}/order_notes`,
            {params: {include: 'account'}}
          ]
        ).then(orderNotes => {
          this.orderNotes = Object.values(orderNotes).sort(this.sortByMostRecent);
        }).catch(err => {
          console.error(err);
        });
      },

      async loadOrderEvents() {
        await this.$store.dispatch(
          'jv/get',
          `/orders/${this.$route.params.id}/order_events`,
        ).then(orderEvents => {
          this.orderEvents = Object.values(orderEvents).sort(this.sortByMostRecent);
        }).catch(err => {
          console.error(err);
        });
      },

      async openItemUpdateModal(orderItem) {
        // when the user wants to edit a line in the shopping cart, we need to fetch other available
        // variants that they can change to. for example, the item in the cart might be blue/small
        // and there is red/small and blue/medium available.
        let filter = [
          { field: 'product_id', op: '==', value: `${orderItem.campaign_product_variant.product_id}` },
          { field: 'campaign_id', op: '==', value: `${this.order.campaign_id}` },
        ];

        await this.$store.dispatch(
          'jv/get',
          [`/campaign_product_variants`, { params: { filter: JSON.stringify(filter) } }]
        ).then(productVariants => {
          this.updateItemId = orderItem._jv.id;
          this.updateItemQuantity = orderItem.quantity;
          this.updateItemSelectedVariant = orderItem.campaign_product_variant;
          this.updateItemPossibleVariants = Object.values(productVariants);
        }).catch(err => {
          console.error(err);
        });

        this.updateItemModalIsOpen = true;
      },

      async deleteItem(orderItem) {
        if (this.orderItems.length !== 1) {
          await this.$store.dispatch(
            'jv/delete', orderItem
          ).then(resp => {
            this.$store.dispatch('raiseSuccess', 'Item deleted');
            this.loadOrderItems();
          }).catch(err => {
            console.error(err);
          });
        } else {
          this.deleteDialogOpened = true;
        }
      },

      async saveItem() {
        const orderItem = {
          quantity: this.updateItemQuantity,
          campaign_product_variant_id: this.updateItemSelectedVariant._jv.id,
          _jv: {
            id: this.updateItemId,
            type: 'OrderItem',
          }
        };

        await this.$store.dispatch(
          'jv/patch', [orderItem, {url: `/order_items/${this.updateItemId}`}]
        ).then(resp => {
          this.$store.dispatch('raiseSuccess', 'Item updated');
          this.loadOrderItems();
          this.updateItemModalIsOpen = false;
        }).catch(err => {
          console.error(err);
        });
      },

      async addNote() {
        // create the note first
        this.newNote.account_id = this.$state.account._jv.id;

        await this.$store.dispatch(
          'jv/post', [this.newNote, {url: '/order_notes'}]
        ).then(note => {
          // then attach it to this order
          this.$axios.post(
            `/orders/${this.$route.params.id}/order_notes`,
            { data: [{ id: note._jv.id, type: note._jv.type }] }
          ).then(resp => {
            this.$store.dispatch('raiseSuccess', 'Note added');
            this.addNoteModalIsOpen = false;
            this.newNote = OrderNote.generateEmpty();
            this.loadOrderNotes()
          }).catch(err => {
            console.error(err);
          });
        }).catch(err => {
          console.error(err);
        });
      },

      async updateStatus(newStatus) {
        let originalStatus = this.order.status;

        this.order.status = newStatus;

        await this.$store.dispatch(
          'jv/patch', this.order
        ).then(order => {
          this.order = order;
          this.$store.dispatch('raiseSuccess', 'Status changed');
          this.loadOrderEvents();
        }).catch(err => {
          this.order.status = originalStatus;
          console.error(err);
        });
      },

      async deleteOrder() {
        this.deleteDialogPending = true;

        await this.$store.dispatch('jv/delete', this.order).then(resp => {
          this.$store.dispatch('raiseSuccess', `Order ${this.order._jv.id} deleted`);
          this.endAction();
        }).catch(err => {
          console.error(err);
        });

        this.deleteDialogPending = false;
      }
    }
  }
</script>
