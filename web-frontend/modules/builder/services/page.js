export default (client) => {
  return {
    create(builderId, name) {
      return client.post(`builder/pages/builder/${builderId}/`, { name })
    },
  }
}
