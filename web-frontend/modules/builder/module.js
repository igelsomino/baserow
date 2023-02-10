import path from 'path'

import { routes } from './routes'
import en from './locales/en.json'
import fr from './locales/fr.json'
import nl from './locales/nl.json'
import de from './locales/de.json'
import it from './locales/it.json'
import es from './locales/es.json'
import pl from './locales/pl.json'

export default function BuilderModule(options) {
  this.addPlugin({ src: path.resolve(__dirname, 'middleware.js') })

  // Add the plugin to register the database application.
  this.appendPlugin({
    src: path.resolve(__dirname, 'plugin.js'),
  })

  // Override the existing generated nuxt router.js file, so that we can change the
  // used router.
  this.addPlugin({
    src: path.resolve(__dirname, 'plugins/router.js'),
    fileName: 'router.js',
  })
  // Create a with the old router that can be used by the `plugins/router.js`
  this.addTemplate({
    fileName: 'defaultRouter.js',
    src: require.resolve('@nuxt/vue-app/template/router'),
  })

  // Add all the related routes.
  this.extendRoutes((configRoutes) => {
    configRoutes.push(...routes)
  })

  this.nuxt.hook('i18n:extend-messages', function (additionalMessages) {
    additionalMessages.push({ en, fr, nl, de, it, es, pl })
  })
}
