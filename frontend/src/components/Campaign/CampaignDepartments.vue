<template>
  <v-container grid-list-xs>
    <v-form class="ml-5 mr-5" ref="form" v-model="valid">

      <v-card class="mt-2 mb-2 pt-3 pl-3 pb-1 elevation-3"
        v-for="(department, index) in departments" 
        :key=index>
        <p class="ml-2 subheading"><b>Department Name:</b> {{ department }}</p>
        <v-card-actions>
          <v-btn color="error" @click="removeDepartment(index)">delete</v-btn>
        </v-card-actions>
      </v-card>

      <v-text-field class="mt-5"
        label="Department name"
        v-model="newDepartment"
      ></v-text-field>
      <v-btn @click="addDepartment">add department</v-btn>

    </v-form>
  </v-container>
</template>

<script>
  export default {
    props: {
      campaign: Object,
      editMode: Boolean,
    },
    
    data() {
      return {
        valid: null,

        departments: [],
        newDepartment: '',
      }
    },

    mounted() {
      if (this.editMode) {
        this.fillPreliminaryData()
      }
    },

    methods: {
      fillPreliminaryData() {
        this.$data.departments = JSON.parse(this.$props.campaign.departments);
      },

      addDepartment() {
        if (!this.newDepartment) {
          this.$store.dispatch('raiseError', 'Department name cannot be blank');
        } else {
          this.departments.push(this.newDepartment);
        }
      },

      removeDepartment(index) {
        this.departments.splice(index, 1);
      },

      updateCampaign(campaign) {
        campaign.departments = JSON.stringify(this.departments);

        return campaign;
      },
    }
  }
</script>
