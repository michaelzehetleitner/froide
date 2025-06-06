<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  dialogClasses: {
    type: String,
    default: ''
  },
  contentClasses: {
    type: String,
    default: ''
  },
  bodyClasses: {
    type: String,
    default: ''
  },
  keepAlive: Boolean
})

const modalEl = ref()
let bsModal

// Current behavior is "keep-alive"-ish:
// modal markup will be rendered on first show,
// then hidden, not unmounted.
// Consider using a v-model here...
const doRender = ref(false)

const show = async () => {
  if (!doRender.value) {
    doRender.value = true
    await nextTick()
    initialize()
  }
  bsModal.show()
}

const hide = () => {
  bsModal.hide()
  if (!props.keepAlive) {
    doRender.value = false
  }
}

const initialize = () => {
  bsModal = new Modal(modalEl.value)
}

onMounted(() => {
  if (props.showOnMounted) {
    show()
  }
})

defineExpose({
  show,
  hide
})
</script>

<template>
  <Teleport to="body">
    <div
      ref="modalEl"
      class="modal"
      tabindex="-1"
      role="dialog"
      v-if="doRender"
    >
      <div :class="'modal-dialog ' + dialogClasses" role="document">
        <div :class="'modal-content ' + contentClasses">
          <div class="modal-header">
            <div class="text-break">
              <slot name="header"></slot>
            </div>
            <button
              @click="hide"
              type="button"
              class="btn-close"
              aria-label="Close"
            ></button>
          </div>
          <div :class="'modal-body ' + bodyClasses">
            <slot name="body"></slot>
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
