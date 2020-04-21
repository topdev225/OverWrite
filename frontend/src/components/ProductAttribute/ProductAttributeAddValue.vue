<template>
  <v-dialog v-model="addValueModalOpened" max-width="800">
    <v-card>
      <v-form ref="addValueForm" @submit.prevent="addValueFormSubmit">
        <v-card-title
          class="headline primary white--text"
          primary-title
        >
          Add Value
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="tmpValue.name"
            label="Value *"
            :rules="[validateNotEmpty]"
          />
        </v-card-text>
        <v-divider />
        <v-card-actions class="py-3 px-3">
          <v-spacer />
          <v-btn
            @click="addValueModalOpened = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            type="submit"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
  import rules from '@/mixins/rules';
  import ProductAttributeValue from "@/models/ProductAttributeValue";

  export default {
    mixins: [
      rules,
    ],

    data() {
      return {
        tmpValue: ProductAttributeValue.generateEmpty(),
        addValueModalOpened: false,
      }
    },
    methods: {

      openAddValueModal() {
        this.addValueModalOpened = true;
      },

      async addValueFormSubmit() {
        if (this.$refs.addValueForm.validate()) {
          this.$emit('onAddValue', this.tmpValue);
          this.addValueModalOpened = false;
          this.tmpValue = ProductAttributeValue.generateEmpty();
        }
      },
    }
  }
</script>
