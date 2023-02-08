<template>
  <SidebarApplication
    :group="group"
    :application="application"
    @selected="selected"
  >
    <template #context>
      <li
        v-if="
          $hasPermission(
            'application.update',
            application,
            application.group.id
          )
        "
      >
        <a>
          <i class="context__menu-icon fas fa-fw fa-cog"></i>
          {{ $t('sidebarComponentBuilder.settings') }}
        </a>
      </li>
    </template>
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
