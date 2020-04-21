<template>
  <div>
    <v-layout justify-center v-if="!report.data && !campaign">
        <v-flex xs10 mt-5>
          <report-builder
            @submit="handleReportBuilderSubmit"
          />
        </v-flex>
    </v-layout>
    <report-layout
      v-else
      :report="report"
    />
  </div>
</template>


<script>

import ReportBuilder from './ReportBuilder'
import ReportLayout from './ReportLayout'

import axios from '@/axios'

export default {
  name: 'ReportPage',
  
  components: {
    ReportBuilder,
    ReportLayout
  },

  data () {
    return {
      report: {
        meta: null,
        data: null
      },
      campaign: null
    }
  },

  watch: {
    '$route' (to, from) {
      this.report = {meta: null, data: null}
      this.campaign = null
    }
  },

  methods: {

    handleReportBuilderSubmit (params) {
      console.log(params)
      if (params.type == 'web')
        this.showReport(params)
      else if (params.type == 'csv')
        this.downloadReport(params)
      else if (params.type == 'pdf')
        this.downloadReport(params)
    },
    downloadReport (params) {
      // Basic url
      let url = NaN
      if (params.type == 'pdf') {
        url =`/reports/${params.report.name}/pdf/${params.campaign.id}`
      }
      else if (params.type == 'csv') {
        url =`/reports/${params.report.name}/csv/${params.campaign.id}`
      }
      // Build report settings
      let settings = {
        params: [],
        filters: params.filters,
        sort: null,
        userTimeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      }
      // Build request params
      let rparams = {headers: {
        'R-Settings': JSON.stringify(settings)
      }}
      axios.get(url, rparams).then(resp => {
        let res = resp.data
        console.log(res)
        window.open(`${process.env.API_BASE_URL}/static/resources/${res.uuid}.${res.type}`, '_blank')
      }).catch(err => {
         this.$store.dispatch('raiseError', err.response.data.message)
      })
    },
    showReport (params) {
      // Basic url
      let url =`/reports/${params.report.name}/json/${params.campaign.id}`
      // Build report settings
      let settings = {
        params: [],
        filters: params.filters,
        sort: null,
        userTimeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      }
      // Build request params
      let rparams = {headers: {
        'R-Settings': JSON.stringify(settings)
        // 'localzone': Intl.DateTimeFormat().resolvedOptions().timeZone
      }}
      axios.get(url, rparams).then(resp => {
        this.campaign = params.campaign
        this.report.meta = params
        this.report.data = resp.data
      }).catch(err => {
         this.$store.dispatch('raiseError', err.response.data.message)
      })
    }
  }

}
</script>
