export default class Product {
  static generateEmpty() {
    return {
      id: null,
      name: '',
      item_number: '',
      product_type_id: null,
      product_type: null,
      distributor_id: null,
      distributor: null,
      product_variants: [],
      _jv: {
        type: 'Product',
      }
    }
  };
}