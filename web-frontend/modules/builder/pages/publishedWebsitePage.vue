<template>
  <div>@TODO show page {{ hostname }}{{ path }}</div>
</template>

<script>
export default {
  asyncData(context) {
    const host = process.server
      ? context.req.headers.host
      : window.location.host
    const hostname = new URL(`http://${host}`).hostname
    return {
      hostname,
      path: context.route.path,
    }
  },
}
</script>
