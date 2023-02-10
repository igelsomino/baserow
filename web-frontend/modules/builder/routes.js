import path from 'path'

export const routes = [
  {
    name: 'published-website-page',
    path: '*',
    component: path.resolve(__dirname, 'pages/publishedWebsitePage.vue'),
    // If publishedWebsiteRoute is true, then that route will only be used on a
    // different subdomain.
    meta: { publishedWebsiteRoute: true },
  },
]
