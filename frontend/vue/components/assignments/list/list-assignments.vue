<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <base-table
    name-vuex-module="moduleAssignments"
    v-bind:name-state-pagination="nameStatePagination"
    v-bind:name-local-storage-pagination="nameLocalStoragePagination"

    v-bind:function-load-page="loadPage"
    v-bind:array-items="array_items"

    v-bind:name-local-storage-columns-selected="nameLocalStorageColumnsSelected"
    v-bind:name-state-columns="nameStateColumns"
    v-bind:name-state-columns-selected="nameStateColumnsSelected"
    v-bind:name-state-columns-selected-initial="nameStateColumnsSelectedInitial"

    v-bind:name-state-items-selected="nameStateItemsSelected"


    v-bind:function-set-items-selected="function_set_items_selected"
    v-bind:function-clear-items-selected="function_clear_items_selected"

    v-bind:filters="filtersComputed"
    v-bind:filters-default="filtersDefaultComputed"
    v-bind:set-state="setState"
    v-bind:name-state-filters="nameStateFilters"
    v-bind:name-local-storage-filters="nameLocalStorageFilters"
  >
    <template v-slot:default="{ props, array_columns_selected, isCondensed }">
      <component-item-assignment
        v-bind:props="props"
        v-bind:array_columns_selected="array_columns_selected"
        v-bind:show_links="showLinks"
        v-bind:is-condensed="isCondensed"
      />
    </template>

    <template v-slot:filters="{ filters, filtersActive }">
      <filters-table-assignments
        v-bind:filters="filters"
        v-bind:filters-active="filtersActive"
      ></filters-table-assignments>
    </template>

    <template v-slot:actions>
      <slot name="actions"/>
    </template>
  </base-table>
</template>
<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex';
import { Service_Assignments as ServiceAssignments } from '../../../services/service_assignments';
import BaseTable from '../../base-table';
import ComponentItemAssignment from './component_item_assignment';
import FiltersTableAssignments from './filters-table-assignments';

export default {
  name: 'ListAssignments',
  components: {FiltersTableAssignments, ComponentItemAssignment, BaseTable },
  props: {
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationGeneral',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_assignments_general',
    },

    nameStateColumns: {
      required: false,
      type: String,
      default: 'array_columns_general',
    },
    nameLocalStorageColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_assignments_general',
    },
    nameStateColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_selected_general',
    },
    nameStateColumnsSelectedInitial: {
      required: false,
      type: String,
      default: 'array_columns_selected_initial_general',
    },

    nameStateItemsSelected: {
      required: false,
      type: String,
      default: 'object_assignments_selected',
    },


    showLinks: {
      required: false,
      type: Boolean,
      default: true,
    },

    filters: {
      required: false,
      type: Object,
      default: undefined,
    },
    filtersDefault: {
      required: false,
      type: Object,
      default: undefined,
    },
    nameStateFilters: {
      required: false,
      type: String,
      default: 'objectFiltersGeneral',
    },
    nameLocalStorageFilters: {
      required: false,
      type: String,
      default: 'filtersAssignmentsGeneral',
    },
  },
  data() {
    return {
      loadPage: ServiceAssignments.load_page,
    };
  },
  computed: {
    filtersComputed() {
      return this.filters !== undefined ? this.filters : this.filtersGeneral;
    },
    filtersDefaultComputed() {
      return this.filtersDefault !== undefined ? this.filtersDefault : this.filtersDefaultGeneral;
    },
    ...mapGetters('moduleAssignments', {
      array_items: 'get_array_assignments',
    }),
    ...mapState('moduleAssignments', {
      filtersGeneral: 'objectFiltersGeneral',
      filtersDefaultGeneral: 'objectFiltersDefaultGeneral',
    }),
  },
  methods: {
    ...mapActions('moduleAssignments', {
      function_reset_array_columns: 'reset_array_columns_general',
      setState: 'setState',
    }),
    ...mapMutations('moduleAssignments', {
      function_set_items_selected: 'set_assignments_selected',
      function_clear_items_selected: 'clear_assignments_selected',
      function_set_array_columns: 'set_array_columns_general',
    }),
  },
};
</script>

<style scoped></style>
