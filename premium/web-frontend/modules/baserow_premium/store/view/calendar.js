import _ from 'lodash'
import moment from '@baserow/modules/core/moment'
import { clone } from '@baserow/modules/core/utils/object'
import ViewService from '@baserow/modules/database/services/view'
import CalendarService from '@baserow_premium/services/views/calendar'
import {
  getRowSortFunction,
  matchSearchFilters,
} from '@baserow/modules/database/utils/view'
import RowService from '@baserow/modules/database/services/row'

export function populateRow(row) {
  row._ = {}
  return row
}

export function populateDateStack(stack) {
  Object.assign(stack, {
    loading: false,
  })
  stack.results.forEach((row) => {
    populateRow(row)
  })
  return stack
}

export const state = () => ({
  // The calendar view id that is being displayed
  lastCalendarId: null,
  // The chosen date field that the 
  // items will be organized by in the view
  dateFieldId: null,
  fieldOptions: {},
  // dateStack organizes rows by dates (2023-02-21)
  // based on the date field with dateFieldId
  dateStacks: {},
  // How many items per date are fetched
  bufferRequestSize: 10,
  // Determines currently selected time period
  // based on a specific date. For example, if selectedDate
  // is today, the calendar view will be showing the 
  // current month surrounding it.
  // It is an instance of moment lib
  selectedDate: null,
})

export const mutations = {
  RESET(state) {
    state.dateFieldId = null
    state.fieldOptions = {}
  },
  SET_LAST_CALENDAR_ID(state, calendarId) {
    state.lastCalendarId = calendarId
  },
  SET_DATE_FIELD_ID(state, dateFieldId) {
    state.dateFieldId = dateFieldId
  },
  SET_SELECTED_DATE(state, selectedDate) {
    state.selectedDate = selectedDate
  },
  REPLACE_ALL_DATE_STACKS(state, stacks) {
    state.dateStacks = stacks
  },
  ADD_ROWS_TO_STACK(state, { date, count, rows }) {
    if (count) {
      state.dateStacks[date].count = count
    }
    state.dateStacks[date].results.push(...rows)
  },
  REPLACE_ALL_FIELD_OPTIONS(state, fieldOptions) {
    state.fieldOptions = fieldOptions
  },
  UPDATE_ALL_FIELD_OPTIONS(state, fieldOptions) {
    state.fieldOptions = _.merge({}, state.fieldOptions, fieldOptions)
  },
  UPDATE_FIELD_OPTIONS_OF_FIELD(state, { fieldId, values }) {
    if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
      Object.assign(state.fieldOptions[fieldId], values)
    } else {
      state.fieldOptions = Object.assign({}, state.fieldOptions, {
        [fieldId]: values,
      })
    }
  },
  DELETE_FIELD_OPTIONS(state, fieldId) {
    if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
      delete state.fieldOptions[fieldId]
    }
  },
  ADD_FIELD_TO_ALL_ROWS(state, { field, value }) {
    // TODO:
    // const name = `field_${field.id}`
    // Object.keys(state.stacks).forEach((stack) => {
    //   // We have to replace all the rows by using the map function to make it
    //   // reactive and update immediately. If we don't do this, the value in the
    //   // field components of the grid and modal don't always have the correct value
    //   // binding.
    //   state.stacks[stack].results = state.stacks[stack].results.map((row) => {
    //     if (row !== null && !Object.prototype.hasOwnProperty.call(row, name)) {
    //       row[`field_${field.id}`] = value
    //       return { ...row }
    //     }
    //     return row
    //   })
    // })
  },
}

/**
 * Given a datetime returns from and to timestamps for monthly calendar
 * view surrounding the provided datetime, including days before and after the
 * datetime's month.
 * @param moment dateTime 
 */
function getMonthlyTimestamps(dateTime) {
    const firstDayOfMonth = moment(`${dateTime.year()}-${dateTime.month() + 1}-01`)
    const firstDayOfMonthWeekday = firstDayOfMonth.isoWeekday()
    const firstDayPreviousMonth = firstDayOfMonth.subtract(1, 'month')
    const visibleNumberOfDaysFromPreviousMonth = firstDayOfMonthWeekday
        ? firstDayOfMonthWeekday - 1
        : 6
    const previousMonthLastMondayDayOfMonth = firstDayOfMonth
          .subtract(visibleNumberOfDaysFromPreviousMonth, 'day')
          .date()
    const fromTimestamp = moment(
      `${firstDayPreviousMonth.year()}-${firstDayPreviousMonth.month() + 1}-${
        previousMonthLastMondayDayOfMonth
      }`
    )
    const daysInMonth = moment(dateTime).daysInMonth()
    const lastDayOfMonth = moment(`${dateTime.year()}-${dateTime.month() + 1}-${daysInMonth}`)    
    const lastDayOfMonthWeekday = lastDayOfMonth.isoWeekday()
    const firstDayNextMonth = moment(
      `${dateTime.year()}-${dateTime.month() + 1}-01`
    ).add(1, 'month')
    const visibleNumberOfDaysFromNextMonth = lastDayOfMonthWeekday
      ? 7 - lastDayOfMonthWeekday
      : lastDayOfMonthWeekday
    const toTimestamp = moment(
      `${firstDayNextMonth.year()}-${firstDayNextMonth.month() + 1}-${visibleNumberOfDaysFromNextMonth}`
    )
    return { fromTimestamp, toTimestamp }
}

export const actions = {
  /**
   * This method is typically called when the view loads, but when it doesn't
   * yet have a date field. This will make sure that the old state
   * of another calendar view will be reset.
   */
  reset({ commit }) {
    commit('RESET')
  },
  /**
   * Fetches an initial set of rows and adds that data to the store.
   */
  async fetchInitial(
    { dispatch, commit, getters, rootGetters },
    { calendarId, dateFieldId, includeFieldOptions = true }
  ) {
    const now = moment()
    commit('SET_SELECTED_DATE', now)
    // const dateField = rootGetters['field/get'](dateFieldId)
    const { fromTimestamp, toTimestamp } = getMonthlyTimestamps(now)
    const { data } = await CalendarService(this.$client).fetchRows({
      calendarId,
      limit: getters.getBufferRequestSize,
      offset: 0,
      includeFieldOptions,
      fromTimestamp: fromTimestamp.format("YYYY-MM-DD hh:mm"),
      toTimestamp: toTimestamp.format("YYYY-MM-DD hh:mm"),
    })
    Object.keys(data.rows).forEach((key) => {
      populateDateStack(data.rows[key])
    })
    commit('REPLACE_ALL_DATE_STACKS', data.rows)
    commit('SET_LAST_CALENDAR_ID', calendarId)
    commit('SET_DATE_FIELD_ID', dateFieldId)
    if (includeFieldOptions) {
      commit('REPLACE_ALL_FIELD_OPTIONS', data.field_options)
    }
  },
  /**
   * Fetches a set of rows based on the provided datetime.
   */
  async fetchMonthly(
    { dispatch, commit, getters, rootGetters },
    { dateTime }
  ) {
    commit('SET_SELECTED_DATE', dateTime)
    const { fromTimestamp, toTimestamp } = getMonthlyTimestamps(dateTime)
    console.log({ dateTime, fromTimestamp, toTimestamp})
    const { data } = await CalendarService(this.$client).fetchRows({
      calendarId: getters.getLastCalendarId,
      limit: getters.getBufferRequestSize,
      offset: 0,
      includeFieldOptions: false,
      fromTimestamp: fromTimestamp.format("YYYY-MM-DD hh:mm"),
      toTimestamp: toTimestamp.format("YYYY-MM-DD hh:mm"),
    })
    Object.keys(data.rows).forEach((key) => {
      populateDateStack(data.rows[key])
    })
    commit('REPLACE_ALL_DATE_STACKS', data.rows)
  },
  /**
   * This action is called when the users scrolls to the end of the stack. Because
   * we don't fetch all the rows, the next set will be fetched when the user reaches
   * the end. TODO:
   */
  // async fetchMore(
  //   { dispatch, commit, getters, rootGetters },
  //   { date }
  // ) {
  //   const stack = getters.getDateStack(date)
  //   const { data } = await CalendarService(this.$client).fetchRows({
  //     calendarId: getters.getLastCalendarId,
  //     limit: getters.getBufferRequestSize,
  //     offset: 0,
  //     includeFieldOptions: false,
  //     // TODO: set correct datetimes
  //     fromTimestamp: '2023-02-01 00:00',
  //     toTimestamp: '2023-03-01 00:00',
  //   })
  //   const count = data.rows[date].count
  //   const rows = data.rows[date].results
  //   rows.forEach((row) => {
  //     populateRow(row)
  //   })
  //   commit('ADD_ROWS_TO_STACK', { date, count, rows })
  // },
  /**
   * Updates the field options of a given field in the store. So no API request to
   * the backend is made.
   */
  setFieldOptionsOfField({ commit }, { field, values }) {
    commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
      fieldId: field.id,
      values,
    })
  },
  /**
   * Replaces all field options with new values and also makes an API request to the
   * backend with the changed values. If the request fails the action is reverted.
   */
  async updateAllFieldOptions(
    { dispatch, getters, rootGetters },
    { newFieldOptions, oldFieldOptions, readOnly = false }
  ) {
    dispatch('forceUpdateAllFieldOptions', newFieldOptions)

    const calendarId = getters.getLastCalendarId
    if (!readOnly) {
      const updateValues = { field_options: newFieldOptions }

      try {
        await ViewService(this.$client).updateFieldOptions({
          viewId: calendarId,
          values: updateValues,
        })
      } catch (error) {
        dispatch('forceUpdateAllFieldOptions', oldFieldOptions)
        throw error
      }
    }
  },
  /**
   * Forcefully updates all field options without making a call to the backend.
   */
  forceUpdateAllFieldOptions({ commit }, fieldOptions) {
    commit('UPDATE_ALL_FIELD_OPTIONS', fieldOptions)
  },
  /**
   * Deletes the field options of the provided field id if they exist.
   */
  forceDeleteFieldOptions({ commit }, fieldId) {
    commit('DELETE_FIELD_OPTIONS', fieldId)
  },
  /**
   * Updates the order of all the available field options. The provided order parameter
   * should be an array containing the field ids in the correct order.
   */
  async updateFieldOptionsOrder(
    { commit, getters, dispatch },
    { order, readOnly = false }
  ) {
    const oldFieldOptions = clone(getters.getAllFieldOptions)
    const newFieldOptions = clone(getters.getAllFieldOptions)

    // Update the order of the field options that have not been provided in the order.
    // They will get a position that places them after the provided field ids.
    let i = 0
    Object.keys(newFieldOptions).forEach((fieldId) => {
      if (!order.includes(parseInt(fieldId))) {
        newFieldOptions[fieldId].order = order.length + i
        i++
      }
    })

    // Update create the field options and set the correct order value.
    order.forEach((fieldId, index) => {
      const id = fieldId.toString()
      if (Object.prototype.hasOwnProperty.call(newFieldOptions, id)) {
        newFieldOptions[fieldId.toString()].order = index
      }
    })

    return await dispatch('updateAllFieldOptions', {
      oldFieldOptions,
      newFieldOptions,
      readOnly,
    })
  },
  /**
   * Updates the field options of a specific field.
   */
  async updateFieldOptionsOfField(
    { commit, getters, rootGetters },
    { view, field, values, readOnly = false }
  ) {
    commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
      fieldId: field.id,
      values,
    })

    if (!readOnly) {
      const calendarId = getters.getLastCalendarId
      const oldValues = clone(getters.getAllFieldOptions[field.id])
      const updateValues = { field_options: {} }
      updateValues.field_options[field.id] = values

      try {
        await ViewService(this.$client).updateFieldOptions({
          viewId: calendarId,
          values: updateValues,
        })
      } catch (error) {
        commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
          fieldId: field.id,
          values: oldValues,
        })
        throw error
      }
    }
  },
  /**
   * Can be called when a new row has been created. This action will make sure that
   * the state is updated accordingly. If the newly created position is within the
   * current buffer (`stack.results`), then it will be added there, otherwise, just
   * the count is increased.
   *
   * @param values  The values of the newly created row.
   * @param row     Can be provided when the row already existed within the state.
   *                In that case, the `_` data will be preserved. Can be useful when
   *                a row has been updated while being dragged. TODO:
   */
  async createdNewRow(
    { dispatch, commit, getters, rootGetters },
    { view, values, fields }
  ) {
    const row = clone(values)
    populateRow(row)

    const matchesFilters = await dispatch('rowMatchesFilters', {
      view,
      row,
      fields,
    })
    if (!matchesFilters) {
      return
    }

    const singleSelectFieldId = getters.getSingleSelectFieldId
    const option = row[`field_${singleSelectFieldId}`]
    const stackId = option !== null ? option.id : 'null'
    const stack = getters.getStack(stackId)

    const sortedRows = clone(stack.results)
    sortedRows.push(row)
    sortedRows.sort(getRowSortFunction(this.$registry, [], fields))
    const index = sortedRows.findIndex((r) => r.id === row.id)
    const isLast = index === sortedRows.length - 1

    // Because we don't fetch all the rows from the backend, we can't know for sure
    // whether or not the row is being added at the right position. Therefore, if
    // it's last, we just not add it to the store and wait for the user to fetch the
    // next page.
    if (!isLast || stack.results.length === stack.count) {
      commit('CREATE_ROW', { row, stackId, index })
    }

    // We always need to increase the count whether row has been added to the store
    // or not because the count is for all the rows and not just the ones in the store.
    commit('INCREASE_COUNT', { stackId })
  },
  /**
   * Can be called when a row in the table has been deleted. This action will make
   * sure that the state is updated accordingly. TODO:
   */
  async deletedExistingRow(
    { dispatch, commit, getters },
    { view, row, fields }
  ) {
    row = clone(row)
    populateRow(row)

    const matchesFilters = await dispatch('rowMatchesFilters', {
      view,
      row,
      fields,
    })
    if (!matchesFilters) {
      return
    }

    const singleSelectFieldId = getters.getSingleSelectFieldId
    const option = row[`field_${singleSelectFieldId}`]
    const stackId = option !== null ? option.id : 'null'
    const current = getters.findStackIdAndIndex(row.id)

    if (current !== undefined) {
      const currentStackId = current[0]
      const currentIndex = current[1]
      const currentRow = current[2]
      commit('DELETE_ROW', { stackId: currentStackId, index: currentIndex })
      commit('DECREASE_COUNT', { stackId: currentStackId })
      return currentRow
    } else {
      commit('DECREASE_COUNT', { stackId })
    }

    return null
  },
  /**
   * Check if the provided row matches the provided view filters. TODO:
   */
  rowMatchesFilters(context, { view, fields, row, overrides = {} }) {
    const values = JSON.parse(JSON.stringify(row))
    Object.assign(values, overrides)

    // The value is always valid if the filters are disabled.
    return view.filters_disabled
      ? true
      : matchSearchFilters(
          this.$registry,
          view.filter_type,
          view.filters,
          fields,
          values
        )
  },

  /**
   * Moves the provided row to the target stack at the provided index. TODO:
   *
   * @param row
   * @param targetStackId
   * @param targetIndex
   */
  forceMoveRowTo({ commit, getters }, { row, targetStackId, targetIndex }) {
    const current = getters.findStackIdAndIndex(row.id)

    if (current !== undefined) {
      const currentStackId = current[0]
      const currentIndex = current[1]

      if (currentStackId !== targetStackId || currentIndex !== targetIndex) {
        commit('MOVE_ROW', {
          currentStackId,
          currentIndex,
          targetStackId,
          targetIndex,
        })
        return true
      }
    }
    return false
  },
  /**
   * Moves the provided existing row before or after the provided target row. TODO:
   *
   * @param row           The row object that must be moved.
   * @param targetRow     Will be placed before or after the provided row.
   * @param targetBefore  Indicates whether the row must be moved before or after
   *                      the target row.
   */
  forceMoveRowBefore({ dispatch, getters }, { row, targetRow, targetBefore }) {
    const target = getters.findStackIdAndIndex(targetRow.id)

    if (target !== undefined) {
      const targetStackId = target[0]
      const targetIndex = target[1] + (targetBefore ? 0 : 1)

      return dispatch('forceMoveRowTo', { row, targetStackId, targetIndex })
    }
    return false
  },
  /**
   * Updates the value of a row and make the changes to the store accordingly. TODO:
   */
  async updateRowValue(
    { commit, dispatch },
    { view, table, row, field, fields, value, oldValue }
  ) {
    const fieldType = this.$registry.get('field', field._.type.type)
    const newValues = {}
    const newValuesForUpdate = {}
    const oldValues = {}
    const fieldName = `field_${field.id}`
    newValues[fieldName] = value
    newValuesForUpdate[fieldName] = fieldType.prepareValueForUpdate(
      field,
      value
    )
    oldValues[fieldName] = oldValue

    fields.forEach((fieldToCall) => {
      const fieldType = this.$registry.get('field', fieldToCall._.type.type)
      const fieldToCallName = `field_${fieldToCall.id}`
      const currentFieldValue = row[fieldToCallName]
      const optimisticFieldValue = fieldType.onRowChange(
        row,
        fieldToCall,
        currentFieldValue
      )

      if (currentFieldValue !== optimisticFieldValue) {
        newValues[fieldToCallName] = optimisticFieldValue
        oldValues[fieldToCallName] = currentFieldValue
      }
    })

    await dispatch('updatedExistingRow', {
      view,
      row,
      values: newValues,
      fields,
    })

    try {
      const { data } = await RowService(this.$client).update(
        table.id,
        row.id,
        newValuesForUpdate
      )
      commit('UPDATE_ROW', { row, values: data })
    } catch (error) {
      dispatch('updatedExistingRow', {
        view,
        row,
        values: oldValues,
        fields,
      })
      throw error
    }
  },
  /**
   * Adds a field with a provided value to the rows in the store. This will for
   * example be called when a new field has been created.
   */
  addField({ commit }, { field, value = null }) {
    commit('ADD_FIELD_TO_ALL_ROWS', { field, value })
  },
}

export const getters = {
  getLastCalendarId(state) {
    return state.lastCalendarId
  },
  getDateFieldId(state) {
    return state.dateFieldId
  },
  getAllFieldOptions(state) {
    return state.fieldOptions
  },
  getDateStack: (state) => (date) => {
    return state.dateStacks[date] ? state.dateStacks[date] : {'results': []}
  },
  getBufferRequestSize(state) {
    return state.bufferRequestSize
  },
  getSelectedDate(state) {
    return state.selectedDate
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
