<template>
  <v-container fluid fill-height>
    <v-layout align-center>
      <v-flex md1></v-flex>
      <v-flex xs12 md4>
        <div>
          <div class="display-1 mb-4 text-xs-center">Welcome to OrderWrite</div>
          <v-form
            class="login-form"
            @submit.prevent="submitHandler"
            v-model="valid"
            ref="form"
          >
            <v-card-text>

              <v-text-field
                prepend-icon="person"
                name="login"
                type="text"
                v-model="username"
                :rules="loginRules"
                placeholder="Username..."
                data-cy="login"
              >
              </v-text-field>
              <v-text-field
                id="password"
                prepend-icon="lock"
                name="password"
                type="password"
                v-model="password"
                :rules="passwordRules"
                placeholder="Password"
                data-cy="password"
              >
              </v-text-field>

            </v-card-text>
            <div class="text-xs-center">
              <v-spacer></v-spacer>
              <v-btn
                large
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="!valid || loading"
                data-cy="submit"
              >Login
              </v-btn>
            </div>
          </v-form>
        </div>
      </v-flex>
      <v-flex md7 hidden-sm-and-down class="background">
        <img src="@/assets/woman_jumping.png" alt="Woman Jumping">
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  class User {
    constructor(data) {
      this.account_id = data.account_id
      this.token = data.token
      this.token_type = data.token_type
    }
  }

  export default {
    data() {
      return {
        username: '',
        password: '',
        valid: false,
        loginRules: [
          v => !!v || 'Login is required'
        ],
        passwordRules: [
          v => !!v || 'Password is required'
        ]
      }
    },

    computed: {
      loading() {
        return this.$store.getters.loading
      }
    },

    methods: {
      submitHandler() {
        if (this.$refs.form.validate()) {
          this.$axios.post('/auth/login', {
            'username': this.username,
            'password': this.password,
          }).then((response) => {
            // clear old account information in localStorage
            this.$store.dispatch('logout');

            // save the token so we can make the next request to get the account's data
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('userId', response.data.account_id);

            this.$store.dispatch(
              'jv/get',
              [`accounts/${response.data.account_id}`, {params: {include: 'role'}}],
            ).then(account => {
              // save the new account information in localStorage
              this.$store.dispatch('login', account);

              // different roles are redirected to different home pages
              if (account.role.name == 'Distributor Manager') {
                this.$router.push('/admin/campaigns');
              } else if (account.role.name == 'Sales Executive') {
                this.$router.push('/admin/campaigns');
              } else if (account.role.name == 'Shopper') {
                this.$router.push('/');
              } else {
                this.$router.push('/admin');
              }
            });
          });
        }
      }
    }
  }
</script>

<style scoped>
  .background {
    text-align: right;
    padding-right: 5vw;
  }

  .background img {
    height: 80vh;
  }

  .container {
    background-color: white;
  }
</style>
