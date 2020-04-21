export default class OrderNote {
  static generateEmpty() {
    return {
      id: null,
      note: '',
      order_id: null,
      account_id: null,
      _jv: {
        type: 'OrderNote',
      }
    }
  };
}