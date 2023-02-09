import Router from 'vue-router'

import {
  createRouter as createDefaultRouter,
  routerOptions,
} from './defaultRouter'

export function createRouter(ssrContext, config) {
  const options =
    routerOptions || createDefaultRouter(ssrContext, config).options
  let isWebFrontendHostname = false

  if (process.server && ssrContext && ssrContext.nuxt && ssrContext.req) {
    const req = ssrContext.req
    const frontendHostname = new URL(ssrContext.req.env.PUBLIC_WEB_FRONTEND_URL)
      .hostname
    const requestHostname = new URL(`http://${req.headers.host}`).hostname
    isWebFrontendHostname = frontendHostname === requestHostname
    ssrContext.nuxt.isWebFrontendHostname = isWebFrontendHostname
  }
  if (
    process.client &&
    window.__NUXT__ &&
    window.__NUXT__.isWebFrontendHostname
  ) {
    isWebFrontendHostname = window.__NUXT__.isWebFrontendHostname
  }

  const newRoutes = options.routes.filter((route) => {
    const isPublishedWebsiteRoute = !!route?.meta?.publishedWebsiteRoute
    return (
      (isWebFrontendHostname && !isPublishedWebsiteRoute) ||
      (!isWebFrontendHostname && isPublishedWebsiteRoute)
    )
  })

  // @TODO show special 404 or 500 page when publicWebsiteRoutes is true.
  return new Router({
    ...options,
    routes: newRoutes,
  })
}
