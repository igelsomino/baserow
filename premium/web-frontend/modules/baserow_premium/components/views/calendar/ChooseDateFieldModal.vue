<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('chooseDateFieldModal.chooseField') }}
    </h2>
    <Error :error="error"></Error>
    <DateFieldSelectForm
      ref="dateFieldSelectForm"
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
            {{ $t('chooseDateFieldModal.save') }}
          </button>
        </div>
      </div>
    </DateFieldSelectForm>
  </Modal>
</template>
<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'

export default {
  name: 'ChooseDateFieldModal',
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
    }
  },
  methods: {
    async submitted(values) {
      this.hideError()

      // TODO: set view date field
      // try {
      //   const { view } = await this.$store.dispatch('view/create', {
      //     type: this.viewType.type,
      //     table: this.table,
      //     values,
      //   })
      //   this.loading = false
      //   this.$emit('created', view)
      //   this.hide()
      // } catch (error) {
      //   this.loading = false
      //   this.handleError(error, 'view')
      // }
    },
  },
}
</script>
