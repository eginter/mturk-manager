<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <base-table
    name-vuex-module="moduleMessages"
    v-bind:name-state-pagination="nameStatePagination"
    v-bind:name-local-storage-pagination="nameLocalStoragePagination"

    v-bind:function-load-page="loadPage"
    v-bind:array-items="arrayItems"

    name-state-columns="arrayColumns"
    v-bind:name-state-columns-selected="nameStateColumnsSelected"
    v-bind:is-condensed="true"
  >
    <template v-slot:default="{ props, array_columns_selected, isCondensed, refresh }">
      <item-messages-reject
        v-bind:props="props"
        v-bind:array-columns-selected="array_columns_selected"
        v-bind:is-condensed="isCondensed"

        v-on:delete="refresh()"
      />
    </template>

    <template v-slot:actions="{ refresh }">
      <item-add-message
        v-on:create="refresh()"
      />
    </template>
  </base-table>
</template>

<script>
import { mapState } from 'vuex';
import BaseTable from '../base-table';
import { ServiceMessages } from '../../services/Service_Messages_Reject';
import ItemMessagesReject from './item-messages-reject';
import ItemAddMessage from './item-add-message';

export default {
  name: 'TableMessagesReject',
  components: { ItemAddMessage, ItemMessagesReject, BaseTable },
  props: {
    loadPage: {
      required: false,
      type: Function,
      default: ServiceMessages.loadPageReject,
    },
    nameStatePagination: {
      required: false,
      type: String,
      default: 'paginationMessagesReject',
    },
    nameLocalStoragePagination: {
      required: false,
      type: String,
      default: 'pagination_messages_reject',
    },
    nameStateColumnsSelected: {
      required: false,
      type: String,
      default: 'array_columns_selected',
    },
  },
  computed: {
    ...mapState('moduleMessages', {
      arrayItems: 'arrayItemsReject',
    }),
  },
};
</script>
