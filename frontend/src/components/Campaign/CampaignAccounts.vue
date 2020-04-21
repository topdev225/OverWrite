<template>
  <v-container grid-list-xs>
    <v-form ref="form" v-model="valid">
      <blockquote class="blockquote text-xs-center"><slot></slot></blockquote>

      <v-text-field
        v-model="account.first_name"
        v-if="!nameDisabled"
        label="First Name"
        :rules="[validateNoSpecials]"
      />

      <v-text-field
        v-model="account.last_name"
        v-if="!nameDisabled"
        label="Last Name"
        :rules="[validateNoSpecials]"
      />

      <v-text-field
        v-model="account.email"
        v-if="!emailDisabled"
        label="Email"
        :rules="[validateEmail]"
      />

      <v-tooltip top v-if="!reportsDisabled">
        <v-switch
          v-model="account.reports_enabled"
          style="width: 250px"
          slot="activator"
          label="Allow account to see reports"
        />
        <span>Click if you want this account to have real-time access to reporting</span>
      </v-tooltip>

      <v-text-field
        v-model="account.username"
        label="Login *"
        :rules="[validateUsername, validateNotEmpty]"
      />

      <v-text-field
        autocomplete="new-password"
        v-model="account.password"
        type="password"
        label="Password *"
        :rules="[validateNotEmpty]"
      />
    </v-form>
  </v-container>
</template>

<script>
  import rules from '@/mixins/rules';
  import Account from '@/models/Account';

  export default {
    props: {
      campaign: Object,
      editMode: Boolean,
      targetRole: Object,
      otherRole: Object,
      nameDisabled: Boolean,
      emailDisabled: Boolean,
      reportsDisabled: Boolean,
    },

    mixins: [
      rules
    ],

    data() {
      return {
        valid: null,
        account: Account.generateEmpty(),
      }
    },

    mounted() {
      if (this.editMode) {
        this.fillPreliminaryData()
      }
    },

    methods: {
      fillPreliminaryData() {
        let account = this.$props.campaign.accounts.filter(
          obj => obj.role.name === this.targetRole.name
        )[0];

        if (account) {
          this.$data.account = account;
        }
      },

      updateCampaign(campaign) {
        // validate model
        if (this.account.username === '') {
            throw 'Account username cannot be blank';
        }

        if (this.account.password === '') {
            throw 'Account password cannot be blank';
        }

        // validate lack of conflict between the usernames of the two accounts in the campaign
        if (campaign.accounts) {
          let otherAccount = campaign.accounts.filter(obj => obj.role.name == this.otherRole.name)[0];

          if (otherAccount && otherAccount.username === this.account.username) {
            throw 'Shopper and Admin Buyer cannot have the same username';
          }

          // if there is an existing model in there, update it rather than create a new one
          let account = campaign.accounts.filter(obj => obj.role.name == this.targetRole.name)[0];

          if (account) {
            account.username = this.account.username;
            account.password = this.account.password;
            account.role = this.targetRole;
            account.role_id = this.targetRole._jv.id;

            return campaign;
          }
        }

        // if we get to this point, there are either no accounts associated with this campaign or
        // there was no shopper in the list of associated accounts. either way, we are going to
        // have to create a shopper model.
        this.account.role = this.targetRole;
        this.account.role_id = this.targetRole._jv.id;

        // ultimately, the method that saves this campaign to the database will have to sort out
        // whether to update an existing account model or create a new one.
        if (campaign.accounts) {
          campaign.accounts.push(this.account);
        } else {
          campaign.accounts = [this.account];
        }

        return campaign;
      },
    }
  }
</script>
