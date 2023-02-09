import moment from '@baserow/modules/core/moment'
import {
  getDateMomentFormat,
  getTimeMomentFormat,
  getTimezone,
} from '@baserow/modules/database/utils/date'

export default {
  methods: {
    getDate(field, value) {
      if (value === null || value === undefined) {
        return ''
      }
      const existing = moment.utc(value || undefined)
      const dateFormat = getDateMomentFormat(field.date_format)
      return existing.format(dateFormat)
    },
    getTime(field, value) {
      if (value === null || value === undefined) {
        return ''
      }

      const existing = moment(value || undefined).tz(getTimezone(field))
      const timeFormat = getTimeMomentFormat(field.date_time_format)
      return existing.format(timeFormat)
    },
    showTimezone(field, value) {
      if (value === null || value === undefined) {
        return ''
      }

      const existing = moment(value || undefined).tz(getTimezone(field))
      return existing.format('z')
    },
  },
}
