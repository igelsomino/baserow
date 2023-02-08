<template>
  <SidebarApplication
    :group="group"
    :application="application"
    @selected="selected"
  >
  </SidebarApplication>
</template>

<script>
import SidebarApplication from '@baserow/modules/core/components/sidebar/SidebarApplication'

export default {
  name: 'TemplateSidebar',
  components: { SidebarApplication },
  props: {
    application: {
      type: Object,
      required: true,
    },
    group: {
      type: Object,
      required: true,
    },
  },
  methods: {
    selected() {
      console.log('TODO')
    },
  },
}
</script>
