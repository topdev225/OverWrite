<template>
  <div>
    <v-card>

      <v-card-title primary-title class="headline">
        Report Builder
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <div class="title">Basic parameters</div>
        <v-form class="mt-3">
          <v-autocomplete
            :disabled="lockedCampaign"
            :items="campaigns"
            v-model="selectedCampaign"
            label="Campaign"
            item-text="name"
            @focus="loadCampaigns()"
            return-object
          >
            <template slot='selection' slot-scope='{ item }'>
              <p v-if="item.complete"><b>Distributor PO:</b> {{ item.distributor_po }}, {{ item.name }}</p>
              <p v-else> {{ item.name }} </p>
            </template>

            <template slot='item' slot-scope='{ item }'>
              <p v-if="item.complete"><b>Distributor PO:</b> {{ item.distributor_po }}, {{ item.name }}</p>
              <p v-else> {{ item.name }} </p>
            </template>
          </v-autocomplete>

          <v-autocomplete
            :items="availableReports"
            v-model="selectedReport"
            @focus="loadAvailableReports()"
            label="Report"
            item-text="name"
            return-object
          >
          </v-autocomplete>
        </v-form>
        <div v-if="showFilters">
          <div class="title">Filters</div>
          <div
            v-for="(filters, table) in selectedReportFilters"
            :key="table"
          >
            <div v-if="filters.length" class="mt-2">{{ table }} table</div>
            <div
              v-for="filter in filters"
              :key="filter.name"
            >
              <v-select
                v-if="filter.variants"
                :items="filterVariants[`${table}${filter.separator}${filter.field}`]"
                v-model="providedFilters[`${table}${filter.separator}${filter.field}`]"
                :label="filter.name"
              ></v-select>
              <v-text-field
                v-else
                :label="filter.name"
                v-model="providedFilters[`${table}${filter.separator}${filter.field}`]"
              ></v-text-field>
            </div>
          </div>
        </div>
        <div v-if="campaigns.length && availableReports.length">
          <div class="mt-3">
            <v-alert
              :value="!isGenWebAllowed"
              color="error"
              icon="priority_high"
              outline
            >
              <div>
                <strong>"{{selectedReport ? selectedReport.name : ''}}"</strong> web reports are not available until
                campaign is completed. You can
                <v-btn small color="error" @click.capture="openCompleteCampaignDialog()">complete</v-btn>
                campaign from here or you can do it from
                <strong>
                  <router-link to="/admin/campaigns">campaigns list.</router-link>
                </strong>
              </div>
            </v-alert>
          </div>
          <div class="mt-3">
            <v-alert
              :value="!isGenPdfCsvAllowed"
              color="error"
              icon="priority_high"
              outline
            >
              <div>
                <strong>"{{selectedReport ? selectedReport.name : ''}}"</strong> CSV and PDF reports eports are not
                available until
                campaign is completed. You can
                <v-btn small color="error" @click.capture="openCompleteCampaignDialog()">complete</v-btn>
                campaign from here or you can do it from
                <strong>
                  <router-link color="error" to="/admin/campaigns">campaigns list.</router-link>
                </strong>
              </div>
            </v-alert>
          </div>
        </div>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions class="pa-3">
        <v-btn :disabled="!isGenWebAllowed" @click="generateReport('web')">
          <v-icon left dark>web</v-icon>
          Web
        </v-btn>
        <v-btn :disabled="!isGenPdfCsvAllowed" @click="generateReport('csv')" >
          <div class="mr-3 d-flex align-center">
            <CsvIcon style="width:22px; height:22px; fill: currentColor"></CsvIcon>
          </div>
          CSV
        </v-btn>
        <v-btn :disabled="!isGenPdfCsvAllowed" @click="generateReport('pdf')">
          <div class="mr-3 d-flex align-center">
            <PdfIcon style="width:22px; height:22px; fill: currentColor"></PdfIcon>
          </div>
          PDF
        </v-btn>
      </v-card-actions>

    </v-card>

    <complete-campaign-dialog
      :campaign="completeCampaign"
      @update="loadCampaigns(true)"
      @close="closeCompleteCampaignDialog()"
    />
  </div>
</template>

<script>

    import axios from '@/axios'
    import CsvIcon from '@/../static/images/csv-file-format-extension.svg?inline';
    import PdfIcon from '@/../static/images/pdf-file-format-symbol.svg?inline';
    import CompleteCampaignDialog from "../../Catalog/CompleteCampaignDialog";

    export default {
        name: 'ReportBuilder',

        data() {
            return {
                params: {headers: {'Authorization': this.$store.state.token}},
                reportsCompleteMode: ['Bin', 'Label Report',
                    'Pick, Pack and Bag', 'Decorator PO',
                    'Vendor PO', 'Location PO', 'All'],
                campaigns: [],
                availableReports: [],

                selectedCampaign: null,
                selectedReport: null,
                lockedCampaign: false,

                providedParams: {},
                providedFilters: {},
                providedSort: null,

                filterVariants: {},

                completeCampaignDialogOpened: false,
                completeCampaign: null,
            }
        },

        computed: {
            showFilters() {
                let totalFilters = 0;
                let filters = this.selectedReportFilters;
                if (!filters) {
                    return false
                }
                if (!this.selectedCampaign) {
                    return false
                }
                Object.keys(filters).forEach(tableName => {
                    totalFilters += filters[tableName].length
                });
                return !!totalFilters
            },
            selectedReportFilters() {  // {table1: [filter1, filter2, ...], ... }
                let filters = {};
                if (!this.selectedReport) {
                    return filters
                }
                this.selectedReport.tables.forEach(table => {
                    !filters[table.name] && (filters[table.name] = []);
                    filters[table.name] = filters[table.name].concat(table.filters)
                });
                return filters
            },
            isGenWebAllowed() {
                if (!this.selectedCampaign || !this.selectedReport) {
                    return false;
                }
                return this.selectedCampaign.complete || !~this.reportsCompleteMode.indexOf(this.selectedReport.name);
            },
            isGenPdfCsvAllowed() {
                if (!this.selectedCampaign || !this.selectedReport || !this.selectedCampaign.complete) {
                    return false;
                } else {
                  return true
                }
                //return ~this.reportsCompleteMode.indexOf(this.selectedReport.name);
            },
        },

        watch: {
            showFilters(val) {
                val && this.loadVariants()
            },
            selectedCampaign() {
                this.showFilters && this.loadVariants()
            },
            '$route'(to, from) {
                setTimeout(function () {
                    this.loadCampaigns(true);
                    this.loadAvailableReports(true);
                }.bind(this), 100)
            }
        },

        mounted() {
            this.loadCampaigns(true);
            this.loadAvailableReports(true);
        },

        methods: {
            loadCampaigns(reset) {
                axios.get('/campaigns', this.params).then(resp => {
                    this.campaigns = resp.data;
                    if (reset) {
                        if (this.$store.state.account.campaign.id && this.$store.state.account.role.name !== 'Admin Buyer') {
                            this.lockedCampaign = true
                            return this.selectedCampaign = this.campaigns.find(c => c.id == this.$store.state.account.campaign.id);
                        } else {
                            this.lockedCampaign = false
                        }
                        if (localStorage.getItem('tempReportCampaignID')) {
                            let found = this.campaigns.find(function (element) {
                                return element.id == localStorage.getItem('tempReportCampaignID')
                            });
                            return this.selectedCampaign = found
                        }
                        this.selectedCampaign = !this.selectedCampaign ? this.campaigns[0] : this.campaigns.find(c => c.id  === this.selectedCampaign.id);
                    }
                }).catch(err => {
                    this.$store.dispatch('raiseError', err)
                })
            },
            loadAvailableReports(reset) {
                axios.get('/reports', this.params).then(resp => {
                    this.availableReports = resp.data;
                    if (reset) {
                        this.selectedReport = this.availableReports.filter(r => r.name === this.$route.query.report)[0]
                    }
                }).catch(err => {
                    this.$store.dispatch('raiseError', err)
                })
            },
            loadVariants() {
                // Filter variants
                Object.keys(this.selectedReportFilters).forEach(tableName => {
                    this.selectedReportFilters[tableName].forEach(filter => {
                        if (filter.variants) {
                            let url = filter.variants;
                            url += `?campaign_id=${this.selectedCampaign.id}`;
                            axios.get(url, this.params).then(resp => {
                                this.$set(this.filterVariants, `${tableName}${filter.separator}${filter.field}`, resp.data)
                            }).catch(err => {
                                this.$store.dispatch('raiseError', err)
                            })
                        }
                    })
                })
            },

            /**
             * Generates report file or redirects to reports table
             * @param {('web' | 'csv' | 'pdf')} reportType='web' Type of generated report
             */
            generateReport(reportType = 'web') {
                this.$emit('submit', {
                    type: reportType,
                    campaign: this.selectedCampaign,
                    report: this.selectedReport,
                    filters: this.providedFilters
                })
            },

            openCompleteCampaignDialog() {
                if (this.selectedCampaign && !this.selectedCampaign.complete) {
                    this.completeCampaign = this.selectedCampaign;
                }
            },
            closeCompleteCampaignDialog() {
                this.completeCampaign = null;
            }
        },

        components: {
            CsvIcon,
            PdfIcon,
            CompleteCampaignDialog,
        }
    }
</script>
