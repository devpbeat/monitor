<template>
  <q-page class="q-pa-sm bg-purpleacalight">
    <div v-for="item in items">
      <card-social :item="item" />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

import CardSocial from "components/cards/CardSocial.vue";

export default defineComponent({
  name: "Status",
  props: ["items"],
  components: {
    CardSocial,
  },
});
</script>

<style scoped></style>
