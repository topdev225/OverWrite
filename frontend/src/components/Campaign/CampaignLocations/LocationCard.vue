<template>
  <v-card class="elevation-3">
    <v-card-title class="headline">
      {{ location.nickname }}
    </v-card-title>

    <v-card-text>
      <v-layout row wrap>
        <v-flex xs6>
          <p class="ml-2 subheading"><b>Company:</b> {{ location.company_name }}</p>
          <p class="ml-2 subheading"><b>Street and number:</b> {{ location.street_and_number }}</p>
          <p class="ml-2 subheading"><b>City:</b> {{ location.city }}</p>
          <p class="ml-2 subheading"><b>Postal Code:</b> {{ location.zip_code }}</p>
        </v-flex>
        <v-flex xs6>
          <p class="ml-2 subheading"><b>Attention/Delivery Contact:</b> {{ location.delivery_contact }}</p>
          <p class="ml-2 subheading"><b>Suite, Unit, Building, Floor, etc.:</b> {{ location.suite_unit_etc }}</p>
          <p class="ml-2 subheading"><b>Country:</b> {{ location.country }}</p>
          <p class="ml-2 subheading"><b>State/Province:</b> {{ location.region }}</p>
        </v-flex>
      </v-layout>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="error" @click="$emit('remove')">Remove</v-btn>
      <v-btn color="info" @click="$emit('edit')">Edit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'LocationCard',
  props: {
    location: Object
  }
}
</script>
