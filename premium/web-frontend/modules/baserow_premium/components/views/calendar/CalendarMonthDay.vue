<template>
  <li
    class="calendar-month-day"
    :class="{
      'calendar-month-day--not-current': !isCurrentMonth,
      'calendar-month-day--today': isToday,
      'calendar-month-day--weekend': isWeekend,
    }"
  >
    <div class="calendar-month-day__date">
      <span>{{ label }}</span>
    </div>
  </li>
</template>

<script>
import moment from '@baserow/modules/core/moment'

export default {
  name: 'CalendarMonthDay',
  props: {
    day: {
      type: Object,
      required: true,
    },
    isCurrentMonth: {
      type: Boolean,
      default: false,
    },
    isToday: {
      type: Boolean,
      default: false,
    },
    isWeekend: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    label() {
      return moment(this.day.date).format('D')
    },
  },
}
</script>
