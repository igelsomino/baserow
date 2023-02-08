import { Registerable } from '@baserow/modules/core/registry'
import IntegrationSettings from '@baserow/modules/builder/components/settings/IntegrationSettings'
import ThemeSettings from '@baserow/modules/builder/components/settings/ThemeSettings'

class BuilderSettingType extends Registerable {
  getType() {
    return null
  }

  getName() {
    return null
  }

  getComponent() {
    return null
  }
}

export class IntegrationsBuilderSettingsType extends BuilderSettingType {
  getType() {
    return 'integrations'
  }

  getName() {
    return this.app.i18n.t('builderSettingTypes.integrationsName')
  }

  getOrder() {
    return 1
  }

  getComponent() {
    return IntegrationSettings
  }
}

export class ThemeBuilderSettingsType extends BuilderSettingType {
  getType() {
    return 'theme'
  }

  getName() {
    return this.app.i18n.t('builderSettingTypes.themeName')
  }

  getOrder() {
    return 2
  }

  getComponent() {
    return ThemeSettings
  }
}
