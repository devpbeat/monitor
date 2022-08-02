<template>
  <q-card class="bg-transparent no-shadow no-border">
    <q-card-section class="q-pa-sm">
      <div class="row q-col-gutter-sm">
        <div class="col-md-12 col-sm-12 col-xs-12">
          <q-item class="q-pa-none">
            <q-item-section
              :style="`background-color: ${item.color1}`"
              class="q-pa-md q-ml-none text-custom-color"
            >
              <q-item-label
                class="text-custom-color text-h6 text-weight-bolder"
                >{{ item.value }}</q-item-label
              >
              <q-item-label>{{ item.title }}</q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "CardSocial",
  props: ["item"],
  setup() {},
});
</script>

<style lang="sass">
.text-custom-color
    color: #9C27B0 !important
</style>
