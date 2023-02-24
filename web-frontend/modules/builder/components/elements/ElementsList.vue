<template>
  <ul>
    <li v-for="element in elements" :key="element.getType()">
      <a>
        <i :class="`fas fa-${element.iconClass}`"></i>
        <span class="margin-left-1"> {{ element.name }}</span>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'ElementsList',
  props: {
    elements: {
      type: Array,
      required: true,
    },
  },
}
</script>
