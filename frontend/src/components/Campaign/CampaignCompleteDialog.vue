<template>
  <v-dialog
    v-model="opened"
    max-width="800"
  >
    <v-card>

      <v-card-title
        class="headline error white--text"
        primary-title>
        Complete campaign
      </v-card-title>

      <v-card-text>
        <div class="title" style="line-height:1.4 !important">
          <p class="mt-2 mb-3">
            Do you want to complete campaign <strong>"{{campaignName}}"?</strong>
          </p>
        </div>
        <v-form
          v-model="formValid"
          ref="completeDialogForm"
        >
          <v-layout row wrap>
            <v-flex xs12>
              <v-text-field
                color="error"
                v-model="formData.distributor_po"
                :rules="[validateNotEmpty]"
                label="Distributor PO *"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-form>
        <v-alert
          :value="true"
          color="error"
          icon="priority_high"
          outline
        >
          Once a campaign is marked <strong>"completed"</strong> you will not be able to make changes to shopper
          orders.
        </v-alert>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="py-3 px-3">
        <v-spacer></v-spacer>
        <v-btn
          outline
          color="error"
          @click="close()"
        >
          cancel
        </v-btn>
        <v-btn
          :loading="pending"
          :disabled="pending || !formValid"
          color="error"
          @click="completeCampaign(campaign, formData.distributor_po)"
        >
          Complete
          <template slot="loader">
            <span>Saving...</span>
          </template>
        </v-btn>
      </v-card-actions>

    </v-card>

  </v-dialog>
</template>

<script>
  import rules from '@/mixins/rules';
  import axios from '@/axios';

  export default {
    props: {
      campaign: {
        type: Object,
        default: null,
      }
    },
    mixins: [
      rules,
    ],
    data() {
      return {
        pending: false,
        formValid: false,
        formData: {
          distributor_po: '',
        },
        opened: false,
      }
    },
    computed: {
      campaignName() {
        return this.campaign ? this.campaign.name : '';
      },
    },
    watch: {
      campaign(next) {
        this.opened = !!next;
      },
      opened(val) {
        if (!val) {
          this.$emit('close');
        }
      }
    },
    methods: {
      /**
       * Sends completeness request
       * @param campaign Campaign's instance
       * @param distributor_po ???
       * @returns {Promise<void>}
       */
      async completeCampaign({accounts, distributor, ...campaign}, distributor_po) {
        this.pending = true;
        try {
          await this.$axios.patch(`/campaigns/${campaign.id}`, {
            complete: true,
            distributor_po,
          });
          this.$emit('update');
          this.$emit('close');
        } catch (e) {
          console.error(e);
        }
        this.pending = false;
      },
      close() {
        this.$emit('close');
      }
    }
  }
</script>

<style scoped>

</style>
