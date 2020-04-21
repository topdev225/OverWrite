<template>
  <v-layout row wrap justify-center class="mb-5">
    <v-flex xs10 mt-5>
      <div class="text-xs-center headline">
        {{ report.meta.campaign.name }} - {{ report.meta.report.name }}
        <!-- Specific solution for Vendor PO (Task 46) -->
        <span v-if="report.meta.report.name == 'Vendor PO' && report.meta.filters['Vendor PO:vendor_name']">
          - {{ report.meta.filters['Vendor PO:vendor_name'] }}
        </span>
      </div>
    </v-flex>
    <v-flex
      v-for="table in report.data.tables"
      :key="table.name"
      xs10 mt-3
    >
      <div class="title">{{ table.name }}</div>
      <v-data-table
        :headers="table.columns.map(c => ({text: c, value: c}))"
        :items="table.rows"
        class="elevation-1 mt-3"
        disable-initial-sort
        :custom-sort="customSort"
      >
        <template slot="items" slot-scope="props">
            <td v-for="(column, index) in table.columns" :key="index">
                {{ props.item[column] }}
            </td>
        </template>
      </v-data-table>
      <div
        v-for="(value, name) in table.meta"
        :key="name"
        class="title text-xs-right mt-2"
      >
        {{ name }}: {{ value }}
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'ReportLayout',
  props: {
    report: Object,
  },
  methods: {
    customSort(items, index, isDescending) {
      // Ignore Itemized Shopper report
      if (this.$props.report.meta.report.name === 'Itemized Shopper') {
        return items
      }
      items.sort((a, b) => {
        let tmpa = Object.assign({}, a);
        let tmpb = Object.assign({}, b);
        if (index === 'Bin Number') {
          tmpa[index] = parseInt(a[index].substr(4));
          tmpb[index] = parseInt(b[index].substr(4));
        }
        if (isDescending) {
          return tmpa[index] > tmpb[index] ? -1 : 1;
        } else {
          return tmpa[index] < tmpb[index] ? -1 : 1;
        }
       });
      return items
    }
  }
}
</script>
