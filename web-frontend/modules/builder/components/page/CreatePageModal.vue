<template>
  <Modal>
    <h2 class="create-page-modal__header">
      {{ $t('createPageModal.header') }}
    </h2>
    <div class="control">
      <label class="control__label">
        <i class="fas fa-font"></i>
        {{ $t('createPageModal.nameLabel') }}
      </label>
      <input
        v-model="pageName"
        type="text"
        class="input input--large"
        :placeholder="$t('createPageModal.namePlaceholder')"
      />
    </div>
    <div class="create-page-modal__controls">
      <button class="button button--large" @click="addPage">
        {{ $t('createPageModal.submit') }}
      </button>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'CreatePageModal',
  mixins: [modal],
  props: {
    builder: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      pageName: null,
    }
  },
  methods: {
    addPage() {
      try {
        this.$store.dispatch('page/add', {
          builder: this.builder,
          name: this.pageName,
        })
        this.hide()
      } catch (error) {
        notifyIf(error, 'application')
      }
    },
  },
}
</script>
