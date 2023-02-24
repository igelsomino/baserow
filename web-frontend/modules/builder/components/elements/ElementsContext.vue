<template>
  <Context class="elements-context">
    <Search
      :placeholder="$t('elementsContext.searchPlaceholder')"
      class="elements-context__search"
      simple
      @input="search = $event.target.value"
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
      search: null,
    }
  },
  computed: {
    elements() {
      // TODO Instead of all elements these need to be the elements currently on the
      // page
      const allElements = Object.values(this.$registry.getAll('element'))

      if (
        this.search === '' ||
        this.search === null ||
        this.search === undefined
      ) {
        return allElements
      }

      return allElements.filter((element) => {
        const nameSanitised = element.name.toLowerCase()
        const searchSanitised = this.search.toLowerCase().trim()
        return nameSanitised.includes(searchSanitised)
      })
    },
  },
}
</script>
