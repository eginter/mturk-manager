<template>
  <v-tooltip top>
    <template v-slot:activator="{ on }">
      <v-icon
        v-if="hasUnseenVersions"
        small
        color="warning"
        v-on="on"
      >
        warning
      </v-icon>
    </template>

    <span>
      Check the changelog for new features and fixes
    </span>
  </v-tooltip>
</template>

<script>
import { compareVersions } from '../../helpers';

export default {
  name: 'ChangelogNotification',
  computed: {
    hasUnseenVersions() {
      if (this.$store.state.module_app.versionSeen === null) {
        return true;
      }

      return compareVersions(this.$store.state.module_app.versionSeen, this.$store.state.module_app.version) === -1;
    },
  },
};
</script>
