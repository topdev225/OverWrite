<template>
  <v-container fluid grid-list-xl>
    <v-layout mt-2 align-center justify-center column fill-height>
      <v-layout align-center justify-center row fill-height>
        <div class="headline">Let's Create A New Campaign!</div>
        <v-btn
          fab
          dark
          @click="$router.push('/admin/campaigns/add')"
          color="primary"
          class="ml-4">
          <v-icon dark>add</v-icon>
        </v-btn>
      </v-layout>
      <v-divider width="90%" class="mt-3 mb-3"></v-divider>
      <v-layout mt-3 align-start justify-center column fill-height style="max-width: 100%;">
        <v-flex>
          <v-data-table
            :loading="campaignsPending"
            :no-data-text="campaignsPending ? 'Loading... Please wait':'No data available'"
            :headers="headers"
            :items="campaigns"
            disable-initial-sort
            hide-actions
            pagination.sync="{'sortBy': 'name'}"
            class=""
          >
            <template slot="items" slot-scope="props">
              <td class="text-xs-left">
                <router-link class="clip" :to="`/admin/campaigns/${props.item.id}`" style="text-decoration: none">
                  <p class="ma-auto black--text" v-if="props.item.complete"> <b>Distributor PO:</b> {{ props.item.distributor_po }}</p>
                  <p class="ma-auto black--text">
                    {{ props.item.name }}
                  </p>
                </router-link>
              </td>
              <td class="text-xs-left">
                <p class="ma-auto clip">
                  {{ props.item.company_name }}
                </p>

              </td>
              <td class="text-xs-left">
                <div class="mt-3" v-if="!props.item.complete">
                  <span>{{ props.item.status }}</span>
                  <v-switch v-if="props.item.ready_for_using || campaignSwitchDisabled "
                            @click="changeStatus(props.item.id, props.item.status)"
                            :input-value="props.item.status === 'Active' ? 'true': ''"
                            :disabled="campaignSwitchDisabled || !props.item.ready_for_using"
                  ></v-switch>
                  <p v-else><b>setup not completed</b></p>
                </div>
                <div class="mt-3" v-else>
                  <b><p><span>{{ props.item.status }}</span></p></b>
                </div>
              </td>
              <td class="text-xs-left">{{ props.item.created_at | moment("MM/DD/YY") }}
              </td>
              <td class="text-xs-left actions">
                <v-tooltip top>
                  <v-btn
                    icon
                    color="primary"
                    @click="$router.push('/admin/campaigns/'+ props.item.id)"
                    slot="activator"
                  >
                    <v-icon>edit</v-icon>
                  </v-btn>
                  <span>Edit</span>
                </v-tooltip>
                <v-tooltip top>
                  <v-btn
                    icon
                    color="primary"
                    @click="duplicateCampaign(props.item.id)"
                    slot="activator"
                  >
                    <v-icon>file_copy</v-icon>
                  </v-btn>
                  <span>Duplicate</span>
                </v-tooltip>
                <v-tooltip top>
                  <v-btn
                    icon
                    color="error"
                    :disabled="props.item.status === 'Active' || props.item.complete"
                    @click="openDeleteDialog(props.item)"
                    slot="activator"
                  >
                    <v-icon>delete</v-icon>
                  </v-btn>
                  <span>{{props.item.status === 'Active' ? "Can't be deleted while active" : 'Delete'}}</span>
                </v-tooltip>
                <v-tooltip top>
                  <v-btn
                    icon
                    color="error"
                    @click.stop="changeCompletenessHandler(props.item)"
                    slot="activator"
                    :disabled="props.item.complete && !$store.getters.isSuperAdmin"
                  >
                    <v-icon v-if="!props.item.complete">lock</v-icon>
                    <v-icon v-if="props.item.complete">lock_open</v-icon>
                  </v-btn>
                  <span>{{!props.item.complete ? 'Complete' : $store.getters.isSuperAdmin ? 'Unlock' : 'Can be unlocked only by a Superadmin'}}</span>
                </v-tooltip>
              </td>
            </template>
          </v-data-table>
          <complete-campaign-dialog
            :campaign="completeDialogCampaign"
            @update="load()"
            @close="closeCompleteDialog()"
          />
          <template>
            <v-layout row justify-center>
              <v-dialog
                v-model="uncompleteCampaignDialogOpened"
                max-width="800"
              >
                <v-card>
                  <v-card-title
                    class="headline error white--text"
                    primary-title>
                    Unlock completed campaign?
                  </v-card-title>

                  <v-card-text>
                    <div class="title" style="line-height:1.4 !important">
                      <p class="mt-2 mb-3">
                        Do you want to unlock completed campaign <strong>"{{uncompleteCampaignData ?
                        uncompleteCampaignData.name : ''}}"?</strong>
                      </p>
                    </div>
                  </v-card-text>

                  <v-divider></v-divider>

                  <v-card-actions class="py-3 px-3">
                    <v-spacer></v-spacer>
                    <v-btn
                      outline
                      color="error"
                      @click="closeUncompleteDialog()"
                    >
                      cancel
                    </v-btn>
                    <v-btn
                      :loading="uncompleteCampaignPending"
                      :disabled="uncompleteCampaignPending"
                      color="error"
                      @click="uncompleteCampaign(uncompleteCampaignData)"
                    >
                      unlock
                      <template slot="loader">
                        <span>Saving...</span>
                      </template>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-layout>
          </template>
          <template>
            <v-layout row justify-center>
              <v-dialog
                v-model="deleteCampaignDialogOpened"
                max-width="800"
              >
                <v-card>
                  <v-card-title
                    class="headline error white--text"
                    primary-title>
                    Delete campaign
                  </v-card-title>

                  <v-card-text>
                    <div class="title" style="line-height:1.4 !important">
                      <p class="mt-2 mb-3">
                        Do you really want to delete campaign <strong>"{{deleteCampaignData ?
                        deleteCampaignData.name : ''}}"?</strong> This operation can't be undone.
                      </p>
                    </div>
                  </v-card-text>

                  <v-divider></v-divider>

                  <v-card-actions class="py-3 px-3">
                    <v-spacer></v-spacer>
                    <v-btn
                      outline
                      color="error"
                      @click="closeDeleteDialog()"
                    >
                      cancel
                    </v-btn>
                    <v-btn
                      :loading="deleteCampaignPending"
                      :disabled="deleteCampaignPending"
                      color="error"
                      @click="deleteCampaign(deleteCampaignData)"
                    >
                      Delete
                      <template slot="loader">
                        <span>Saving...</span>
                      </template>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-layout>
          </template>
        </v-flex>
      </v-layout>
    </v-layout>
  </v-container>
</template>

<script>
  import CampaignCompleteDialog from "./CampaignCompleteDialog";
  import {SET_CAMPAIGN_SAVING_DIALOG} from "@/store/campaign";

  export default {
    components: {
      CampaignCompleteDialog,
    },
    data() {
      return {
        headers: [
          {
            text: 'Campaign',
            value: 'name'
          },
          {
            text: 'Company',
            value: 'company_name'
          },
          {
            text: 'Status',
            value: 'status'
          },
          {
            text: 'Create Date',
            value: 'created_at'

          },
          {
            text: 'Actions',
            sortable: false
          }
        ],
        campaigns: [],
        campaignsPending: true,
        completeDialogCampaign: null,

        uncompleteCampaignDialogOpened: false,
        uncompleteCampaignPending: false,
        uncompleteCampaignData: null,

        deleteCampaignDialogOpened: false,
        deleteCampaignPending: false,
        deleteCampaignData: null,
      }
    },

    beforeRouteLeave(to, from, next) {
      if (to.path != '/admin/campaigns/add' && this.isSaving) {
        this.$store.commit(SET_CAMPAIGN_SAVING_DIALOG, true);
        next(false);
      } else {
        next();
      }
    },

    computed: {
      campaignSwitchDisabled() {
        let disabled = false
        if (this.$store.state.account && this.$store.state.account.role.name == 'Admin Buyer')
          disabled = true
        return disabled
      },
      isSaving() {
        return this.$store.state.campaign.isSaving;
      }
    },

    mounted() {
      this.load()
    },
    methods: {
      async load() {
        this.campaignsPending = true;
        try {
          const resp = await this.$axios.get(`/campaigns`, {headers: {'Authorization': this.$data.token}});
          this.campaigns = resp.data;
        } catch (e) {
          console.error(e);
        }
        this.campaignsPending = false;
      },

      duplicateCampaign(id) {
        this.campaignsPending = true;
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        this.$axios.post(`/campaigns/${id}/duplicate`, {}, params)
          .then(this.load)
          .catch((e) => this.$store.dispatch('raiseError', e.response.data.message))
          .finally(() => this.campaignsPending = false);
      },

      openDeleteDialog(campaign) {
        this.deleteCampaignData = campaign;
        this.deleteCampaignDialogOpened = true;
      },
      closeDeleteDialog() {
        this.deleteCampaignData = null;
        this.deleteCampaignDialogOpened = false;
      },
      async deleteCampaign(campaign) {
        this.deleteCampaignPending = true;
        try {
          await this.$axios.delete(`/campaigns/${campaign.id}`, {headers: {Authorization: this.$data.token}});
          this.closeDeleteDialog();
          this.load();
        } catch (e) {
          this.$store.dispatch('raiseError', e.response.data.message);
        }
        this.deleteCampaignPending = false;
      },

      changeStatus(id, status) {
        let params = {
          headers: {
            Authorization: this.$data.token
          }
        }
        let data = {}
        if (status === 'Active') {
          data.status = 'Not Active'
        } else {
          data.status = 'Active'
        }
        axios
          .put(`/campaigns/${id}`, data, params)
          .then(resp => {
            this.campaigns = []
            this.load()
          })
          .catch(err => {
            console.log(err);
          });
      },

      openCompleteDialog(campaign) {
        this.completeDialogCampaign = campaign;
      },
      closeCompleteDialog() {
        this.completeDialogCampaign = null;
      },

      changeCompletenessHandler(campaign) {
        campaign.complete ? this.openUncompleteDialog(campaign) : this.openCompleteDialog(campaign);
      },

      openUncompleteDialog(campaign) {
        this.uncompleteCampaignData = campaign;
        this.uncompleteCampaignDialogOpened = true;
      },
      closeUncompleteDialog() {
        this.uncompleteCampaignData = null;
        this.uncompleteCampaignDialogOpened = false;
      },
      async uncompleteCampaign({accounts, distributor, product_variants, ...campaign}) {
        this.uncompleteCampaignPending = true;
        try {
          await this.$axios.patch(`/campaigns/${campaign.id}`, {
            complete: false
          });
          this.closeUncompleteDialog();
          this.load();
        } catch (e) {
          this.$store.dispatch('raiseError', e.response.data.message);
        }
        this.uncompleteCampaignPending = false;
      },
    }
  }
</script>


<style>
  .actions {
    white-space: nowrap;
  }

  .actions .v-btn {
    margin: 3px;
  }

  .v-table {

  }

</style>
