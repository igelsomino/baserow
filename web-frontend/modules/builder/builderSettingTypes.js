import { Registerable } from '@baserow/modules/core/registry'

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
}
