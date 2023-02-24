<template>
  <h1>{{ value }}</h1>
</template>

<script>
import textElement from '@baserow/modules/builder/mixins/elements/textElement'

export default {
  name: 'HeaderElement',
  mixins: [textElement],
}
</script>
