<template>
  <div>
    <SelectDateFieldModal
      ref="selectDateFieldModal"
      :view="view"
      :table="table"
      :database="database"
    >
    </SelectDateFieldModal>
    <CalendarMonth></CalendarMonth>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import SelectDateFieldModal from '@baserow_premium/components/views/calendar/SelectDateFieldModal'
import CalendarMonth from '@baserow_premium/components/views/calendar/CalendarMonth'

export default {
  name: 'CalendarView',
  components: {
    SelectDateFieldModal,
    CalendarMonth,
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
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        dateFieldId:
          this.$options.propsData.storePrefix + 'view/calendar/getDateFieldId',
      }),
    }
  },
  mounted() {
    if (this.dateFieldId === null) {
      this.showChooseDateFieldModal()
    }
  },
  methods: {
    showChooseDateFieldModal() {
      this.$refs.selectDateFieldModal.show()
    },
  },
}
</script>
