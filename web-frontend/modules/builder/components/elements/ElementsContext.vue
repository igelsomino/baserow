<template>
  <Context class="elements-context">
    <Search
      v-model="search"
      :placeholder="$t('elementsContext.searchPlaceholder')"
      class="elements-context__search"
      simple
    />
    <ElementsList class="context__menu" :elements="elements" />
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import ElementsList from '@baserow/modules/builder/components/elements/ElementsList'

export default {
  name: 'ElementsContext',
  components: { ElementsList },
  mixins: [context],
  data() {
    return {
      search: 'test',
    }
  },
  computed: {
    elements() {
      return this.$registry.getAll('element')
    },
  },
}
</script>
