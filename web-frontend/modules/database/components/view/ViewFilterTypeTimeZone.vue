<template>
  <div class="filters__value-timezone">{{ timezone }}</div>
</template>

<script>
import viewFilter from '@baserow/modules/database/mixins/viewFilter'
import moment from '@baserow/modules/core/moment'

export default {
  name: 'ViewFilterTypeTimeZone',
  mixins: [viewFilter],
  computed: {
    timezone() {
      if (!this.field?.date_include_time) {
        return 'GMT'
      }
      return moment().tz(this.filter.value).format('z')
    },
  },
}
</script>
