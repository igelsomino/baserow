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
        :date="day.date"
        :is-today="day.date === today"
        :is-current-month="day.isCurrentMonth"
        :is-weekend="isWeekendDay(day.date)"
        :store-prefix="storePrefix"
      >
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
  props: {
    storePrefix: {
      type: String,
      required: true,
    },
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
          date: moment(
            `${this.selectedDate.year()}-${this.selectedDate.month() + 1}-${
              index + 1
            }`
          ).format('YYYY-MM-DD'),
          isCurrentMonth: true,
        }
      })
    },
    previousMonthDays() {
      const firstDayOfTheMonthWeekday = this.getWeekDay(
        this.currentMonthDays[0].date
      )
      const previousMonth = moment(
        `${this.selectedDate.year()}-${this.selectedDate.month() + 1}-01`
      ).subtract(1, 'month')
      const visibleNumberOfDaysFromPreviousMonth = firstDayOfTheMonthWeekday
        ? firstDayOfTheMonthWeekday - 1
        : 6
      const previousMonthLastMondayDayOfMonth = moment(
        this.currentMonthDays[0].date
      )
        .subtract(visibleNumberOfDaysFromPreviousMonth, 'day')
        .date()
      return [...Array(visibleNumberOfDaysFromPreviousMonth)].map(
        (day, index) => {
          return {
            date: moment(
              `${previousMonth.year()}-${previousMonth.month() + 1}-${
                previousMonthLastMondayDayOfMonth + index
              }`
            ).format('YYYY-MM-DD'),
            isCurrentMonth: false,
          }
        }
      )
    },
    nextMonthDays() {
      const lastDayOfTheMonthWeekday = this.getWeekDay(
        `${this.selectedDate.year()}-${this.selectedDate.month() + 1}-${
          this.currentMonthDays.length
        }`
      )
      const nextMonth = moment(
        `${this.selectedDate.year()}-${this.selectedDate.month() + 1}-01`
      ).add(1, 'month')
      const visibleNumberOfDaysFromNextMonth = lastDayOfTheMonthWeekday
        ? 7 - lastDayOfTheMonthWeekday
        : lastDayOfTheMonthWeekday
      return [...Array(visibleNumberOfDaysFromNextMonth)].map((day, index) => {
        return {
          date: moment(
            `${nextMonth.year()}-${nextMonth.month() + 1}-${index + 1}`
          ).format('YYYY-MM-DD'),
          isCurrentMonth: false,
        }
      })
    },
    days() {
      return [
        ...this.previousMonthDays,
        ...this.currentMonthDays,
        ...this.nextMonthDays,
      ]
    },
  },
  methods: {
    selectDate(newSelectedDate) {
      this.selectedDate = newSelectedDate
      this.$store.dispatch(this.storePrefix + 'view/calendar/fetchMonthly', {
        dateTime: newSelectedDate
      })
    },
    getWeekDay(date) {
      return moment(date).isoWeekday()
    },
    isWeekendDay(date) {
      const dayOfWeek = moment(date).isoWeekday()
      const isWeekend = dayOfWeek === 6 || dayOfWeek === 7
      return isWeekend
    },
  },
}
</script>
