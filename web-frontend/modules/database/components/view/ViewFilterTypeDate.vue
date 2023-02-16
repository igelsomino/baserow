<template>
  <div class="filters__value-date-timezone">
    <div>
      <input
        ref="date"
        v-model="dateString"
        type="text"
        class="input filters__value-input"
        :disabled="disabled"
        :class="{ 'input--error': $v.copy.$error }"
        :placeholder="getDatePlaceholder(field)"
        @focus="$refs.dateContext.toggle($refs.date, 'bottom', 'left', 0)"
        @blur="$refs.dateContext.hide()"
        @input="
          ;[
            setCopyFromDateString(dateString, 'dateString'),
            combinedDelayedUpdate(copy),
          ]
        "
        @keydown.enter="combinedDelayedUpdate(copy, true)"
      />
      <Context
        ref="dateContext"
        :hide-on-click-outside="false"
        class="datepicker-context"
      >
        <client-only>
          <date-picker
            :inline="true"
            :monday-first="true"
            :value="dateObject"
            :language="datePickerLang[$i18n.locale]"
            class="datepicker"
            @input="
              ;[
                setCopy($event, 'dateObject'),
                combinedDelayedUpdate(copy, true),
              ]
            "
          ></date-picker>
        </client-only>
      </Context>
    </div>
    <div class="filters__value-timezone">{{ timezoneShortName }}</div>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'
import {
  getDateMomentFormat,
  getDateHumanReadableFormat,
} from '@baserow/modules/database/utils/date'
import filterTypeInput from '@baserow/modules/database/mixins/filterTypeInput'
import { en, fr } from 'vuejs-datepicker/dist/locale'

export default {
  name: 'ViewFilterTypeDate',
  mixins: [filterTypeInput],
  data() {
    return {
      copy: '',
      timezoneValue: null,
      dateString: '',
      dateObject: '',
      datePickerLang: {
        en,
        fr,
      },
    }
  },
  computed: {
    timezoneShortName() {
      if (this.timezoneValue === null) {
        this.getTimezone()
      }
      return moment().tz(this.timezoneValue).format('z')
    },
  },
  watch: {
    'filter.value'(value) {
      this.setCopy(value)
      this.getTimezone()
    },
    'field.date_include_time'() {
      this.timezoneValue = null
      this.getTimezone()
    },
  },
  created() {
    const [timezone, dateValue] = this.splitCombinedValue(this.filter.value)
    this.timezoneValue = timezone
    this.setCopy(dateValue)
  },
  mounted() {
    this.$v.$touch()
  },
  methods: {
    getTimezone() {
      const field = this.field
      if (!field?.date_include_time) {
        this.timezoneValue = 'GMT'
      } else if (this.timezoneValue === null) {
        this.timezoneValue = field.date_force_timezone || moment.tz.guess()
      }
      return this.timezoneValue
    },
    getSeparator() {
      return '?'
    },
    splitCombinedValue(value) {
      const separator = this.getSeparator()
      let timezone, dateValue
      if (!value.includes(separator) || !this.field.date_include_time) {
        dateValue = value
        timezone = this.getTimezone()
      } else {
        ;[timezone, dateValue] = value.split(separator)
      }
      return [timezone, dateValue]
    },
    setCopy(value, sender) {
      const newDate = moment(value)

      if (newDate.isValid()) {
        this.copy = newDate.format('YYYY-MM-DD')

        if (sender !== 'dateObject') {
          this.dateObject = newDate.toDate()
        }

        if (sender !== 'dateString') {
          const dateFormat = getDateMomentFormat(this.field.date_format)
          this.dateString = newDate.format(dateFormat)
        }
      }
    },
    setCopyFromDateString(value, sender) {
      if (value === '') {
        this.copy = ''
        this.getTimezone()
        return
      }

      const dateFormat = getDateMomentFormat(this.field.date_format)
      const newDate = moment(value, dateFormat)

      if (newDate.isValid()) {
        this.setCopy(newDate, sender)
      } else {
        this.copy = value
      }
    },
    prepareValue(dateValue, field) {
      const separator = this.getSeparator()
      return `${this.timezoneValue}${separator}${dateValue}`
    },
    getDatePlaceholder(field) {
      return this.$t(
        'humanDateFormat.' + getDateHumanReadableFormat(field.date_format)
      )
    },
    focus() {
      this.$refs.date.focus()
    },
    combinedDelayedUpdate(value, immediately = false) {
      const preparedValue = this.prepareValue(value)
      return this.delayedUpdate(preparedValue, immediately)
    },
  },
  validations: {
    copy: {
      date(value) {
        return value === '' || moment(value).isValid()
      },
    },
  },
}
</script>
