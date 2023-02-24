import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/page/components/ParagraphElement'

export class ElementType extends Registerable {
  get name() {
    return null
  }

  get iconClass() {
    return null
  }

  get component() {
    return null
  }

  /**
   * By default, the properties available for an element are the props of its component.
   * You can override this function to define your own props that are made available
   * to the user.
   *
   * @returns {string[]}
   */
  get properties() {
    if (this.component !== null) {
      return Object.keys(this.component.$props)
    }
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

  get component() {
    return ParagraphElement
  }
}

export class ParagraphElementType extends Registerable {
  getType() {
    return 'paragraph'
  }

  get name() {
    return this.app.i18n.t('elementType.paragraph')
  }

  get iconClass() {
    return 'paragraph'
  }

  get component() {
    return ParagraphElement
  }
}
