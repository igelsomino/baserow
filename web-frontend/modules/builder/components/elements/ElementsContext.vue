<template>
  <Context class="elements-context">
    <Search
      v-model="search"
      :placeholder="$t('elementsContext.searchPlaceholder')"
      class="elements-context__search"
      simple
    />
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'ElementsContext',
  mixins: [context],
  data() {
    return {
      search: 'test',
    }
  },
}
</script>
