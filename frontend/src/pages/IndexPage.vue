<template>
  <q-page class="flex flex-center bg-purpleaca">
    <div class="row">
      <q-btn
        color="orange"
        icon="contactless"
        label="Status"
        :to="{ name: 'status' }"
      />
      <q-btn
        color="orange"
        icon="attach_money"
        label="Credits"
        :to="{ name: 'credits' }"
      />
      <q-btn color="orange" icon="check" label="Test" :to="{ name: 'index' }" />
      <q-btn
        color="orange"
        icon="bar_chart"
        label="Chart"
        :to="{ name: 'chart' }"
      />
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { useInfoStore } from "src/stores/info";

export default defineComponent({
  name: "IndexPage",
  setup() {
    const infoStore = useInfoStore();
    infoStore.title = "Index";
    return {};
  },
});
</script>

<style lang="sass"></style>
