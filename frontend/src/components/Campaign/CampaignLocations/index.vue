<template>
  <div>
    <v-container grid-list-lg>
      <v-layout row wrap align-center>
        <v-flex
          xs12
          v-for="(location, index) in locations"
          :key="index"
        >
          <location-card
            :location="location"
            @edit="$refs.locationModal.show(location, index)"
            @remove="() => $data.locations.splice(index, 1)"
          ></location-card>
        </v-flex>

        <v-flex xs12 class="add-container">
          <v-btn fab @click="$refs.locationModal.show()">
              <v-icon>add</v-icon>
          </v-btn>
        </v-flex>

      </v-layout>
    </v-container>

    <location-modal
      ref="locationModal"
      @save="l => $data.locations.push(l)"
      @update="(l, i) => $data.locations.splice(i, 1, l)"
    ></location-modal>
  </div>
</template>

<script>
  import LocationModal from './LocationModal';
  import LocationCard from './LocationCard';

  export default {
    name: 'CampaignLocations',

    props: {
      campaign: Object,
      editMode: Boolean,
    },

    components: {
      LocationModal,
      LocationCard
    },

    computed: {
      valid() {
        return this.locations.length > 0;
      },
    },

    data() {
      return {
        locations: [],
      }
    },

    mounted() {
      if (this.editMode && this.$props.campaign.locations) {
          this.$data.locations = this.$props.campaign.locations;
      } else {
        this.$data.locations = [];
      }
    },

    methods: {
      updateCampaign(campaign) {
        campaign.locations = this.locations;

        return campaign;
      },
    },
  }
</script>


<style scoped>
.add-container {
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>
