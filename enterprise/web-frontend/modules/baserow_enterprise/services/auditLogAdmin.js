import baseService from '@baserow/modules/core/crudTable/baseService'

export default (client) => {
  return Object.assign(baseService(client, '/admin/audit-log/'), {
    fetchUsers(page, search) {
      const usersUrl = '/admin/audit-log/users/'
      const userPaginatedService = baseService(client, usersUrl)
      return userPaginatedService.fetch(usersUrl, page, '', [], [])
    },
    fetchGroups(page, search) {
      const groupsUrl = '/admin/audit-log/groups/'
      const groupPaginatedService = baseService(client, groupsUrl)
      return groupPaginatedService.fetch(groupsUrl, page, search, [], [])
    },
    fetchActionTypes(page, search) {
      const actionTypesUrl = '/admin/audit-log/action-types/'
      const actionTypePaginatedService = baseService(client, actionTypesUrl)
      return actionTypePaginatedService.fetch(actionTypesUrl, page, search, [], [])
    },
  })
}