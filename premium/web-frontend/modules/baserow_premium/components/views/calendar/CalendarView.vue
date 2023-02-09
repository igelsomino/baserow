<template>
  <div>
    <ChooseDateFieldModal
      ref="chooseDateFieldModal"
      :view="view"
      :table="table"
      :database="database"
    >
    </ChooseDateFieldModal>
    <button @click="showChooseDateFieldModal">click</button>
  </div>
</template>
<script>
import ChooseDateFieldModal from '@baserow_premium/components/views/calendar/ChooseDateFieldModal'

export default {
  name: 'CalendarView',
  components: {
    ChooseDateFieldModal
  },
  props: {
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  mounted() {
    // this.showChooseDateFieldModal()
  },
  methods: {
    showChooseDateFieldModal() {
      this.$refs.chooseDateFieldModal.show()
    },
  },
}
</script>
