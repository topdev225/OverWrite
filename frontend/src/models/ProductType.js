export default class ProductType {
  static generateEmpty() {
    return {
      id: null,
      name: '',
      product_attributes: [],
      distributors: [],
      vendors: [],
      _jv: {
        type: 'ProductType',
      }
    }
  };
}
