<template>
  <ul v-if="!tableLoading" class="header__filter header__filter--full-width">
    <li class="header__filter-item">
      <a
        class="header__filter-link"
      >
        <i class="header__filter-icon fas fa-calendar-alt"></i>
        <span class="header__filter-name">
          <template v-if="view.date_field === null">{{
            $t('calendarViewHeader.displayBy')
          }}</template
          ><template v-else>{{
            $t('calendarViewHeader.displayedBy', {
              fieldName: displayedByFieldName,
            })
          }}</template>
        </span
        >
      </a>
    </li>
    <li v-if="dateFieldId !== null" class="header__filter-item">
      <a
        ref="customizeContextLink"
        class="header__filter-link"
        @click="
          $refs.customizeContext.toggle(
            $refs.customizeContextLink,
            'bottom',
            'left',
            4
          )
        "
      >
        <i class="header__filter-icon fas fa-list-ul"></i>
        <span class="header__filter-name">{{
          $t('calendarViewHeader.labels')
        }}</span>
      </a>
      <ViewFieldsContext
        ref="customizeContext"
        :database="database"
        :view="view"
        :fields="fields"
        :field-options="fieldOptions"
        :allow-cover-image-field="false"
        @update-all-field-options="updateAllFieldOptions"
        @update-field-options-of-field="updateFieldOptionsOfField"
        @update-order="orderFieldOptions"
      ></ViewFieldsContext>
    </li>
  </ul>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import { notifyIf } from '@baserow/modules/core/utils/error'

import ViewFieldsContext from '@baserow/modules/database/components/view/ViewFieldsContext'

export default {
  name: 'CalendarViewHeader',
  components: {
    ViewFieldsContext,
  },
  props: {
    storePrefix: {
      type: String,
      required: true,
      default: ''
    },
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    displayedByFieldName() {
      for (let i = 0; i < this.fields.length; i++) {
        if (this.fields[i].id === this.view.date_field) {
          return this.fields[i].name
        }
      }
      return ''
    },
    ...mapState({
      tableLoading: (state) => state.table.loading,
    }),
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
          this.$options.propsData.storePrefix + 'view/calendar/getAllFieldOptions',
        dateFieldId:
          this.$options.propsData.storePrefix + 'view/calendar/getDateFieldId',
      }),
    }
  },
  methods: {
    async updateAllFieldOptions({ newFieldOptions, oldFieldOptions }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/calendar/updateAllFieldOptions',
          {
            newFieldOptions,
            oldFieldOptions,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.group.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateFieldOptionsOfField({ field, values, oldValues }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/calendar/updateFieldOptionsOfField',
          {
            field,
            values,
            oldValues,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.group.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async orderFieldOptions({ order }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/calendar/updateFieldOptionsOrder',
          {
            order,
            readOnly: this.readOnly,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  }
}
</script>
