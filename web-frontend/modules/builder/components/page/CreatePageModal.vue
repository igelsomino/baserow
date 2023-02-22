<template>
  <Modal>
    <h2 class="box__title">
      {{ $t('createPageModal.header') }}
    </h2>
    <CreatePageForm
      :loading="loading"
      :builder="builder"
      @submit="addPage"
    ></CreatePageForm>
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
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async addPage({ name }) {
      this.loading = true
      try {
        const page = await this.$store.dispatch('page/add', {
          builder: this.builder,
          name,
        })
        await this.$router.push({
          name: 'builder-page',
          params: { builderId: this.builder.id, pageId: page.id },
        })
        this.hide()
      } catch (error) {
        notifyIf(error, 'application')
      }
      this.loading = false
    },
  },
}
</script>
