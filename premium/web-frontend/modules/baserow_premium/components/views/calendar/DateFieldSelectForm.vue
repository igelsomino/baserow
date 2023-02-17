<template>
  <form @submit.prevent="submit">
    <FormElement class="control">
      <label class="control__label">
        {{ $t('dateFieldSelectForm.dateField') }}
      </label>
      <div class="control__elements">
        <Dropdown v-model="values.dateField" :show-search="true">
          <template #defaultValue>
            <i class="select__item-icon color-neutral fas fa-calendar-alt"></i>
            {{ $t('dateFieldSelectForm.date') }}
          </template>
          <DropdownItem
            v-for="dateField in dateFields"
            :key="dateField.id"
            :name="dateField.name"
            :value="dateField.id"
            :icon="fieldIcon(dateField.type)"
          >
          </DropdownItem>
        </Dropdown>
        <div v-if="fieldHasErrors('dateField')" class="error">
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </FormElement>
    <slot></slot>
  </form>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'DateFieldSelectForm',
  mixins: [form],
  props: {
    table: {
      type: Object,
      required: true,
    },
    dateFields: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      values: {
        dateField: null,
      },
    }
  },
  methods: {
    fieldIcon(type) {
      const ft = this.$registry.get('field', type)
      if (ft && ft.getIconClass() !== null) {
        return ft.getIconClass()
      }
      return 'calendar-alt'
    },
  },
  validations: {
    values: {
      dateField: { required },
    },
  },
}
</script>
