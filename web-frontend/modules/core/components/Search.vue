<template>
  <div>
    <i class="fas fa-sm fa-search"></i>
    <input
      type="text"
      class="margin-left-1"
      :placeholder="placeholder"
      :class="{ 'search-input--simple': simple }"
      v-bind="$attrs"
      v-on="$listeners"
    />
  </div>
</template>

<script>
export default {
  name: 'Search',
  inheritAttrs: false,
  props: {
    placeholder: {
      type: String,
      required: false,
      default: null,
    },
    simple: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
