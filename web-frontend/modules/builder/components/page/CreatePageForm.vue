<template>
  <form @submit.prevent="submit">
    <FormElement :error="fieldHasErrors('name')" class="control">
      <label class="control__label">
        <i class="fas fa-font"></i>
        {{ $t('createPageForm.nameLabel') }}
      </label>
      <input
        ref="name"
        v-model="values.name"
        type="text"
        class="input input--large"
        :class="{ 'input--error': fieldHasErrors('name') }"
        @focus.once="$event.target.select()"
        @blur="$v.values.name.$touch()"
      />
      <div
        v-if="$v.values.name.$dirty && !$v.values.name.required"
        class="error"
      >
        {{ $t('error.requiredField') }}
      </div>
      <div
        v-if="$v.values.name.$dirty && !$v.values.name.isUnique"
        class="error"
      >
        {{ $t('createPageForm.errorNameNotUnique') }}
      </div>
    </FormElement>
    <FormElement>
      <div class="actions actions--right">
        <button class="button button--large" type="submit">
          {{ $t('createPageForm.submit') }}
        </button>
      </div>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import { required } from 'vuelidate/lib/validators'
import { getNextAvailableNameInSequence } from '@baserow/modules/core/utils/string'

export default {
  name: 'CreatePageForm',
  mixins: [form],
  props: {
    builder: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: ['name'],
      values: {
        name: null,
      },
    }
  },
  computed: {
    pageNames() {
      return this.builder.pages.map((page) => page.name)
    },
    defaultName() {
      const baseName = this.$t('createPageForm.defaultName')
      return getNextAvailableNameInSequence(baseName, this.pageNames)
    },
  },
  created() {
    this.values.name = this.defaultName
  },
  mounted() {
    this.$refs.name.focus()
  },
  methods: {
    submit() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      this.$emit('submit', this.values)
    },
    isNameUnique(name) {
      return !this.pageNames.includes(name)
    },
  },
  validations() {
    return {
      values: {
        name: { required, isUnique: this.isNameUnique },
      },
    }
  },
}
</script>
