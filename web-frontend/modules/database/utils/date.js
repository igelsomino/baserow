import moment from 'moment-timezone'

const dateMapping = {
  EU: {
    momentFormat: 'DD/MM/YYYY',
    humanFormat: 'dd/mm/yyyy',
  },
  US: {
    momentFormat: 'MM/DD/YYYY',
    humanFormat: 'mm/dd/yyyy',
  },
  ISO: {
    momentFormat: 'YYYY-MM-DD',
    humanFormat: 'yyyy-mm-dd',
  },
}

const timeMapping = {
  12: {
    momentFormat: 'hh:mm A',
    humanFormat: 'hh:mm AM',
  },
  24: {
    momentFormat: 'HH:mm',
    humanFormat: 'hh:mm',
  },
}

export const getDateMomentFormat = (type) => {
  if (!Object.prototype.hasOwnProperty.call(dateMapping, type)) {
    throw new Error(`${type} wasn't found in the date mapping.`)
  }
  return dateMapping[type].momentFormat
}

export const getTimeMomentFormat = (type) => {
  if (!Object.prototype.hasOwnProperty.call(timeMapping, type)) {
    throw new Error(`${type} wasn't found in the time mapping.`)
  }
  return timeMapping[type].momentFormat
}

export const getDateHumanReadableFormat = (type) => {
  if (!Object.prototype.hasOwnProperty.call(dateMapping, type)) {
    throw new Error(`${type} wasn't found in the date mapping.`)
  }
  return dateMapping[type].humanFormat
}

export const getTimeHumanReadableFormat = (type) => {
  if (!Object.prototype.hasOwnProperty.call(timeMapping, type)) {
    throw new Error(`${type} wasn't found in the time mapping.`)
  }
  return timeMapping[type].humanFormat
}

export const getFieldTimezone = (field) => {
  if (!field.date_include_time) return 'UTC'
  return field.date_force_timezone || moment.tz.guess()
}

export const getCellTimezoneAbbr = (field, value) => {
  if (value === null || value === undefined) return ''
  return moment(value).tz(getFieldTimezone(field)).format('z')
}

export const localizeMoment = (
  field,
  value,
  format = undefined,
  replace = false
) => {
  const timezone = getFieldTimezone(field)
  return moment(value, format).tz(timezone, replace)
}
