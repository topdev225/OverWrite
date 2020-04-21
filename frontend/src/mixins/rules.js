export default {
  methods: {
    validateNotEmpty: v => !!v || 'Required',
    validateNotEmptyCheckbox: v => !!(v===true || v===false) || 'Item is required',
    validateUsername: v => /^\w*$/.test(v) || 'Username is not valid',
    validateEmail: v => /^$|^.+@.*\..*$/.test(v) || 'Email is not valid',
    validateNoSpecials: v => /^[a-zA-Z0-9 ]*$/.test(v) || 'Special symbols are not allowed',
    validateNumber: v => v && /^[0-9]*\.{0,1}[0-9]*$/.test(v.toString().trim()) || 'Number is incorrect',
    validateInteger: v => /^[0-9]*$/.test(v) || 'Number is incorrect',
    validateZipCode: v => !v || /^[0-9-]*$/.test(v) || 'Zip code is incorrect',
    validateLimit: limit => v => (parseInt(v) || 0) <= limit || 'Out of limit',
    validateCharLimit: limit => v => (v || '').length <= limit || 'Out of limit',
    validateCount: limit => v => (v || '').length >= limit || `Please select at least ${limit}`,
    validateMin: limit => v => typeof v !== "undefined" && Number(v) >= limit || `Has to be at least ${limit}`,
    validateMax: limit => v => typeof v !== "undefined" && Number(v) <= limit || `Can be max ${limit}`,
    validateOneOf: valuesArr => v => valuesArr && Array.isArray(valuesArr) && valuesArr.find(va => va) || 'One of these have to be selected',
  }
}
