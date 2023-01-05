<template>
  <form @submit.prevent="submit">
    <FormElement :error="fieldHasErrors('name')" class="control">
      <label class="control__label">
        {{ $t('viewForm.name') }}
      </label>
      <div class="control__elements">
        <input
          ref="name"
          v-model="values.name"
          :class="{ 'input--error': fieldHasErrors('name') }"
          type="text"
          class="input input--large"
          @focus.once="$event.target.select()"
          @blur="$v.values.name.$touch()"
        />
        <div v-if="fieldHasErrors('name')" class="error">
          {{ $t('error.requiredField') }}
        </div>
      </div>
    </FormElement>
    <FormElement class="control">
      <label class="control__label">
        {{ $t('viewForm.whoCanEdit') }}
      </label>
      <div class="control__elements view-ownership-select">
        <Radio v-model="values.ownershipType" value="collaborative"
          ><i class="fas fa-users"></i>
          {{ $t('viewForm.collaborative') }}</Radio
        >
        <Radio
          v-model="values.ownershipType"
          value="personal"
          :disabled="!hasPremiumFeaturesEnabled"
          ><i class="fas fa-user-tag"></i> {{ $t('viewForm.personal') }}
          <div v-if="!hasPremiumFeaturesEnabled" class="deactivated-label">
            <i class="fas fa-lock"></i></div
        ></Radio>
      </div>
    </FormElement>
    <slot></slot>
  </form>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'
import Radio from '@baserow/modules/core/components/Radio'
import PremiumFeatures from '@baserow_premium/features'

export default {
  name: 'ViewForm',
  components: { Radio },
  mixins: [form],
  props: {
    defaultName: {
      type: String,
      required: false,
      default: '',
    },
    database: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      values: {
        name: this.defaultName,
        ownershipType: 'collaborative',
      },
    }
  },
  computed: {
    hasPremiumFeaturesEnabled() {
      return this.$hasFeature(PremiumFeatures.PREMIUM, this.database.group.id)
    },
  },
  mounted() {
    this.$refs.name.focus()
  },
  validations: {
    values: {
      name: { required },
    },
  },
}
</script>
