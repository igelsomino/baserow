<template>
  <ol class="calendar-week-days">
    <li v-for="weekday in weekDays" :key="weekday">
      {{ weekday }}
    </li>
  </ol>
</template>

<script>
// TODO: translate week days
import { weekDays } from '@baserow/modules/core/utils/date'

export default {
  name: 'CalendarWeekdays',
  computed: {
    weekDays() {
      return weekDays
    },
  },
}
</script>
