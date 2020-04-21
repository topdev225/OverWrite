<template>
  <campaign v-if="campaign" :campaign="campaign"></campaign>
</template>


<script>

    import axios from '@/axios'

    import Campaign from '../base/Campaign'
    import {SET_CAMPAIGN_SAVING_DIALOG} from "../../../../store/campaign";

    export default {

        components: {
            'campaign': Campaign
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
            isSaving() {
                return this.$store.state.campaign.isSaving;
            }
        },

        data() {
            return {
                campaign: null     // Dash 'cause of component name
            }
        },

        mounted() {
            let fields = '*,distributor,accounts{*,role}'
            let params = {
                headers: {
                    'Authorization': this.$store.state.token,
                    'X-Fields': fields
                }
            }
            axios.get(`/campaigns/${this.$route.params.id}`, params).then(resp => {
                this.$data.campaign = resp.data
            })
        }

    }
</script>
