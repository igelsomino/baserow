export default (client) => {
  return {
    fetchRows({
      calendarId,
      limit = 100,
      offset = null,
      includeFieldOptions = false,
    }) {
      const include = []
      const params = new URLSearchParams()
      params.append('limit', limit)

      if (offset !== null) {
        params.append('offset', offset)
      }

      if (includeFieldOptions) {
        include.push('field_options')
      }

      if (include.length > 0) {
        params.append('include', include.join(','))
      }

      const config = { params }

      return client.get(`/database/views/calendar/${calendarId}/`, config)
    },
  }
}
