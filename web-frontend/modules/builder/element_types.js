import { Registerable } from '@baserow/modules/core/registry'

export class ElementType extends Registerable {
  get name() {
    return null
  }

  get iconClass() {
    return null
  }
}

export class HeaderElementType extends Registerable {
  getType() {
    return 'header'
  }

  get name() {
    return this.app.i18n.t('elementType.header')
  }

  get iconClass() {
    return 'heading'
  }
}
