<template>
  <header class="layout__col-2-1 header header--space-between">
    <ul class="header__filter">
      <li class="header__filter-item">
        <PageHeaderElements />
      </li>
    </ul>
  </header>
</template>

<script>
import PageHeaderElements from '@baserow/modules/builder/components/elements/PageHeaderElements'
export default {
  name: 'PageHeader',
  components: { PageHeaderElements },
}
</script>
