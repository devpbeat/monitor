<template>
  <q-page>
    <div class="fit">
      <div class="row half">
        <div class="col-8">
          <PortalTarget name="big"></PortalTarget>
        </div>
        <div class="col-4">
          <div class="half">
            <PortalTarget name="medium1"> </PortalTarget>
            <PortalTarget name="medium2"> </PortalTarget>
          </div>
        </div>
      </div>

      <div class="row half">
        <div class="col-3">
          <PortalTarget name="small1"> </PortalTarget>
        </div>
        <div class="col-3">
          <PortalTarget name="small2"> </PortalTarget>
        </div>
        <div class="col-3">
          <PortalTarget name="small3"> </PortalTarget>
        </div>
        <div class="col-3">
          <PortalTarget name="small4"> </PortalTarget>
        </div>
      </div>
    </div>

    <CardInfo v-for="detail in details" :key="detail.title" v-bind="detail" />
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { details } from "../helpers/credits";
import CardInfo from "src/components/CardInfo";
import { PortalTarget } from "portal-vue";
import { useInfoStore } from "src/stores/info";
export default defineComponent({
  name: "Credits",
  components: { CardInfo, PortalTarget },

  setup() {
    const infoStore = useInfoStore();
    infoStore.title = "Credits";
    return {
      details,
    };
  },
});
</script>

<style lang="sass" scoped>
.q-page
  background-color: #831F82

.medium
  width: 100%

.fit
  position: absolute
  top:0px
  right:0px
  bottom:0px
  left:0px


.half
  height: 50%
</style>
