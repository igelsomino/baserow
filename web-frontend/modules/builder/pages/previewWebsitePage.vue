<template>
  <PageContent
    :application="application"
    :path="path"
    :page="page"
    :params="params"
  />
</template>

<script>
import PageContent from '@baserow/modules/builder/components/PageContent'
import publicSiteService from '@baserow/modules/builder/services/builderApplication.js'
import { resolveApplicationRoute } from '@baserow/modules/builder/utils/routing'

export default {
  components: { PageContent },
  async asyncData(context) {
    const application = await publicSiteService(context.$client).fetchById(
      context.route.params.id
    )

    const found = resolveApplicationRoute(
      application,
      context.route.params.pathMatch
    )
    // Handle 404
    if (!found) {
      context.error({
        statusCode: 404,
        message: 'Page not found.',
      })
      return {}
    }

    const [page, path, params] = found

    return {
      application,
      page,
      path,
      params,
    }
  },
}
</script>
