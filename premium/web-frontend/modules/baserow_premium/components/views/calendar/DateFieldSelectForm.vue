<template>
  <form @submit.prevent="submit">
    <FormElement class="control">
      <label class="control__label">
        {{ $t('dateFieldSelectForm.dateField') }}
      </label>
        <div class="control__elements">
          <Dropdown v-model="values.default_role" :show-search="false">
            <DropdownItem
              v-for="role in roles"
              :key="role.uid"
              :name="role.name"
              :value="role.uid"
              :description="role.description"
            >
              {{ role.name }}
              <Badge
                v-if="!role.isBillable && atLeastOneBillableRole"
                primary
                class="margin-left-1"
                >{{ $t('common.free') }}
              </Badge>
            </DropdownItem>
          </Dropdown>
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
  props: {},
  data() {
    return {
      values: {
        dateField: undefined,
      },
    }
  },
  computed: {
    // TODO: Provide a list of fields to choose from
    // viewOwnershipTypes() {
    //   return this.$registry.getAll('viewOwnershipType')
    // },
  },
  mounted() {
    this.$refs.name.focus()
  },
  validations: {
    values: {
      dateField: { required },
    },
  },
}
</script>
