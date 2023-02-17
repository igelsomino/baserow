<template>
  <div class="calendar-date-indicator">{{ selectedMonth }}</div>
</template>

<script>
import { getMonthName } from '@baserow/modules/core/utils/date'

export default {
  name: 'CalendarDateIndicator',
  props: {
    selectedDate: {
      type: Object,
      required: true,
    },
  },
  computed: {
    selectedMonth() {
      return getMonthName(this.selectedDate)
    },
  },
}
</script>
