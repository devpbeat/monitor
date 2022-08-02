<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-purpleaca">
      <q-toolbar>
        <q-btn flat dense round @click="onClickDrawer" icon="menu" aria-label="Menu" />
        <q-toolbar-title class="items-center text-center">
          {{
              statusLabelSelected === ""
                ? "Panel de control"
                : `${statusLabelSelected}`
          }}
        </q-toolbar-title>
        <q-space />
        <q-btn @click="onClickRefresh" round dense flat color="white" icon="refresh">
        </q-btn>
      </q-toolbar>
    </q-header>
    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="text-gray bg-grey-2">
      <q-list>
        <q-item class="items-center">
          <q-item-label>Menu</q-item-label>
        </q-item>
        <q-item :to="{ name: 'status' }" active-class="q-item-link-highlighting">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Inicio</q-item-label>
          </q-item-section>
        </q-item>
        <q-expansion-item icon="storage" label="Datos de servicios en AWS">
          <q-item clickable v-for="(item, label) in aws_data" @click="onClickStatus(item, label)" class="q-ml-xl"
            active-class="q-item-no-link-highlighting">
            <q-item-section>
              <q-item-label>{{ label }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>
    <q-page-container class="bg-grey-2">
      <Status :items="statusItemSelected" />
      <q-dialog v-model="error">
        <!-- error -->
        <q-card>
          <q-card-section>
            <div class="text-h6">Alert</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet
            porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro
            labore.
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, toRaw } from "vue";

import { spider_repository } from "src/data/repository/spider_repository";

import Status from "pages/Status.vue";

import { structure_aws_data_card } from "src/helpers/aws_raw_to_card_social";

export default defineComponent({
  name: "MainLayout",

  components: { Status },

  setup() {
    const leftDrawerOpen = ref(false);

    const aws_data = ref({});

    const statusLabelSelected = ref("");

    const statusItemSelected = ref({});

    let count = 0;

    (() => {
      spider_repository.get_aws_data().then((response) => {
        aws_data.value = response.data;
        const dataRaw = toRaw(aws_data.value);
        var arrayLabels = Object.keys(dataRaw);
        var size = arrayLabels.length;
        if (size > 1) {
          const label = arrayLabels[count];
          const item = dataRaw[arrayLabels[count]];
          statusItemSelected.value = toRaw(item).map((value) => {
            return structure_aws_data_card(
              value,
              "computer",
              "#fff",
              "#3e51b5"
            );
          });
          statusLabelSelected.value = label;
        }
      });
    })();

    setInterval(() => {
      spider_repository.get_aws_data().then((response) => {
        aws_data.value = response.data;
      });
    }, 60000 * 5);

    setInterval(() => {
      const dataRaw = toRaw(aws_data.value);
      var arrayLabels = Object.keys(dataRaw);
      var size = arrayLabels.length;
      if (count < size) {
        const label = arrayLabels[count];
        const item = dataRaw[arrayLabels[count]];
        statusItemSelected.value = toRaw(item).map((value) => {
          return structure_aws_data_card(value, "computer", "#fff", "#3e51b5");
        });
        statusLabelSelected.value = label;
        count++;
      } else {
        count = 0;
      }
    }, 60000 * 1);

    return {
      error: false,
      leftDrawerOpen,
      aws_data,
      statusLabelSelected,
      statusItemSelected,
      onClickDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      onClickRefresh() {
        spider_repository.get_aws_data().then((response) => {
          aws_data.value = response.data;
        });
      },
      onClickStatus: (item, label) => {
        const data = toRaw(item).map((value) => {
          return structure_aws_data_card(value, "computer", "#fff", "#3e51b5");
        });
        statusItemSelected.value = data;
        statusLabelSelected.value = label;
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
});
</script>
<style lang="sass">
.bg-purpleaca
  background-color: #831F82 !important
</style>
