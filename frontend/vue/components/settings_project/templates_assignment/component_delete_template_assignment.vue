<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-btn
      slot="activator"
      class="my-0"
      icon
      small
    >
      <v-icon color="error">delete</v-icon>
    </v-btn>

    <v-card>
      <!-- <v-card-title>
            <span class="headline">Add Profile</span>
            <v-spacer></v-spacer>
            <v-btn icon v-on:click="dialog = false">
                <v-icon>close</v-icon>
            </v-btn>
        </v-card-title> -->
      <v-card-text>
        Do you really want to delete the worker template '{{
          template_assignment.name
        }}'?
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat color="error" v-on:click="remove()">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  mapState, mapMutations, mapActions, mapGetters,
} from 'vuex';
import { Service_Templates } from '../../../services/service_templates';

export default {
  name: 'ComponentDeleteTemplateAssignment',
  props: {
    template_assignment: {},
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    remove() {
      Service_Templates.delete({
        typeTemplate: 'assignment',
        project: this.project_current,
        template: this.template_assignment,
        callback: () => {
          Service_Templates.cleanup({
            typeTemplate: 'assignmentAll',
            component: this,
            nameEvent: 'deleted',
            template: this.template_assignment,
          });
        },
      });
    },
    ...mapActions('moduleProjects', {
      delete_template_assignment: 'delete_template_assignment',
    }),
  },
  computed: {
    ...mapGetters('moduleProjects', {
      project_current: 'get_project_current',
    }),
  },
  components: {},
};
</script>

<style scoped></style>
