<template>
  <form @submit.prevent="submit">
    <FormElement :error="fieldHasErrors('name')" class="control">
      <label class="control__label">
        <i class="fas fa-font"></i>
        {{ $t('createPageForm.nameLabel') }}
      </label>
      <input
        v-model="values.name"
        type="text"
        class="input input--large"
        :placeholder="$t('createPageForm.namePlaceholder')"
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
      <div class="create-page-form__controls">
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
  methods: {
    submit() {
      this.$v.$touch()
      if (this.$v.$invalid) {
        return
      }
      this.$emit('submit', this.values)
    },
    isNameUnique(name) {
      return !this.builder.pages.map((page) => page.name).includes(name)
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
