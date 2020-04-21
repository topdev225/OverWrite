export default class Vendor {
  static generateEmpty() {
    return {
      id: null,
      name: '',
      email: '',
      address: '',
      is_decorator: false,
      is_supplier: false,
      is_pick_pack: false,
      product_types: [],
      _jv: {
        type: 'Vendor',
      }
    };
  }
}
