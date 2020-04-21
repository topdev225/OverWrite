<template>
  <div>

    <v-divider class="mt-1 mb-5"></v-divider>

    <!-- Variants -->
    <div
      v-if="productVariantSets.length > 0"
      v-for="(set, pvsIndex) in productVariantSets" :key="pvsIndex"
      class="pa-3 mb-3 elevation-3">

      <v-layout row wrap>
        <v-flex xs4>
          <!-- Major select -->
          <div class="headline">
            {{ Object.keys(productAttributes).sort()[0] | capitalize }} #{{ pvsIndex+1 }}
          </div>
          <v-layout
            row>
            <v-autocomplete
              :placeholder="`Select or add ${Object.keys(productAttributes).sort()[0]} *`"
              :items="filterAttributes((productAttributes[Object.keys(productAttributes).sort()[0]] || []), pvsIndex)"
              v-model="productVariantSets[pvsIndex].major"
              :search-input.sync="productVariantSets[pvsIndex].tempMajor"
              :no-data-text="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[0]) ? 'Click + button to add new type to system': 'No data found'"
              item-text="name"
              item-value="name"
            ></v-autocomplete>
            <v-btn
              color="success"
              fab small depressed
              class="mr-5 mt-2"
              @click="addCustomAttributeValue('major', pvsIndex, productVariantSets)"
              :disabled="!allowedToAddAttributeValue('major', pvsIndex)"
              v-if="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[0])"
            >
              <v-icon>add</v-icon>
            </v-btn>
          </v-layout>
          <v-checkbox
            :id="`default-image-${pvsIndex}`"
            label="Set as default image"
            v-model="defaultImagePvsIndex"
            :true-value="pvsIndex"
            :false-value="null"
          >
          </v-checkbox>
        </v-flex>
        <v-flex xs4>
          <!-- Image -->
          <picture-input
            width="200"
            height="200"
            margin="16"
            accept="image/jpeg,image/png"
            size="10"
            :z-index="0"
            button-class="v-btn theme--light info"
            :custom-strings="{
                            drag: 'Put image here'
                        }"
            :prefill="imageURL(set.resource)"
            :ref="`pictureInput${pvsIndex}`"
            @change="onImagePicked(pvsIndex, $event, false)">
          </picture-input>
        </v-flex>
        <v-flex xs4>
          <!-- Minor select -->
          <div v-if="Object.keys(productAttributes).length > 1">
            <div class="headline">
              {{ Object.keys(productAttributes).sort()[1] | capitalize }} #{{ pvsIndex+1 }}
            </div>

            <v-layout row wrap>
              <v-flex xs4
                      v-for="(productAttribute, pAttrIndex) in productAttributes[Object.keys(productAttributes).sort()[1]]"
                      :key="pAttrIndex"
                      :label="productAttribute.name"
              >
                <v-checkbox
                  class="mt-1"
                  :label="productAttribute.name"
                  v-model="productVariantSets[pvsIndex].minor[productAttribute.name]"
                ></v-checkbox>
              </v-flex>
            </v-layout>
            <v-form
              v-model="minorLockedInputValid"
              style="width: 100%"
              v-if="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[1])"
            >
              <v-layout row>
                <v-text-field
                  class="ml-3"
                  :placeholder="`Add ${Object.keys(productAttributes).sort()[1]} if not listed`"
                  :id="`new-minor-${pvsIndex}`"
                  v-model="newAttributesInputsMinor[pvsIndex]"
                  :rules="Object.keys(productAttributes).sort()[1].toLowerCase() == 'size' ? [validateCharLimit(10)] : []"
                ></v-text-field>
                <v-btn
                  color="success"
                  fab small depressed
                  class="mr-5 mt-2"
                  @click="addCustomAttributeValue('minor', pvsIndex, productVariantSets)"
                  :disabled="!allowedToAddAttributeValue('minor', pvsIndex)"
                >
                  <v-icon>add</v-icon>
                </v-btn>
              </v-layout>
            </v-form>
          </div>
        </v-flex>
      </v-layout>

      <!-- Remove button -->
      <div class="text-xs-right mt-3">
        <v-btn color="error" @click="removeProductVariantSet(pvsIndex)">remove set</v-btn>
      </div>

    </div>

    <!-- Default Variants -->
    <div
      v-if="defaultProductVariantSetsActive"
      class="pa-3 mb-3 ">

      <v-layout row wrap>
        <v-flex xs4>
          <!-- Major select -->
          <div class="headline">
            {{ Object.keys(productAttributes).sort()[0] | capitalize }} #{{ productVariantSets.length+1 }}
          </div>
          <v-layout
            row>
            <v-autocomplete
              :placeholder="`Select or add ${Object.keys(productAttributes).sort()[0]}`"
              :items="filterAttributes((productAttributes[Object.keys(productAttributes).sort()[0]] || []), productVariantSets.length)"
              v-model="defaultProductVariantSets.major"
              :search-input.sync="defaultProductVariantSets.tempMajor"
              :no-data-text="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[0]) ? 'Click + button to add new type to system': 'No data found'"
              item-text="name"
              item-value="name"
            ></v-autocomplete>
            <v-btn
              color="success"
              fab small depressed
              class="mr-5 mt-2 11"
              @click="addCustomAttributeValue('major', 0, [defaultProductVariantSets])"
              :disabled="!allowedToAddAttributeValue('major')"
              v-if="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[0])"
            >
              <v-icon>add</v-icon>
            </v-btn>
          </v-layout>
          <v-checkbox :id="`default-image-${productVariantSets.length}`" label="Set as default image"
                      :value="defaultImagePvsIndex === productVariantSets.length"
                      @click="defaultImagePvsIndex = productVariantSets.length"></v-checkbox>
        </v-flex>
        <v-flex xs4>
          <!-- Image -->
          <picture-input
            width="200"
            height="200"
            margin="16"
            accept="image/jpeg,image/png"
            size="10"
            :z-index="0"
            button-class="v-btn theme--light info"
            :custom-strings="{
                            drag: 'Put image here'
                        }"
            :prefill="imageURL(defaultProductVariantSets.resource)"
            :ref="`pictureInput${productVariantSets.length}`"
            @change="onImagePicked(productVariantSets.length, $event, true)">
          </picture-input>
        </v-flex>
        <v-flex xs4>
          <!-- Minor select -->
          <div v-if="Object.keys(productAttributes).length > 1">
            <div class="headline">
              {{ Object.keys(productAttributes).sort()[1] | capitalize }} #{{ productVariantSets.length+1 }}
            </div>

            <v-layout row wrap>
              <v-flex xs4
                      v-for="(productAttribute, pAttrIndex) in productAttributes[Object.keys(productAttributes).sort()[1]]"
                      :key="pAttrIndex"
                      :label="productAttribute.name"
              >
                <v-checkbox
                  class="mt-1"
                  :label="productAttribute.name"
                  v-model="defaultProductVariantSets.minor[productAttribute.name]"
                ></v-checkbox>
              </v-flex>
            </v-layout>
            <v-form
              v-model="minorInputValid"
              style="width: 100%"
              v-if="hasAccessToAddAttribute(Object.keys(productAttributes).sort()[1])"
            >
              <v-layout
                row>
                <v-text-field
                  class="ml-3"
                  :placeholder="`Add ${Object.keys(productAttributes).sort()[1]} if not listed`"
                  :id="`new-minor-${productVariantSets.length}`"
                  v-model="newAttributesInputsMinor[productVariantSets.length]"
                  :rules="Object.keys(productAttributes).sort()[1].toLowerCase() == 'size' ? [validateCharLimit(10)] : []"
                ></v-text-field>
                <v-btn
                  color="success"
                  fab small depressed
                  class="mr-5 mt-2"
                  @click="addCustomAttributeValue('minor', productVariantSets.length, [defaultProductVariantSets])"
                  :disabled="!allowedToAddAttributeValue('minor')"
                >
                  <v-icon>add</v-icon>
                </v-btn>
              </v-layout>
            </v-form>
          </div>
        </v-flex>
      </v-layout>
      <div class="text-xs-right mt-3">
        <v-btn
          v-if="productVariantSets.length > 0"
          color="error" @click="changeDefaultProductVariantSetsState">
          Cancel
        </v-btn>
        <v-btn color="success" @click="addProductVariantSet" :disabled="addProductVariantSetDisabled">
          Save
        </v-btn>
      </div>
    </div>
    <div
      class="text-xs-center mt-3"
      v-if="!defaultProductVariantSetsActive"
    >
      <v-btn
        color="success"
        fab small depressed
        class="mr-5 mt-2"
        @click="changeDefaultProductVariantSetsState">
        <v-icon>add</v-icon>
      </v-btn>
    </div>


    <v-divider class="mb-5 mt-5"></v-divider>

    <div class="display-1 mb-3">Product details</div>


    <!-- Basic info -->
    <v-form
      v-model="basicInfoFormValid"
      ref="basicInfoForm">
      <v-container grid-list-xs class="pa-0">
        <v-flex class="d-flex flex-nowrap">
          <v-select
            :items="vendorsSuppliersNamesList"
            v-model="vendor_name"
            label="Vendor name *"
            :rules="[validateNotEmpty]"
            :loading="vendorsSuppliersLoading"
            @focus="loadVendorsSuppliers"
            @change="updateVendorId"
          ></v-select>
          <div class="flex-grow-0 align-center d-flex" style="flex-grow:0 !important"
               v-if="~[1,2,3].indexOf($store.state.account.role.id)">
            <router-link :to="'/admin/vendors'" target="_blank">
              <v-btn flat text small color="primary" class="no-underline">New</v-btn>
            </router-link>
          </div>
        </v-flex>

        <v-text-field
          prefix="$"
          label="Vendor Cost #1 *"
          v-model.number="vendor_cost"
          :rules="[validateNumber, validateLimit(1000*10000)]">
        </v-text-field>
      </v-container>
    </v-form>

    <v-layout row wrap class="mt-3">
      <v-flex xs6 class="pa-3" v-if="addedCostAttribute">

        <div class="title mb-3">
          Added costs
        </div>

        <v-chip
          v-if="!canHaveAddedCosts"
          class="ma-2">
          Please add at least 2 variants to manage added costs
        </v-chip>

        <div v-else>
          <!-- TODO: upcharge attribute value -->
          <v-card class="elevation-2 mb-3"
                  v-for="(upcharge, index) in upcharges"
                  :key="index">

            <v-card-text>
              <p><b>Size:</b> {{upcharge.attribute.value}}</p>
              <p><b>Vendor Cost #{{ index+2 }}:</b> ${{upcharge.vendor_cost.toFixed(2)}}</p>
            </v-card-text>

            <v-divider></v-divider>
            <div class="text-xs-right px-2 py-2">
              <v-btn color="info" @click="editUpcharge(index)">edit</v-btn>
              <v-btn color="error" @click="removeUpcharge(index)">remove</v-btn>
            </div>

          </v-card>

          <v-form
            v-if="defaultUpchargesActive"
            v-model="upchargesFormValid"
            ref="upchargesForm">

            <!-- TODO: upcharge attribute value -->
            <v-layout row>
              <v-flex xs4>
                <v-select
                  :items="upchargeAttributeValues"
                  v-model="upchargeAttributeValue"
                  label="Size:"
                ></v-select>
              </v-flex>
              <v-flex xs4>
                <v-text-field
                  label="Custom vendor cost"
                  prefix="$"
                  v-model.number="upchargeVendorCost"
                  :rules="[validateNumber, validateLimit(1000*10000)]">
                </v-text-field>
              </v-flex>
            </v-layout>
            <div class="text-xs-right px-2 py-2">
              <v-btn
                color="error" @click="changeDefaultUpchargesActiveState">
                Cancel
              </v-btn>
              <v-btn color="success" :disabled="addUpchargeButtonDisabled" @click="addUpcharge">save</v-btn>
            </div>
          </v-form>
          <div
            class="text-xs-center mt-3"
            v-if="!defaultUpchargesActive"
          >
            <v-btn
              color="success"
              fab small depressed
              class="mr-5 mt-2"
              @click="changeDefaultUpchargesActiveState">
              <v-icon>add</v-icon>
            </v-btn>
          </div>
        </div>
      </v-flex>
      <v-flex xs6 class="pa3">

        <!-- Decorations -->

        <div class="title mb-3">Decorations</div>

        <v-card class="elevation-2 mb-3"
                v-for="(decoration, index) in decorations"
                :key="index">

          <v-card-text>
            <p><b>Decorator name:</b> {{decoration.decorator_name}}</p>
            <p><b>Logo description:</b> {{decoration.logo_description}}</p>
            <p><b>Decoration cost:</b> ${{decoration.decoration_cost.toFixed(2)}}</p>
            <p><b>Decoration location:</b> {{decoration.decoration_location}}</p>
          </v-card-text>

          <v-divider></v-divider>

          <div class="text-xs-right px-2 py-2">
            <v-btn color="info" @click="editDecoration(index)">edit</v-btn>
            <v-btn
              color="error"
              @click="removeDecoration(index)">
              remove
            </v-btn>
          </div>

        </v-card>

        <v-form
          v-if="defaultDecorationActive"
          v-model="decorationsFormValid"
          ref="decorationsForm">
          <v-container grid-list-xs class="pa-0">
            <v-layout row wrap>
              <v-flex xs6>
                <v-layout column wrap>
                  <v-flex>
                    <v-select
                      :items="vendorsDecoratorsNamesList"
                      :loading="vendorsDecoratorsLoading"
                      v-model="decorator_name"
                      label="Decorator Name"
                      @focus="loadVendorsDecorators"
                      @change="updateDecoratorId"
                    ></v-select>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="logo_description"
                      label="Logo description *">
                    </v-text-field>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex xs6>
                <v-layout column wrap>
                  <v-flex>
                    <v-text-field
                      v-model="decoration_cost"
                      label="Decoration cost *"
                      prefix="$"
                      :rules="[validateNumber, validateLimit(1000*10000)]">
                    </v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="decoration_location"
                      label="Decoration location *">
                    </v-text-field>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
            <div class="text-xs-right px-2 py-2">
              <v-btn
                v-if="decorations.length > 0"
                color="error" @click="changeDefaultDecorationActiveState">
                Cancel
              </v-btn>
              <v-btn color="success" :disabled="addDecorationButtonDisabled" @click="addDecoration">save</v-btn>
            </div>
          </v-container>
        </v-form>
        <div
          class="text-xs-center mt-3"
          v-if="!defaultDecorationActive"
        >
          <v-btn
            color="success"
            fab small depressed
            class="mr-5 mt-2"
            @click="changeDefaultDecorationActiveState">
            <v-icon>add</v-icon>
          </v-btn>
        </div>
      </v-flex>
    </v-layout>

    <!-- Additional info -->
    <v-layout row wrap>
      <v-flex xs6>
        <v-text-field
          disabled
          prefix="$"
          label="Bag Fold Label Cost"
          v-model="$store.state.campaign.BFLCost"
          :rules="[validateNumber, validateLimit(1000*10000)]">
        </v-text-field>
      </v-flex>
      <v-flex xs6>
        <!-- <v-text-field
          prefix="$"
          label="OW Cost"
          :value="$store.state.campaign.distributor ? $store.state.campaign.distributor.ow_cost.toFixed(2) : 0"
          disabled>
        </v-text-field> -->
      </v-flex>
    </v-layout>

    <!-- Total -->
    <v-card class="mt-3 mb-3 elevation-3">
      <v-card-title primary-title class="title">
        Total
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <table class="totals-table">
          <col width='34%'>
          <col width='33%'>
          <col width='33%'>
          <tr class="green-row">
            <th height="30">Total Cost #1</th>
            <th>Margin #1</th>
            <th>Sale Price #1</th>
          </tr>
          <tr>
            <td>${{totalCostWithoutMargin.toFixed(2)}}</td>
            <td class="text-xs-center">
              <v-text-field
                style="width: 100px; margin: 0 auto"
                label="Margin"
                suffix="%"
                @input="modifyMargin"
                :value="margin"
              ></v-text-field>
            </td>
            <td>
              <v-text-field
                style="width: 100px; margin: 0 auto"
                label="Sale Price"
                prefix="$"
                :value="totalCost"
                :rules="[validateNumber]"
                @input="modifyTotal">
              </v-text-field>
            </td>
          </tr>
          <tr v-if="margin < 30 || margin > 50">
            <td></td>
            <td>
              <small v-if="margin < 30">Your margin is less than suggested 40%. You may increase sales price</small>
              <small v-if="margin > 50">Your margin is more than suggested 40%. You may decrease sales price</small>
            </td>
            <td></td>
          </tr>
        </table>

        <table
          class="totals-table"
          v-for="(upcharge, index) in upcharges"
          :key="index"
        >
          <col width='34%'>
          <col width='33%'>
          <col width='33%'>
          <tr class="green-row">
            <th>Total Cost #{{ index+2 }} ({{ upcharge.attribute.value }})</th>
            <th>Margin #{{ index+2 }}</th>
            <th>Sale Price #{{ index+2 }}</th>
          </tr>
          <tr>
            <td>${{ upchargeTotalWithoutMargin(upcharge).toFixed(2) }}</td>
            <td>
              <v-text-field
                style="width: 100px; margin: 0 auto"
                label="Margin"
                prefix="%"
                :rules="[validateNumber, validateLimit(100)]"
                :value="upcharges[index].margin"
                @input="modifyUpchargeMargin(index, $event)"
              ></v-text-field>

            </td>
            <td>
              <v-text-field
                style="width: 100px; margin: 0 auto"
                label="Sale Price"
                prefix="$"
                :rules="[validateNumber]"
                :value="upcharges[index].total"
                @input="modifyUpchargeTotal(index, $event)"
              ></v-text-field>
            </td>
          </tr>
          <tr v-if="upcharges[index].margin < 30 || upcharges[index].margin > 50">
            <td></td>
            <td>
              <small v-if="upcharges[index].margin < 30">Your margin is less than suggested 40%. You may increase sales
                price</small>
              <small v-if="upcharges[index].margin > 50">Your margin is more than suggested 40%. You may decrease sales
                price</small>
            </td>
            <td></td>
          </tr>
        </table>

      </v-card-text>
    </v-card>

  </div>
</template>


<script>

  import axios from '@/axios'
  import PictureInput from 'vue-picture-input'
  import Vue from 'vue';

  import rules from '@/mixins/rules'
  import {DISTRIBUTOR_MANAGER_ROLE_ID, SALES_MANAGER_ROLE_ID} from "../../../../../../../config";

  const ADDED_COST_ATTRIBUTE = 2;
  const addedCostAttrCheck = attr => ~attr.name.toLowerCase().indexOf('size') || ~attr.associateWith.indexOf(ADDED_COST_ATTRIBUTE);

  export default {

    props: [
      'products', 'productName'
    ],

    mixins: [
      rules
    ],

    components: {
      PictureInput
    },

    data() {
      return {

        /* Vendors with 'decorator' property and product types of campaign's distributor */
        vendorsDecoratorsLoading: true,
        vendorsDecoratorsList: [],
        vendorsDecoratorsNamesList: [],

        /* Vendors with 'supplier' property and product types of campaign's distributor */
        vendorsSuppliersLoading: true,
        vendorsSuppliersList: [],
        vendorsSuppliersNamesList: [],

        sortingArr: [
          "XXS",
          "XS",
          "S", "SM",
          "M", "MD",
          "L", "LG",
          "XL",
          "XXL", "2XL",
          "XXXL", "3XL",
          "XXXXL", "4XL",
          "XXXXXL", "5XL",
          "XXXXXXL", "6XL"
        ],

        productAttributes: {},
        productAttributeIDs: {},
        // needed for added cost
        productTypeAttributes: [],

        // Product variants
        productVariantSets: [],             // [{"major": "name", "minor": {"name": boolean}}, ...]
        serverProductVariantSets: [],
        deletedServerProductVariantSets: [],
        newAttributesInputsMajor: {},            // {index: value}
        newAttributesInputsMinor: {},            // {index: value}
        defaultImagePvsIndex: null,
        minorInputValid: true,
        minorLockedInputValid: true,

        // default product variants
        defaultProductVariantSets: {
          'major': "",
          'minor': {},
          'resource': null,
          'image_name': null
        },
        defaultProductVariantSetsActive: false,

        // Basic info
        basicInfoFormValid: true,
        description: '',
        vendor_name: '',
        vendor_cost: '',
        vendor_id: '',
        margin: 10,
        totalCost: 0,
        bagFoldLabelCost: '',

        // Upchargres
        showUpcharges: false,
        upchargesFormValid: true,
        upchargeAttributeName: '',
        upchargeAttributeValue: null,
        upchargeVendorCost: '',
        upchargeCustomMargin: '',
        upcharges: [],
        defaultUpchargesActive: false,

        // Decorations
        decorationsFormValid: true,
        decorator_name: '',
        decorator_id: '',
        logo_description: '',
        decoration_cost: '',
        decoration_location: '',
        decorations: [],
        defaultDecorationActive: false,
      }
    },

    watch: {
      canHaveAddedCosts(value) {
        if (!value) {
          this.upcharges = [];
        }
      },

      // Update attributes list
      productName(name) {
        if (!name)
          return;
        this.loadProductTypeAttributes();
      },

      upchargeAttributeName() {
        // this.updateUpchargeAttributeValues()
      },
      selectedProductAttributes() {
        // this.updateUpchargeAttributeValues()
      },
      upchargeVendorCost() {
        let _ref = this.addUpchargeButtonDisabled
      },

      decorations() {
        this.modifyTotal(this.totalCost);
        this.upcharges.forEach((_, index) => {
          this.modifyUpchargeTotal(index, _.total)
        })
      },
      upcharges() {
        this.modifyMargin(this.margin);
        this.upcharges.forEach((_, index) => {
          this.modifyUpchargeMargin(index, _.margin)
        })
      },
      vendor_cost() {
        this.modifyTotal(this.totalCost);
        this.upcharges.forEach((_, index) => {
          this.modifyUpchargeTotal(index, _.total)
        })
      },

      productAttributes(val) {
        const attributeWithSize = Object.keys(val).find(v => ~v.toLowerCase().indexOf('size'));
        if (attributeWithSize) {
          return this.upchargeAttributeName = attributeWithSize;
        }
        if (this.addedCostAttribute) {
          this.upchargeAttributeName = this.addedCostAttribute.name;
        }
      },
    },

    computed: {
      canHaveAddedCosts() {
        return this.productVariantSets.length >= 1 && this.upchargeAttributeValues.length > 1;
      },
      addedCostAttribute() {
        return this.productTypeAttributes.find(addedCostAttrCheck);
      },

      upchargeAttributeValues() {
        let upchargeValues = [];
        this.productVariantSets.forEach(set => {
          const majorValue = set.major;
          const minorsValues = Object.keys(set.minor).filter(key => set.minor[key]);
          const minorValue = minorsValues[0];
          for (let [productAttributeName, productAttributeValues] of Object.entries(this.productAttributes)) {
            const itemMajor = productAttributeValues.find(val => val.name === majorValue);
            const itemMinor = productAttributeValues.find(val => val.name === minorValue);
            if (itemMajor) {
              const majorAttr = this.productTypeAttributes.find(attr => attr.name === productAttributeName);
              if (majorAttr && addedCostAttrCheck(majorAttr)) {
                upchargeValues.push(set.major);
              }
            }
            if (itemMinor) {
              const minorAttr = this.productTypeAttributes.find(attr => attr.name === productAttributeName);
              if (minorAttr && addedCostAttrCheck(minorAttr)) {
                upchargeValues.push(...minorsValues);
              }
            }
          }
        });
        /* TODO: custom sorting for secondary attribute, was like that:
        *  upchargeValues = this.sortingArr.filter(x => new Set(upchargeValues).has(x));
        * */
        return upchargeValues
      },

      owCost() {
        return this.$store.state.campaign.distributor ? this.$store.state.campaign.distributor.ow_cost : 0
      },

      totalCostWithoutMargin() {
        let total = parseFloat(this.$data.vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        return total || 0
      },


      // Buttons statuses
      addUpchargeButtonDisabled() {
        return !(this.$data.upchargesFormValid &&
          this.$data.upchargeAttributeName &&
          this.$data.upchargeAttributeValue &&
          (this.$data.upchargeVendorCost || this.$data.upchargeCustomMargin))
      },
      addDecorationButtonDisabled() {
        return !(this.$data.decorationsFormValid &&
          this.$data.logo_description &&
          this.$data.decoration_cost &&
          this.$data.decoration_location)
      },
      addProductVariantSetDisabled() {
        return !(this.defaultProductVariantSets.major && ~Object.values(this.defaultProductVariantSets.minor).indexOf(true));
      },
    },

    methods: {
      /**
       * Checks allownes to add new value to attribute
       * @param {'major' | 'minor' | Number} attributeType Type of attribute to add to
       * @param {Number} [pvsIndex] index of 'productVariantSets' item
       */
      allowedToAddAttributeValue(attributeType, pvsIndex) {
        const attrs = Object.keys(this.productAttributes).sort();
        let majorAttrName = attrs[0];
        let minorAttrName = Object.keys(this.productAttributes).length > 1 ? attrs[1] : null;
        if (attributeType === 'major') {
          const productTypeAttribute = this.productTypeAttributes.find(attr => attr.name === majorAttrName);

          if (productTypeAttribute && !this.allowAddAttributeValuesByRoles(productTypeAttribute)) {
            return false
          }

          if (typeof pvsIndex !== 'undefined') {
            return !(!this.productVariantSets[pvsIndex].tempMajor || this.productVariantSets[pvsIndex].major === this.productVariantSets[pvsIndex].tempMajor);
          } else {
            return !(!this.defaultProductVariantSets.tempMajor || this.defaultProductVariantSets.major === this.defaultProductVariantSets.tempMajor);
          }
        } else {
          const productTypeAttribute = this.productTypeAttributes.find(attr => attr.name === minorAttrName);

          if (productTypeAttribute && !this.allowAddAttributeValuesByRoles(productTypeAttribute)) {
            return false
          }

          if(typeof pvsIndex !== 'undefined') {
            return !(!this.newAttributesInputsMinor[pvsIndex] || !this.minorLockedInputValid);
          } else {
            return !(!this.newAttributesInputsMinor[this.productVariantSets.length] || !this.minorInputValid);
          }
        }
      },

      allowAddAttributeValuesByRoles(productTypeAttribute) {
        return !((
          /* check disallowed for distributors */
          !productTypeAttribute.allowDistributorsAddValues &&
          this.$store.state.account.role.id === DISTRIBUTOR_MANAGER_ROLE_ID
        ) || (
          /* check disallowed for sales */
          !productTypeAttribute.allowSalesAddValues &&
          this.$store.state.account.role.id === SALES_MANAGER_ROLE_ID
        ));
      },

      hasAccessToAddAttribute(attrName){
        const productType = this.productTypeAttributes.find(attr => attr.name === attrName);
        if(productType) {
          return this.allowAddAttributeValuesByRoles(productType);
        }
        return false;
      },

      changeDefaultDecorationActiveState() {
        this.defaultDecorationActive = !this.defaultDecorationActive
      },
      changeDefaultUpchargesActiveState() {
        this.defaultUpchargesActive = !this.defaultUpchargesActive
      },
      removeProductVariantSet(pvsIndex) {
        if (this.productVariantSets[pvsIndex].id) {
          this.productVariantSets[pvsIndex].id.forEach((pvsId) => {
            if (this.serverProductVariantSets.indexOf(pvsId) != -1) {
              this.deletedServerProductVariantSets.push(pvsId)
            }
          })
        }

        this.productVariantSets.splice(pvsIndex, 1);
        this.productVariantSets.length === 0 && (this.defaultProductVariantSetsActive = true)
      },

      changeDefaultProductVariantSetsState() {
        if (this.productVariantSets.length > 0) {
          this.defaultProductVariantSets.minor = Object.assign({}, this.productVariantSets[this.productVariantSets.length - 1].minor);
        }
        this.defaultProductVariantSetsActive = !this.defaultProductVariantSetsActive
      },

      // Form methods

      modifyMargin(val) {
        this.margin = val;
        let total = parseFloat(this.vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let divider = (1 - (parseFloat(this.margin) / 100));
        total = (total / divider) || 0;
        this.totalCost = total.toFixed(2)
      },

      modifyTotal(val) {
        this.totalCost = val;
        let total = parseFloat(this.vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let divider = (total / this.totalCost) || 0.9;
        this.margin = ((1 - divider) * 100).toFixed(2)
      },

      toFixedVal(val) {
        return parseFloat(val).toFixed(2)
      },

      modifyUpchargeMargin(index, val) {
        this.upcharges[index].margin = val;
        // Recalculate sale price
        let total = parseFloat(this.upcharges[index].vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let divider = (1 - (parseFloat(val) / 100));
        total = (total / divider) || 0;
        this.upcharges[index].total = total.toFixed(2)
      },

      modifyUpchargeTotal(index, val) {
        this.upcharges[index].total = val;
        let total = parseFloat(this.upcharges[index].vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let divider = (total / val) || 0.9;
        this.upcharges[index].margin = ((1 - divider) * 100).toFixed(4)
      },

      // For determining unique upcharge/decoration/etc.
      uid(obj) {
        let keys = Object.keys(obj).sort();
        let result = '';
        keys.forEach(key => {
          result += obj[key]
        });
        return result
      },

      upchargeTotalWithoutMargin(upcharge) {
        let total = parseFloat(upcharge.vendor_cost || this.vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        return total
      },

      upchargeTotal(upcharge) {
        let total = parseFloat(upcharge.vendor_cost || this.vendor_cost) +
          (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let divider = (1 - (parseFloat(upcharge.margin || this.margin) / 100));
        return (total / divider) || 0
      },

      init() {
        this.loadProductTypeAttributes();
        this.loadVendorsDecorators();
        this.loadVendorsSuppliers();
      },

      attributeValueComparator(selectedOption, optionId) {
        return parseInt(selectedOption) === parseInt(optionId);
      },

      async loadProductTypeAttributes() {
        // Extract product
        let product = this.$props.products.filter(x => x.name == this.$props.productName)[0];
        let attrs = {};
        let ids = {};

        const params = {
          headers: {
            'X-Filters': JSON.stringify({
              "field": "distributor_id",
              "op": "==",
              "value": this.$store.state.campaign.distributor.id
            })
          }
        };
        const {data: productAttributes} = await this.$axios.get(`/products/types/${product.product_type_id}/product-attributes`, params);
        /* load global values & distributor's ones */
        const valuesResponses = await Promise.all(productAttributes.map(pa => this.$axios.get(`/products/product-attributes/${pa.id}/values`, params)));

        productAttributes.forEach((attr, index) => {
          attrs[attr.name] = valuesResponses[index].data || [];
          ids[attr.name] = attr.id;
        });
        this.productAttributes = attrs;
        this.productAttributeIDs = ids;
        this.productTypeAttributes = productAttributes;

        return productAttributes;
      },

      /**
       * Get vendors only with 'decorator' property & product types of campaign
       * @returns {Promise<Vendor[]>}
       */
      async loadVendorsDecorators() {
        let data = [];
        try {
          this.vendorsDecoratorsLoading = true;
          const productTypesIds = this.$store.state.campaign.distributor.related_product_types.map(rpt => rpt.product_type.id);
          const response = await axios.get(`/vendors?is_decorator=true&product_types=${productTypesIds}`);
          data = response.data;
          this.vendorsDecoratorsList = data;
          this.vendorsDecoratorsNamesList = data.map(x => x.name).sort();
        } catch (e) {
          console.error(e);
        }
        this.vendorsDecoratorsLoading = false;
        return data;
      },

      /**
       * TODO: refactor to Vendor entity
       * During selection of decorator updates selected decorator_id
       * @param {string} decorator_name Name of decorator
       */
      updateDecoratorId(decorator_name) {
        const item = this.vendorsDecoratorsList.find(d => d.name === decorator_name);
        this.decorator_id = item ? item.id : '';
      },

      /**
       * TODO: refactor to Vendor entity
       * During selection of vendor updates selected vendor_id
       * @param {string} vendor_name Name of vendor
       */
      updateVendorId(vendor_name) {
        const item = this.vendorsSuppliersList.find(d => d.name === vendor_name);
        this.vendor_id = item ? item.id : '';
      },

      /**
       * Get vendors only with 'supplier' property & product types of campaign
       * @returns {Promise<Vendor[]>}
       */
      async loadVendorsSuppliers() {
        let data = [];
        try {
          this.vendorsSuppliersLoading = true;
          const productTypesIds = this.$store.state.campaign.distributor.related_product_types.map(rpt => rpt.product_type.id);
          const response = await axios.get(`/vendors?is_supplier=true&product_types=${productTypesIds}`);
          data = response.data;
          this.vendorsSuppliersList = data;
          this.vendorsSuppliersNamesList = data.map(x => x.name).sort();
        } catch (e) {
          console.error(e);
        }
        this.vendorsSuppliersLoading = false;
        return data;
      },

      load(productVariants) {
        // Wait for attributes loading
        if (!Object.keys(this.productAttributes).length) {
          setTimeout(this.load, 1000, productVariants);
          return
        }
        // Basic info
        let pvsWithoutCustomMargin = productVariants.filter(x => x.custom_margin == false);
        this.description = productVariants[0].description;

        this.vendor_name = productVariants[0].vendor_name;
        this.vendor_id = productVariants[0].vendor_id;
        this.vendor_cost = productVariants.filter(pv => !pv.custom_vendor_cost)[0] ? productVariants.filter(pv => !pv.custom_vendor_cost)[0].vendor_cost : 0;

        this.margin = pvsWithoutCustomMargin.length ? pvsWithoutCustomMargin[0].margin : productVariants[0].margin;
        // Decorations
        let decorations = {};
        productVariants.forEach(pv => {
          pv.decorations.forEach(decoration => {
            decorations[this.uid(decoration)] = decoration
          })
        });
        this.decorations = Object.values(decorations);
        // Upcharges
        let upchargedProductVariants = [];
        //  Find upcharged products
        productVariants.forEach(pv => {
          if (pv.upcharged_attribute)
            upchargedProductVariants.push(pv)
        });
        //  Generate upcharges
        let upcharges = {};
        upchargedProductVariants.forEach(pv => {
          let attrs = {};
          pv.attributes.forEach(attr => {
            attrs[attr.name] = attr.value
          });
          let upcharge = {
            attribute: {
              name: pv.upcharged_attribute,
              value: attrs[pv.upcharged_attribute]
            },
            vendor_cost: pv.vendor_cost,
            margin: pv.margin
          };
          upcharges[this.uid(upcharge)] = upcharge
        });
        this.upcharges = Object.values(upcharges);

        let sortingArr = this.sortingArr;
        this.upcharges = this.upcharges.sort(function (a, b) {
          return sortingArr.indexOf(a.attribute.value) - sortingArr.indexOf(b.attribute.value);
        });
        // Variants
        let majorAttrName = Object.keys(this.productAttributes).sort()[0];
        let minorAttrName = Object.keys(this.productAttributes).length > 1 ? Object.keys(this.productAttributes).sort()[1] : null;
        let variantSets = [];
        productVariants.forEach(pv => {
          let attrs = {};
          pv.attributes.forEach(attr => {
            attrs[attr.name] = attr.value
          });
          // Try to add in existing variants set
          let added = false;
          variantSets.forEach((vs, index) => {
            if (vs.major == attrs[majorAttrName]) {
              added = true;
              variantSets[index].minor[attrs[minorAttrName]] = true;
              variantSets[index].id.push(pv.id)
            }
          });
          // Add new variants set
          if (!added) {
            let variant = {
              id: [pv.id],
              major: attrs[majorAttrName],
              minor: {},
              resource: pv.resources[0] || null,
              image_name: null
            };
            variant.minor[attrs[minorAttrName]] = true;
            variantSets.push(variant)
          }
        });
        this.productVariantSets = variantSets;
        /*            if (!variantSets.length) {
                        this.addProductVariantSet()
                    }*/
        this.modifyMargin(this.margin);
        this.upcharges.forEach((_, index) => {
          this.modifyUpchargeMargin(index, _.margin)
        });
        // Load default image
        let product = this.$parent.$parent.$parent.$parent.$data.editing;
        if (product) {
          this.productVariantSets.forEach((vs, index) => {
            if (
              vs.resource &&
              vs.resource.meta &&
              product.resources &&
              product.resources.length &&
              vs.resource.hash === product.resources[0].hash
            ) {
              this.defaultImagePvsIndex = index;
            }
          });
          this.serverProductVariantSets = product.product_variants.map(pv => pv.id);
        }
      },

      // Product variants
      addProductVariantSet() {
        this.productVariantSets.push(this.defaultProductVariantSets);
        this.defaultProductVariantSets = {'major': "", 'minor': {}, 'resource': null, 'image_name': null};
        this.defaultProductVariantSetsActive = false;
      },
      toggleAttribute(attributeName, attributeValue) {
        // Empty case
        if (!this.$data.selectedProductAttributes[attributeName]) {
          this.$data.selectedProductAttributes[attributeName] = []
        }
        // Add
        if (this.$data.selectedProductAttributes[attributeName].indexOf(attributeValue) === -1) {
          this.$data.selectedProductAttributes[attributeName].push(attributeValue)
        }
        // Remove
        else {
          this.$data.selectedProductAttributes[attributeName] =
            this.$data.selectedProductAttributes[attributeName].filter(x => x !== attributeValue)
        }
        // Trigger upcharge
        // this.updateUpchargeAttributeValues()
      },

      // Upcharges
      updateUpchargeAttributeValues() {
        if (!this.upchargeAttributeName) {
          this.upchargeAttributeValues = [];
          return
        }
        let lowerProductAttributes = {};
        Object.keys(this.productAttributes).forEach(name => {
          let value = this.productAttributes[name.toLowerCase()];
          lowerProductAttributes[name] = value
        });
        this.upchargeAttributeValues = this.productAttributes[this.upchargeAttributeName]
      },
      addUpcharge() {
        if (this.upcharges.filter(x =>
          x.attribute.name == this.upchargeAttributeName &&
          x.attribute.value == this.upchargeAttributeValue).length) {
          this.$store.dispatch('raiseError', 'This attribute is already upcharged');
          return
        }
        this.$data.upcharges.push({
          attribute: {
            name: this.$data.upchargeAttributeName,
            value: this.$data.upchargeAttributeValue,
          },
          vendor_cost: parseFloat(this.$data.upchargeVendorCost) || 0,
          margin: parseFloat(this.$data.upchargeCustomMargin) || this.margin
        });
        let sortingArr = this.sortingArr;
        this.upcharges.sort(function (a, b) {
          return sortingArr.indexOf(a.attribute.value) - sortingArr.indexOf(b.attribute.value);
        });
        this.$refs.upchargesForm.reset();
        this.changeDefaultUpchargesActiveState()
      },
      editUpcharge(index) {
        this.defaultUpchargesActive = true;
        let upcharge = this.$data.upcharges[index];
        this.$data.upchargeAttributeName = upcharge.attribute.name;
        this.$data.upchargeAttributeValue = upcharge.attribute.value;
        this.$data.upchargeVendorCost = upcharge.vendor_cost;
        this.$data.upcharges.splice(index, 1)
      },
      removeUpcharge(index) {
        this.$data.upcharges.splice(index, 1)
      },

      // Decorations
      addDecoration() {
        this.$data.decorations.push({
          'decorator_name': this.$data.decorator_name,
          'decorator_id': this.$data.decorator_id,
          'logo_description': this.$data.logo_description,
          'decoration_cost': parseFloat(this.$data.decoration_cost),
          'decoration_location': this.$data.decoration_location
        });
        this.changeDefaultDecorationActiveState();
        this.$refs.decorationsForm.reset()
      },
      editDecoration(index) {
        this.defaultDecorationActive = true;
        this.$data.decorator_name = this.$data.decorations[index]['decorator_name'];
        this.$data.decorator_id = this.$data.decorations[index]['decorator_id'];
        this.$data.logo_description = this.$data.decorations[index]['logo_description'];
        this.$data.decoration_cost = this.$data.decorations[index]['decoration_cost'];
        this.$data.decoration_location = this.$data.decorations[index]['decoration_location'];
        this.$data.decorations.splice(index, 1)
      },
      removeDecoration(index) {
        this.$data.decorations.splice(index, 1);
        this.$data.decorations.length === 0 && (this.defaultDecorationActive = true)
      },

      // Totals
      calulateUpchargeTotalCost(upcharge) {
        let total = parseFloat(upcharge.vendor_cost || this.$data.vendor_cost) +
          parseFloat(this.$store.state.campaign.BFLCost) +
          this.owCost;
        this.$data.decorations.forEach(x => total += parseFloat(x.decoration_cost));
        let margin = (upcharge.margin || parseFloat(this.$data.margin));
        let divider = (1 - (margin / 100));
        return (total / divider) || 0
      },

      /**
       * Add custom value. Makes request to add new value, loads product types attributes and selects value in ui
       * @param {'major' | 'minor' | Number} attrType Major/minor attribute
       * @param {Number} index Index in product variant sets
       * @param {ProductVariantSet[]} pvSets An array with all "ProductVariantSet"s or with one "Default ProductVariantSet"
       * @returns {Promise<void>}
       */
      async addCustomAttributeValue(attrType, index, pvSets) {
        let attrName = Object.keys(this.productAttributes).sort()[attrType === 'major' ? 0 : 1];
        let attrID = this.productAttributeIDs[attrName];
        let value = attrType === 'major' ? pvSets[index].tempMajor : this.newAttributesInputsMinor[index];

        const {data: [newAddedValue]} = await this.$axios.post(`/products/product-attributes/${attrID}/values`, [{
          name: value,
          product_attribute_id: attrID,
        }]);
        await this.loadProductTypeAttributes();

        if(attrType === 'major') {
          pvSets[index].major = newAddedValue.name;
        } else {
          Vue.set(pvSets[index].minor, newAddedValue.name, true);
        }

        this.$store.dispatch('raiseSuccess', 'Attribute added');
      },

      imageURL(resource) {
        if (!resource) {
          return null
        }
        return `${process.env.API_BASE_URL}` +
          `/static` +
          `/resources` +
          `/${resource.uuid}` +
          `.${resource.type}`
      },

      onImagePicked(pvsIndex, img, isDefault) {
        // Pass no image
        this._upload(pvsIndex, img, isDefault)
      },

      _upload(pvsIndex, img, isDefault) {
        // Prepare params
        let params = {
          headers: {
            'Authorization': this.$store.state.token
          }
        };
        let url = '/data_resources/b64';
        let data = {
          'b64_img': img,
          'meta': JSON.stringify({'pvsIndex': pvsIndex}),
          'linked_to': Math.random().toString(36).substring(7)
        };
        // Upload
        axios.post(url, data, params).then(resp => {
          if (isDefault) {
            this.defaultProductVariantSets.resource = resp.data;
            this.defaultProductVariantSets.image_name = 'temp'
          } else {
            this.productVariantSets[pvsIndex].resource = resp.data;
            this.productVariantSets[pvsIndex].image_name = 'temp'
          }
        }).catch(err => {
          console.error(err);
          this.$store.dispatch('raiseError', err);
        })
      },

      // Final result, that would be used in parent

      productVariants(callback) {
        // Final storage
        let pvs = [];
        let removed_pvs = this.deletedServerProductVariantSets;
        let pvsTotalVariant = 0;
        let productAttributes = this.productAttributes;
        // Interate sets
        this.productVariantSets.forEach(pvset => {
          // Handle not full set
          if (Object.keys(productAttributes).length === 1 &&
            pvset.major == '')
            return;
          if (Object.keys(productAttributes).length === 2 &&
            (pvset.major == '' || !Object.keys(pvset.minor).length))
            return;
          // If no minor attribute, add empty record
          if (!Object.keys(pvset.minor).length)
            pvset.minor[null] = true;
          // Create combinations
          let major = pvset.major;
          Object.keys(pvset.minor).forEach(minor => {

            if (!pvset.minor[minor])
              return;

            // Generate attributes
            let attributes = [];
            attributes.push({
              name: Object.keys(productAttributes).sort()[0],
              value: major
            });
            if (Object.keys(productAttributes).length > 1) {
              attributes.push({
                name: Object.keys(productAttributes).sort()[1],
                value: minor
              })
            }

            // Determine upcharge and margin
            let vendor_cost = parseFloat(this.$data.vendor_cost);
            let margin = parseFloat(this.$data.margin);
            let upchargedAttribute = null;
            let customMargin = false;
            let customVendorCost = false;
            attributes.forEach(attr => {
              this.$data.upcharges.forEach(_upcharge => {
                if (attr.name == _upcharge.attribute.name &&
                  attr.value == _upcharge.attribute.value) {
                  vendor_cost = _upcharge.vendor_cost;
                  customVendorCost = true;
                  upchargedAttribute = attr.name;
                  if (_upcharge.margin) {
                    margin = parseFloat(_upcharge.margin);
                    customMargin = true
                  }
                }
              })
            });

            let decorations = JSON.parse(JSON.stringify(this.decorations));
            const vendor_id = this.vendor_id;
            let vendor_name = '';
            try {
              vendor_name = JSON.parse(JSON.stringify(this.vendor_name));
            } catch (e) {
            }

            // Local resource for variant

            pvsTotalVariant++;

            if (pvset.resource) {
              let params = {headers: {'Authorization': this.$store.state.token}};
              axios.post(`/data_resources/${pvset.resource.uuid}/duplicate`, null, params).then(resp => {
                // Calculate price
                let price = parseFloat(vendor_cost) +
                  (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
                  parseFloat(this.$store.state.campaign.distributor.ow_cost);
                decorations.forEach(x => price += parseFloat(x.decoration_cost));
                let divider = (1 - (parseFloat(margin) / 100));
                price = (price / divider) || 0;
                // Collect data
                let data = {
                  'vendor_name': vendor_name,
                  'vendor_id': vendor_id,
                  'vendor_cost': vendor_cost,
                  'margin': margin,
                  'upcharged_attribute': upchargedAttribute,
                  'custom_margin': customMargin,
                  'custom_vendor_cost': customVendorCost,
                  'decorations': decorations,
                  'attributes': attributes,
                  'resources': [resp.data],
                  'price': price
                };
                // Save to pvs list
                pvs.push(data);
                //return pvs
                if (pvs.length == pvsTotalVariant) {
                  // all variants resources loaded
                  const all_pvs = this.serverProductVariantSets;
                  callback(pvs, removed_pvs, all_pvs)
                }
              }).catch(error => {
                let price = parseFloat(vendor_cost) +
                  (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
                  parseFloat(this.$store.state.campaign.distributor.ow_cost);
                decorations.forEach(x => price += parseFloat(x.decoration_cost));
                let divider = (1 - (parseFloat(margin) / 100));
                price = (price / divider) || 0;
                // Collect data
                let data = {
                  'vendor_name': vendor_name,
                  'vendor_cost': vendor_cost,
                  'vendor_id': vendor_id,
                  'margin': margin,
                  'upcharged_attribute': upchargedAttribute,
                  'custom_margin': customMargin,
                  'custom_vendor_cost': customVendorCost,
                  'decorations': decorations,
                  'attributes': attributes,
                  'resources': [],
                  'price': price
                };
                // Save to pvs list
                pvs.push(data);
                //return pvs
                if (pvs.length == pvsTotalVariant) {
                  // all variants resources loaded
                  const all_pvs = this.serverProductVariantSets;
                  callback(pvs, removed_pvs, all_pvs)
                }
              });
            } else {
              // Calculate price
              let price = parseFloat(vendor_cost) +
                (parseFloat(this.$store.state.campaign.BFLCost) || 0) +
                parseFloat(this.$store.state.campaign.distributor.ow_cost);
              decorations.forEach(x => price += parseFloat(x.decoration_cost));
              let divider = (1 - (parseFloat(margin) / 100));
              price = (price / divider) || 0;
              // Collect data
              let data = {
                'vendor_name': vendor_name,
                'vendor_cost': vendor_cost,
                'vendor_id': vendor_id,
                'margin': margin,
                'upcharged_attribute': upchargedAttribute,
                'custom_margin': customMargin,
                'custom_vendor_cost': customVendorCost,
                'decorations': decorations,
                'attributes': attributes,
                'resources': [],
                'price': price
              };
              // Save to pvs list
              pvs.push(data)
            }
          })
        });

        if (pvs.length == pvsTotalVariant) {
          // all variants resources loaded
          const all_pvs = this.serverProductVariantSets;
          callback(pvs, removed_pvs, all_pvs);
        }

      },

      filterAttributes(attributes, pvsIndex) {
        let selectedAttributes = [];
        this.productVariantSets.forEach((set, i) => {
          (i !== pvsIndex) && selectedAttributes.push(set.major);
        });
        /* Show only values of major attribute that are not selected */
        return attributes.filter(x => !selectedAttributes.includes(x.name));
      },

      validateMargin(val) {
        if (val === Infinity || val === -Infinity) {
          return 'Please, provide sale price'
        }
        return true
      }
    }
  }
</script>


<style scoped>
  .v-messages {
    max-height: 0 !important;
    min-height: 0 !important;
  }

  .totals-table {
    width: 100%;
    border-collapse: collapse;
  }

  .totals-table td:first-child, th:first-child {
    border: none;
  }

  .green-row {
    color: white;
    background-color: #44C038;
  }

  .totals-table td, th {
    text-align: center;
    padding: 10px;
  }
</style>
