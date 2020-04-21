export default class Order {
  static generateEmpty() {
    return {
      id: null,
      created_at: '',
      status: null,
      checkout_fields: {},
      total: 0.0,
      account_id: null,
      account: null,
      campaign_id: null,
      campaign: null,
      order_notes: [],
      order_items: [],
      order_events: [],
      _jv: {
        type: 'Order',
      }
    }
  };
}
