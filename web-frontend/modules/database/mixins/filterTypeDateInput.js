import moment from '@baserow/modules/core/moment'
import { getFieldTimezone } from '@baserow/modules/database/utils/date'
import filterTypeInput from '@baserow/modules/database/mixins/filterTypeInput'

export default {
  mixins: [filterTypeInput],
  data() {
    return {
      copy: '',
      timezoneValue: null,
    }
  },
  watch: {
    'field.date_include_time'() {
      this.timezoneValue = null
    },
  },
  created() {
    const [timezone, filterValue] = this.splitCombinedValue(this.filter.value)
    this.timezoneValue = timezone
    this.setCopy(filterValue)
  },
  methods: {
    getSeparator() {
      return '?'
    },
    getTimezone() {
      if (this.timezoneValue === null) {
        this.timezoneValue = getFieldTimezone(this.field)
      }
      return this.timezoneValue
    },
    getTimezoneAbbr() {
      return moment().tz(this.getTimezone()).format('z')
    },
    splitCombinedValue(value) {
      const separator = this.getSeparator()
      let timezone, filterValue
      if (!value.includes(separator)) {
        filterValue = value
      } else {
        ;[timezone, filterValue] = value.split(separator)
      }
      if (timezone === undefined || !this.field.date_include_time) {
        timezone = this.getTimezone()
      }
      return [timezone, filterValue || '']
    },
    setCopy(value) {
      this.copy = value
    },
    prepareValue(value, field) {
      const separator = this.getSeparator()
      return `${this.getTimezone()}${separator}${value}`
    },
    delayedUpdate(value, immediately = false) {
      const combinedValue = this.prepareValue(value, this.field)
      return this.$super(filterTypeInput).delayedUpdate(
        combinedValue,
        immediately
      )
    },
  },
}
