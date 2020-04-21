export default class Location {
  static generateEmpty() {
    return {
      id: null,
      nickname: null,
      company_name: null,
      street_and_number: null,
      city: null,
      zip_code: null,
      delivery_contact: null,
      suite_unit_etc: null,
      region: null,
      country: 'United States',
      campaign_id: null,
      _jv: {
        type: 'Location',
      }
    }
  };
}