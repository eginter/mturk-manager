<template>
  <tr>
    <td
      v-bind:style="{
        ...stylesCell,
        'paddingLeft': '16px',
      }"
      class="text-xs-left"
    >
      {{ templateWorker.name }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-right"
    >{{ templateWorker.height_frame }} px</td>
    <td
      v-bind:style="stylesCell"
      class="right"
    >
      {{ Object.keys(templateWorker.dict_parameters).length }}
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <span v-if="templateWorker.template_assignment === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.template_assignment.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <span v-if="templateWorker.template_hit === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.template_hit.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <span v-if="templateWorker.template_global === null">
        None
      </span>
      <span v-else>
        {{ templateWorker.template_global.name }}
      </span>
    </td>
    <td
      v-bind:style="stylesCell"
      class="text-xs-center"
    >
      <component-edit-template-worker
        v-bind:key="`component-edit-template-worker-${templateWorker.id}`"
        v-bind:template_worker_current="templateWorker"
        v-on:edited="$emit('edited')"
      />
      <component-delete-template-worker
        v-bind:key="`component-delete-template-worker-${props.item.id}`"
        v-bind:template-worker="props.item"
        v-bind:disabled="templateWorker.has_assignments === true"
        v-on:deleted="snackbar_deleted = true"
      />
    </td>
  </tr>
</template>

<script>
import ComponentEditTemplateWorker from './component_edit_template_worker';
import ComponentDeleteTemplateWorker from './component_delete_template_worker';
export default {
  name: 'ItemTemplatesWorker',
  components: {ComponentDeleteTemplateWorker, ComponentEditTemplateWorker},
  props: {
    props: {
      type: Object,
      required: true,
    },
    isCondensed: {
      required: true,
      type: Boolean,
    },
  },
  data() {
    return {};
  },
  computed: {
    templateWorker() { return this.props.item; },
    stylesCell() {
      if (this.isCondensed) {
        return {
          height: 'unset !important',
          paddingLeft: '5px !important',
          paddingRight: '5px !important',
        };
      }
      return {};
    },
  },
};
</script>

<style scoped>
</style>