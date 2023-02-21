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
    <CalendarCard
      v-for="row in rows"
      :key="row.id"
      :row="row"
      :store-prefix="storePrefix"
    >
    </CalendarCard>
  </li>
</template>

<script>
import moment from '@baserow/modules/core/moment'
import CalendarCard from '@baserow_premium/components/views/calendar/CalendarCard'

export default {
  name: 'CalendarMonthDay',
  components: {
    CalendarCard,
  },
  props: {
    day: {
      type: Object,
      required: true,
    },
    date: {
      type: String,
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
    storePrefix: {
      type: String,
      required: true,
    },
  },
  computed: {
    label() {
      return moment(this.day.date).format('D')
    },
    rows() {
      const dayStack = this.$store.getters[
        this.storePrefix + 'view/calendar/getDateStack'
      ](this.date)
      return dayStack.results
    },
  },
}
</script>
