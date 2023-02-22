<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('createPageModal.header') }}
    </h2>
    <CreatePageForm :builder="builder" @submit="addPage"></CreatePageForm>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import { notifyIf } from '@baserow/modules/core/utils/error'
import CreatePageForm from '@baserow/modules/builder/components/page/CreatePageForm'

export default {
  name: 'CreatePageModal',
  components: { CreatePageForm },
  mixins: [modal],
  props: {
    builder: {
      type: Object,
      required: true,
    },
  },
  methods: {
    addPage({ name }) {
      try {
        this.$store.dispatch('page/add', {
          builder: this.builder,
          name,
        })
        this.hide()
      } catch (error) {
        notifyIf(error, 'application')
      }
    },
  },
}
</script>
