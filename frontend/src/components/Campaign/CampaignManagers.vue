<template>
  <v-container grid-list-xs>
    <v-form class="ml-5 mr-5"
      ref="form"
      v-model="valid">

      <v-card
        class="mt-2 mb-2 pt-3 pl-3 pb-1 elevation-3"
        v-for="(manager, index) in managers"
        :key=index
      >
        <p class="ml-2 subheading"><b>First Name:</b> {{ manager.first_name }}</p>
        <p class="ml-2 subheading"><b>Last Name:</b> {{ manager.last_name }}</p>
        <p class="ml-2 subheading"><b>Email:</b> {{ manager.email }}</p>
        <v-card-actions>
          <v-btn color="error" @click="removeManager(index)">delete</v-btn>
        </v-card-actions>
      </v-card>

      <v-text-field class="mt-5"
        label="First Name"
        v-model="managerFirstName"
        :rules="[validateNoSpecials]"
      />
      <v-text-field
        label="Last Name"
        v-model="managerLastName"
        :rules="[validateNoSpecials]"
      />
      <v-text-field
        label="Email"
        v-model="managerEmail"
        :rules="[validateEmail]"
      />
      <v-btn :disabled="!valid" @click="addManager">add manager</v-btn>
    </v-form>
  </v-container>
</template>

<script>
  import rules from '@/mixins/rules'

  export default {
    props: {
      campaign: Object,
      editMode: Boolean,
    },

    mixins: [
      rules
    ],
    
    data() {
      return {
        valid: null,

        managers: [],

        managerFirstName: '',
        managerLastName: '',
        managerEmail: '',
      }
    },

    validate() {
      if(this.$data.managers.length > 0) {
       return true
      } else {
      return false
      }
    },

    mounted() {
      if (this.editMode) {
        this.fillPreliminaryData();
      }
    },

    methods: {
      fillPreliminaryData() {
        this.$data.managers = JSON.parse(this.$props.campaign.managers);
      },

      addManager() {
        this.$data.managers.push({
          'first_name': this.$data.managerFirstName.slice(),
          'last_name': this.$data.managerLastName.slice(),
          'email': this.$data.managerEmail.slice(),
        })

        this.$data.managerFirstName = '';
        this.$data.managerLastName = '';
        this.$data.managerEmail = '';
      },

      removeManager(index) {
        this.$data.managers.splice(index, 1);
      },

      updateCampaign(campaign) {
        campaign.managers = JSON.stringify(this.managers);

        return campaign;
      }
    }
  }
</script>

