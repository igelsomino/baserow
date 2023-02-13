<template>
  <li class="tree__sub" :class="{ active: page._.selected }">
    <a
      class="tree__sub-link"
      :title="page.name"
      :href="resolvePageHref(builder, page)"
      @mousedown.prevent
      @click.prevent="selectPage(builder, page)"
    >
      <Editable
        :value="page.name"
        @change="renamePage(builder, page, $event)"
      ></Editable>
    </a>
  </li>
</template>

<script>
export default {
  name: 'SidebarItemBuilder',
  props: {
    builder: {
      type: Object,
      required: true,
    },
    page: {
      type: Object,
      required: true,
    },
  },
  methods: {
    setLoading(database, value) {
      this.$store.dispatch('application/setItemLoading', {
        application: database,
        value,
      })
    },
    selectPage(builder, page) {
      this.setLoading(builder, true)
      this.$nuxt.$router.push(
        {
          name: 'builder-page',
          params: {
            builderId: builder.id,
            pageId: page.id,
          },
        },
        () => {
          this.setLoading(builder, false)
        },
        () => {
          this.setLoading(builder, false)
        }
      )
    },
    resolvePageHref(builder, page) {
      const props = this.$nuxt.$router.resolve({
        name: 'builder-page',
        params: {
          builderId: builder.id,
          pageId: page.id,
        },
      })

      return props.href
    },
    renamePage(builder, page) {
      console.log('TODO')
    },
  },
}
</script>
