import path from 'path'

export const routes = [
  {
    name: 'website-page',
    path: '*',
    component: path.resolve(__dirname, 'pages/publishedWebsitePage.vue'),
    // If publishedWebsiteRoute is true, then that route will only be used on a
    // different subdomain.
    meta: { publishedWebsiteRoute: true },
  },
  {
    name: 'website-page',
    // This route to the preview of the website
    path: '/preview/application/:id/page*',
    component: path.resolve(__dirname, 'pages/previewWebsitePage.vue'),
  },
]
