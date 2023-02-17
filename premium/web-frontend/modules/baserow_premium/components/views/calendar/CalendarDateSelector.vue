<template>
  <div class="calendar-date-selector">
    <span @click="selectPrevious">﹤</span>
    <span @click="selectNext">﹥</span>
    <span @click="selectCurrent">Today</span>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'

export default {
  name: 'CalendarDateSelector',
  props: {
    currentDate: {
      type: String,
      required: true,
    },
    selectedDate: {
      type: Object,
      required: true,
    },
  },
  methods: {
    selectPrevious() {
      const newSelectedDate = moment(this.selectedDate).subtract(1, 'month')
      this.$emit('date-selected', newSelectedDate)
    },
    selectCurrent() {
      const newSelectedDate = moment(this.currentDate)
      this.$emit('date-selected', newSelectedDate)
    },
    selectNext() {
      const newSelectedDate = moment(this.selectedDate).add(1, 'month')
      this.$emit('date-selected', newSelectedDate)
    },
  },
}
</script>
