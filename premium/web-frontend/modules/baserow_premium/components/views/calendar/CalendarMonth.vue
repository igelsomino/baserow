<template>
  <div class="calendar-month">
    <div class="calendar-month__header">
      <CalendarDateIndicator
        :selected-date="selectedDate"
        class="calendar-month__header-selected-month"
      />
      <CalendarDateSelector
        :selected-date="selectedDate"
        :current-date="today"
        @date-selected="selectDate"
      />
    </div>
    <CalendarWeekdays />
    <ol class="calendar-month__days-grid">
      <CalendarMonthDay 
        v-for="day in days"
        :key="day.date"
        :day="day"
        :is-today="day.date === today"
        :is-current-month="day.isCurrentMonth"
        :is-weekend="isWeekendDay(day.date)">
      </CalendarMonthDay>
    </ol>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'
import CalendarDateIndicator from '@baserow_premium/components/views/calendar/CalendarDateIndicator'
import CalendarDateSelector from '@baserow_premium/components/views/calendar/CalendarDateSelector'
import CalendarMonthDay from '@baserow_premium/components/views/calendar/CalendarMonthDay'
import CalendarWeekdays from '@baserow_premium/components/views/calendar/CalendarWeekdays'

export default {
  name: 'CalendarMonth',
  components: {
    CalendarDateIndicator,
    CalendarDateSelector,
    CalendarMonthDay,
    CalendarWeekdays,
  },
  data() {
    return {
      selectedDate: moment(),
      today: moment().format('YYYY-MM-DD'),
    }
  },
  computed: {
    numberOfDaysInMonth() {
      return moment(this.selectedDate).daysInMonth()
    },
    weekNumber() {
      return moment(this.selectedDate).isoWeek()
    },
    currentMonthDays() {
      return [...Array(this.numberOfDaysInMonth)].map((day, index) => {
        return {
          date: moment(`${this.selectedDate.year}-${this.selectedDate.month}-${index + 1}`).format("YYYY-MM-DD"),
          isCurrentMonth: true,
        }
      })
    },
    days() {
      const t = this.currentMonthDays
      console.log(t)
      return t
      // return [
      //   { date: "2023-01-29", isCurrentMonth: false },
      //   { date: "2023-01-30", isCurrentMonth: false },
      //   { date: "2023-02-01", isCurrentMonth: true },
      //   { date: "2023-02-02", isCurrentMonth: true },
      //   { date: "2023-02-03", isCurrentMonth: true },
      //   { date: "2023-02-04", isCurrentMonth: true },
      //   { date: "2023-02-05", isCurrentMonth: true },
      //   { date: "2023-02-06", isCurrentMonth: true },
      //   { date: "2023-02-07", isCurrentMonth: true },
      //   { date: "2023-02-08", isCurrentMonth: true },
      //   { date: "2023-02-09", isCurrentMonth: true },
      //   { date: "2023-02-10", isCurrentMonth: true },
      //   { date: "2023-02-11", isCurrentMonth: true },
      //   { date: "2023-02-12", isCurrentMonth: true },
      //   { date: "2023-02-13", isCurrentMonth: true },
      //   { date: "2023-02-14", isCurrentMonth: true },
      //   { date: "2023-02-15", isCurrentMonth: true },
      //   { date: "2020-07-16", isCurrentMonth: true },
      //   { date: "2023-02-17", isCurrentMonth: true },
      //   { date: "2020-07-18", isCurrentMonth: true },
      //   { date: "2020-07-19", isCurrentMonth: true },
      //   { date: "2020-07-20", isCurrentMonth: true },
      //   { date: "2020-07-21", isCurrentMonth: true },
      //   { date: "2020-07-22", isCurrentMonth: true },
      //   { date: "2020-07-23", isCurrentMonth: true },
      //   { date: "2020-07-24", isCurrentMonth: true },
      //   { date: "2020-07-25", isCurrentMonth: true },
      //   { date: "2020-07-26", isCurrentMonth: true },
      //   { date: "2020-07-27", isCurrentMonth: true },
      //   { date: "2020-07-28", isCurrentMonth: true },
      //   { date: "2020-07-29", isCurrentMonth: true },
      //   { date: "2020-07-30", isCurrentMonth: true },
      //   { date: "2020-07-31", isCurrentMonth: true },
      //   { date: "2020-08-01", isCurrentMonth: false },
      //   { date: "2020-08-02", isCurrentMonth: false }
      // ]
    },
  },
  methods: {
    selectDate(newSelectedDate) {
      this.selectedDate = newSelectedDate
    },
    getWeekDay(date) {
      return moment(date).isoWeekday()
    },
    isWeekendDay(date) {
      const dayOfWeek = moment(date).isoWeekday()
      const isWeekend = (dayOfWeek === 6) || (dayOfWeek  === 7)
      return isWeekend
    }
  },
}
</script>
