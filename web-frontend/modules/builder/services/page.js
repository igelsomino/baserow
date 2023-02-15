export default (client) => {
  return {
    create(builderId, name) {
      return client.post(`builder/${builderId}/pages/`, { name })
    },
    update(builderId, pageId, values) {
      return client.patch(`builder/${builderId}/pages/${pageId}/`, values)
    },
  }
}
