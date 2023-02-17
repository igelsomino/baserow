<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('selectDateFieldModal.chooseDateField') }}
    </h2>
    <Error :error="error"></Error>
    <DateFieldSelectForm
      ref="dateFieldSelectForm"
      :date-fields="dateFields"
      :table="table"
      @submitted="submitted"
    >
      <div class="actions">
        <div class="align-right">
          <button
            class="button button--large"
            :class="{ 'button--loading': loading }"
            :disabled="loading"
          >
            {{ $t('selectDateFieldModal.save') }}
          </button>
        </div>
      </div>
    </DateFieldSelectForm>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'
import DateFieldSelectForm from '@baserow_premium/components/views/calendar/DateFieldSelectForm'
import FieldService from '@baserow/modules/database/services/field'
import ViewService from '@baserow/modules/database/services/view'

export default {
  name: 'ChooseDateFieldModal',
  components: {
    DateFieldSelectForm,
  },
  mixins: [modal, error],
  props: {
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    database: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      dateFields: [],
    }
  },
  async fetch() {
    this.loading = true
    try {
      const dataFieldTypes = Object.values(this.$registry.getAll('field'))
        .filter((fieldType) => fieldType.isDateField() === true)
        .map((fieldType) => fieldType.getType())
      const { data } = await FieldService(this.$client).fetchAll(this.table.id)
      this.dateFields = data.filter((field) =>
        dataFieldTypes.includes(field.type)
      )
    } catch (error) {
      this.loading = false
      this.handleError(error)
    } finally {
      this.loading = false
    }
  },
  methods: {
    async submitted(values) {
      this.loading = true
      this.hideError()
      try {
        await ViewService(this.$client).update(this.view.id, {
          date_field: values.dateField,
        })
        this.loading = false
        this.hide()
      } catch (error) {
        this.handleError(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
