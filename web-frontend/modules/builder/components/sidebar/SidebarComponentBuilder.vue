<template>
  <div>
    <SidebarApplication
      ref="sidebarApplication"
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
          <a @click="settingsClicked">
            <i class="context__menu-icon fas fa-fw fa-cog"></i>
            {{ $t('sidebarComponentBuilder.settings') }}
          </a>
        </li>
      </template>
      <template v-if="isAppSelected(application)" #body>
        <ul class="tree__subs">
          <SidebarItemBuilder
            v-for="page in orderedPages"
            :key="page.id"
            :builder="application"
            :page="page"
          ></SidebarItemBuilder>
        </ul>
      </template>
    </SidebarApplication>
    <BuilderSettingsModal ref="builderSettingsModal"></BuilderSettingsModal>
  </div>
</template>

<script>
import SidebarApplication from '@baserow/modules/core/components/sidebar/SidebarApplication'
import BuilderSettingsModal from '@baserow/modules/builder/components/settings/BuilderSettingsModal'
import { mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import SidebarItemBuilder from '@baserow/modules/builder/components/sidebar/SidebarItemBuilder'

export default {
  name: 'TemplateSidebar',
  components: { SidebarItemBuilder, BuilderSettingsModal, SidebarApplication },
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
  computed: {
    ...mapGetters({ isAppSelected: 'application/isSelected' }),
    orderedPages() {
      return this.application.pages
        .map((page) => page)
        .sort((a, b) => a.order - b.order)
    },
  },
  methods: {
    selected(application) {
      try {
        this.$store.dispatch('application/select', application)
      } catch (error) {
        notifyIf(error, 'group')
      }
    },
    settingsClicked() {
      this.$refs.sidebarApplication.$refs.context.hide()
      this.$refs.builderSettingsModal.show()
    },
  },
}
</script>
