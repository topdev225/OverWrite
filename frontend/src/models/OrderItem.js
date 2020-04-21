export default class OrderItem {
  static generateEmpty() {
    return {
      id: null,
      quantity: 0,
      order_id: null,
      order: null,
      campaign_product_variant_id: null,
      campaign_product_variant: null,
      _jv: {
        type: 'OrderItem',
      }
    }
  };
}
