<template>
  <Context>
    <ViewDecoratorList
      v-if="augmentedDecorations.length === 0"
      :view="view"
      @select="addDecoration($event)"
    />
    <div v-else class="decorator-context">
      <div class="decorator-context__list">
        <div
          v-for="dec in augmentedDecorations"
          :key="dec.decoration.id"
          class="decorator-context__decorator"
        >
          <div class="decorator-context__decorator-header">
            <div class="decorator-context__decorator-header-info">
              <ViewDecoratorItem :decorator-type="dec.decoratorType" />
            </div>
            <div
              v-show="dec.decoration.value_provider"
              class="decorator-context__decorator-header-select"
            >
              <Picker
                v-if="dec.decoration.value_provider"
                :icon="dec.valueProviderType.getIconClass()"
                :name="dec.valueProviderType.getName()"
                @select="selectValueProvider(dec.decoration, $event)"
              >
                <template #default="{ hidePicker }">
                  <div
                    class="
                      decorator-context__decorator-value-provider-select-list
                    "
                  >
                    <DecoratorValueProviderList
                      :decoration="dec.decoration"
                      @select="
                        ;[
                          selectValueProvider(dec.decoration, $event),
                          hidePicker(),
                        ]
                      "
                    />
                  </div>
                </template>
              </Picker>
            </div>
            <div class="decorator-context__decorator-header-trash">
              <a
                class="decorator-context__decorator-header-trash-link"
                @click="removeDecoration(dec.decoration)"
              >
                <i class="fa fa-trash" />
              </a>
            </div>
          </div>
          <component
            :is="dec.valueProviderType.getFormComponent()"
            v-if="dec.valueProviderType"
            :view="view"
            :table="table"
            :fields="allFields"
            :read-only="readOnly"
            :options="dec.decoration.value_provider_conf"
            @update="updateDecorationOptions(dec.decoration, $event)"
          />
          <DecoratorValueProviderList
            v-else
            :decoration="dec.decoration"
            :direction="'row'"
            @select="selectValueProvider(dec.decoration, $event)"
          />
        </div>
      </div>
      <div class="decorator-context__footer">
        <a
          ref="addDecoratorLink"
          class="decorator-context__add"
          @click="
            $refs.selectDecoratorContext.toggle(
              $refs.addDecoratorLink,
              'bottom',
              'left',
              4
            )
          "
        >
          <i class="fas fa-plus" />
          {{ $t('viewDecoratorContext.addDecorator') }}
        </a>
        <SelectViewDecoratorContext
          ref="selectDecoratorContext"
          :view="view"
          @select="
            ;[$refs.selectDecoratorContext.hide(), addDecoration($event)]
          "
        />
      </div>
    </div>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import ViewDecoratorList from '@baserow/modules/database/components/view/ViewDecoratorList'
import ViewDecoratorItem from '@baserow/modules/database/components/view/ViewDecoratorItem'
import SelectViewDecoratorContext from '@baserow/modules/database/components/view/SelectViewDecoratorContext'
import DecoratorValueProviderItem from '@baserow/modules/database/components/view/DecoratorValueProviderItem'
import DecoratorValueProviderList from '@baserow/modules/database/components/view/DecoratorValueProviderList'

export default {
  name: 'ViewDecoratorContext',
  components: {
    ViewDecoratorList,
    ViewDecoratorItem,
    DecoratorValueProviderItem,
    SelectViewDecoratorContext,
    DecoratorValueProviderList,
  },
  mixins: [context],
  props: {
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    allFields() {
      return [this.primary, ...this.fields]
    },
    augmentedDecorations() {
      return this.view.decorations.map((decoration) => {
        const deco = { decoration }
        deco.decoratorType = this.$registry.get(
          'viewDecorator',
          decoration.type
        )

        if (decoration.value_provider) {
          deco.valueProviderType = this.$registry.get(
            'decoratorValueProvider',
            decoration.value_provider
          )
        }

        deco.availableValueProviderTypes = this.$registry
          .getOrderedList('decoratorValueProvider')
          .filter((valueProviderType) =>
            valueProviderType.isCompatible(deco.decoratorType)
          )

        deco.isDeactivated = deco.decoratorType.isDeactivated({
          view: this.view,
        })

        return deco
      })
    },
  },
  methods: {
    async removeDecoration(decoration) {
      await this.$store.dispatch('view/deleteDecoration', {
        view: this.view,
        decoration,
      })
    },
    async selectValueProvider(decoration, valueProvider) {
      const valueProviderType = this.$registry.get(
        'decoratorValueProvider',
        valueProvider
      )
      await this.$store.dispatch('view/updateDecoration', {
        view: this.view,
        values: {
          value_provider: valueProviderType.getType(),
          value_provider_conf: valueProviderType.getDefaultConfiguration({
            view: this.view,
            fields: this.fields,
          }),
        },
        decoration,
      })
    },
    async addDecoration(decoratorType) {
      const decoration = {
        type: decoratorType.getType(),
        value_provider: null,
      }
      await this.$store.dispatch('view/createDecoration', {
        view: this.view,
        values: decoration,
      })
    },
    async updateDecorationOptions(decoration, options) {
      await this.$store.dispatch('view/updateDecoration', {
        view: this.view,
        values: { value_provider_conf: options },
        decoration,
      })
    },
  },
}
</script>