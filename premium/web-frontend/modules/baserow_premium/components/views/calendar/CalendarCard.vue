<template>
  <div class="calendar-card">{{ row[`field_${visibleFieldId}`] }}</div>
</template>

<script>
export default {
  name: 'CalendarCard',
  props: {
    row: {
      type: Object,
      required: true
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  computed: {
    visibleFieldId() {
      const options = this.$store.getters[this.storePrefix + 'view/calendar/getAllFieldOptions']
      const keys = Object.keys(options)
      for (const key of keys) {
        if (options[key].hidden === false) {
          return key
        }
      }
    },
  }
}
</script>