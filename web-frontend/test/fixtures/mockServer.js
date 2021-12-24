import { createApplication } from '@baserow/test/fixtures/applications'
import { createGroup } from '@baserow/test/fixtures/groups'
import {
  createGridView,
  createPublicGridView,
} from '@baserow/test/fixtures/view'
import { createFields } from '@baserow/test/fixtures/fields'
import {
  createPublicGridViewRows,
  createRows,
} from '@baserow/test/fixtures/grid'

/**
 * MockServer is responsible for being the single place where we mock out calls to the
 * baserow server API in tests. This way when an API change is made we should only
 * need to make one change in this class to reflect the change in the tests.
 */
export class MockServer {
  constructor(mock, store) {
    this.mock = mock
    this.store = store
  }

  async createAppAndGroup(table) {
    const group = createGroup(this.mock, {})
    const application = createApplication(this.mock, {
      groupId: group.id,
      tables: [table],
    })
    await this.store.dispatch('group/fetchAll')
    await this.store.dispatch('application/fetchAll')
    return { application, group }
  }

  createTable() {
    return { id: 1, name: 'Test Table 1' }
  }

  createGridView(application, table, { filters = [], sortings = [] }) {
    return createGridView(this.mock, application, table, {
      filters,
      sortings,
    })
  }

  createPublicGridView(viewSlug, { name, fields = [], sortings = [] }) {
    return createPublicGridView(this.mock, viewSlug, { name, fields, sortings })
  }

  createPublicGridViewRows(viewSlug, fields, rows) {
    return createPublicGridViewRows(this.mock, viewSlug, fields, rows)
  }

  createFields(application, table, fields) {
    return createFields(this.mock, application, table, fields)
  }

  createRows(gridView, fields, rows) {
    return createRows(this.mock, gridView, fields, rows)
  }

  nextSearchForTermWillReturn(searchTerm, gridView, results) {
    this.mock
      .onGet(`/database/views/grid/${gridView.id}/`, {
        params: { count: true, search: searchTerm },
      })
      .reply(200, {
        count: results.length,
      })

    this.mock
      .onGet(`/database/views/grid/${gridView.id}/`, {
        params: {
          limit: 120,
          offset: 0,
          search: searchTerm,
          include: 'row_metadata',
        },
      })
      .reply(200, {
        count: results.length,
        next: null,
        previous: null,
        results,
      })
  }

  creatingRowInTableReturns(table, result) {
    this.mock.onPost(`/database/rows/table/${table.id}/`).reply(200, result)
  }

  updateViewFilter(filterId, newValue) {
    this.mock
      .onPatch(`/database/views/filter/${filterId}/`, { value: newValue })
      .reply(200)
  }

  resetMockEndpoints() {
    this.mock.reset()
  }
}
