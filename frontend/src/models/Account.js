export default class Account {
  static generateEmpty() {
    return {
      id: null,
      username: '',
      password: '',
      email: '',
      first_name: '',
      last_name: '',
      role_id: null,
      reports_enabled: false,
      _jv: {
        type: 'Account',
      }
    }
  };
}