export const SET_CAMPAIGN_SAVING = "@campaign/SET_CAMPAIGN_SAVING";
export const SET_CAMPAIGN_SAVING_DIALOG = "@campaign/SET_CAMPAIGN_SAVING_DIALOG";

export default {
  state: {
    distributor: null,
    companyName: '',

    // Checkout fields
    firstNameEnabled: false,
    lastNameEnabled: false,
    companyEmailEnabled: false,
    departmentsEnabled: false,
    locationsEnabled: false,
    managersEnabled: false,
    customFields: [],

    products: [],

    BFLCost: 0,

    forms: {
      campaignSetup: {
        distributor_id: null,
        name: '',
        company_name: '',
        message: '',
        start_date: null,
        end_date: null
      },
      showOptions: false,
    },

    isSaving: false,
    isDisableDialogActive: false,
  },

  mutations: {
    [SET_CAMPAIGN_SAVING](state, payload) {
      state.isSaving = !!payload;
    },
    [SET_CAMPAIGN_SAVING_DIALOG](state, payload) {
      state.isDisableDialogActive = !!payload;
    }
  },
}
