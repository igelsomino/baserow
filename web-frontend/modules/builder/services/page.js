export default (client) => {
  return {
    create(builderId, name) {
      return client.post(`builder/${builderId}/pages/`, { name })
    },
    update(builderId, pageId, values) {
      return client.patch(`builder/${builderId}/pages/${pageId}/`, values)
    },
    delete(builderId, pageId) {
      return client.delete(`builder/${builderId}/pages/${pageId}/`)
    },
    order(builderId, order) {
      return client.post(`/builder/${builderId}/pages/order/`, {
        page_ids: order,
      })
    },
  }
}
