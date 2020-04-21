export default class ProductAttribute {
  static generateEmpty() {
    return {
      id: null,
      name: '',
      distributors_enabled: false,
      sales_execs_enabled: false,
      assoc_product_image: false,
      assoc_added_costs: false,
      assoc_bin_id: false,
      product_type_id: null,
      product_type: null,
      values: [],
      _jv: {
        type: 'ProductAttribute',
      }
    };
  };
}

