<template>
  <Portal :to="location">
    <div
      class="card text-white"
      :class="{
        danger: high,
        alert: medium,
        ok: small,
      }"
    >
      <div class="container fit">
        <div>
          <div class="shadow">{{ title }}</div>
          <br />
          <div class="small">{{ value }}</div>
          <div class="">{{ details }}</div>
        </div>
      </div>
    </div>
  </Portal>
</template>

<script>
import { defineComponent } from "vue";
import { Portal } from "portal-vue";
export default defineComponent({
  name: "CardInfo",
  components: { Portal },
  props: {
    title: {
      type: String,
      required: true,
    },

    value: {
      type: String,
      default: "",
      required: true,
    },

    details: {
      type: String,
      default: "",
    },

    high: {
      type: Boolean,
      default: false,
    },

    medium: {
      type: Boolean,
      default: false,
    },

    small: {
      type: Boolean,
      default: false,
    },

    location: {
      type: String,
      default: "small",
    },
  },
});
</script>

<style lang="sass" scoped>
.card
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2)
  transition: 0.3s
  border-radius: 20px
  border-color: #831F82
  border-style: solid
  height: 94%
  width: 100%
  padding: 10px
  font-size: 2.5em

.card:hover
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2)

.container
  margin: auto
  position: relative
  display: flex
  align-items: center
  justify-content: center

.danger
  // background-color: $red
  text-align: center
  background-color: #feae96
  background-image: linear-gradient(315deg, #feae96 0%, #fe0944 74%)


.alert
  text-align: center
  background-color: #fbb034
  background-image: linear-gradient(315deg, #fbb034 0%, #ffdd00 74%)


.ok
  // background-color: $green
  text-align: center
  background-color: #00b712
  background-image: linear-gradient(315deg, #00b712 25%, #5aff15 65%)

.centered
  text-align: center

.shadow
  text-shadow: 0.1em 0.1em 0.2em black
   font-size: calc(1rem + 1vw)

.small
  h1,
  h2,
  p
    // Font minimum, preferred and maximum value
    font-size: clamp(var(--min), var(--val), var(--max))


  // Font size variables
  h1
    --min: 2em // minimum value
    --val: 5vw // preferred value = 5% viewport width
    --max: 3em // maximum value

  h2
    --min: 1.5em /* minimum value */
    --val: 4vw /* preferred value = 4% viewport width */
    --max: 2.25em /* maximum value */

  p
    --min: 1em // minimum value
    --val: 2.5vw // preferred value = 2.5% viewport width
    --max: 1.5em // maximum value
</style>
