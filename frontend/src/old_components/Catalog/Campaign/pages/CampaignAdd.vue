<template>
  <campaign></campaign>
</template>


<script>

    import Campaign from '../base/Campaign'
    import {SET_CAMPAIGN_SAVING_DIALOG} from "../../../../store/campaign";

    export default {
        components: {
            'campaign': Campaign
        },
        beforeRouteLeave(to, from, next) {
            if (from.path === '/admin/campaigns/add' && to.name !== 'campaignEdit'  && this.isSaving) {
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

    }
</script>
