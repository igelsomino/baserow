import moment from '@baserow/modules/core/moment'
import {
  getDateMomentFormat,
  getTimeMomentFormat,
  getCellTimezoneAbbr,
  localizeMoment,
} from '@baserow/modules/database/utils/date'

export default {
  methods: {
    getDate(field, value) {
      if (value === null || value === undefined) {
        return ''
      }
      const existing = localizeMoment(
        field,
        moment(value),
        undefined,
        !field.date_include_time
      )
      const dateFormat = getDateMomentFormat(field.date_format)
      return existing.format(dateFormat)
    },
    getTime(field, value) {
      if (value === null || value === undefined) {
        return ''
      }

      const existing = localizeMoment(field, moment(value))
      const timeFormat = getTimeMomentFormat(field.date_time_format)
      return existing.format(timeFormat)
    },
    getCellTimezoneAbbr(field, value) {
      return getCellTimezoneAbbr(field, value)
    },
  },
}
