import _ from 'lodash'

/**
 * Serializes a row to make sure that the values are according to what the API expects.
 *
 * If a field doesn't have a value it will be assigned the empty value of the field
 * type.
 */
export function prepareRowForRequest(row, fields, registry) {
  return fields.reduce((preparedRow, field) => {
    const name = `field_${field.id}`
    const fieldType = registry.get('field', field._.type.type)

    if (fieldType.isReadOnly) {
      return preparedRow
    }

    preparedRow[name] = Object.prototype.hasOwnProperty.call(row, name)
      ? (preparedRow[name] = fieldType.prepareValueForUpdate(field, row[name]))
      : fieldType.getEmptyValue(field)

    return preparedRow
  }, {})
}

/**
 * Returns the readonly values that have been updated. If no values have been
 * updated then null is returned.
 * @param {*} fields
 * @param {*} row
 * @param {*} updatedValues
 * @returns an object with the readonly values that have been updated or null.
 */
export function getReadOnlyValuesToUpdate(fields, row, updatedValues) {
  const readonlyFieldIds = fields
    .filter((field) => field.read_only)
    .map((field) => `field_${field.id}`)

  const readOnlyValuesChanged = Object.fromEntries(
    Object.entries(updatedValues).filter(
      ([fieldId, value]) =>
        readonlyFieldIds.includes(fieldId) && !_.isEqual(row[fieldId], value)
    )
  )
  return _.isEmpty(readOnlyValuesChanged) ? null : readOnlyValuesChanged
}
