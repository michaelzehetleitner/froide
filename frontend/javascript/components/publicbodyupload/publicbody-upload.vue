<template>
  <div class="publicbody-upload mb-3 mt-3">
    <div class="text-end mt-3">
      <button
        v-if="canSubmit"
        type="submit"
        class="btn btn-lg btn-primary"
        @click="submitting = true">
        <span
          v-if="uploading"
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true" />
        {{ i18n.createResponse }}
      </button>
    </div>
    <FileUploader
      :config="config"
      class="mb-3 mt-3"
      :auto-proceed="true"
      :allow-remove="false"
      :required="true"
      @ready="canSubmit = $event"
      @uploading="uploading = $event" />
    <div class="text-end mt-3">
      <button
        type="submit"
        class="btn btn-lg btn-primary"
        :disabled="!canSubmit"
        @click="submitting = true">
        <span
          v-if="uploading"
          class="spinner-border spinner-border-sm"
          role="status"
          aria-hidden="true" />
        {{ i18n.createResponse }}
      </button>
    </div>
  </div>
</template>

<script>
import FileUploader from '../upload/file-uploader.vue'

import I18nMixin from '../../lib/i18n-mixin'

export default {
  name: 'PublicbodyUpload',
  components: {
    FileUploader
  },
  mixins: [I18nMixin],
  props: {
    config: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      canSubmit: false,
      uploading: false,
      submitting: false
    }
  },
  mounted() {
    window.addEventListener('beforeunload', (e) => {
      if (!this.canSubmit && !this.uploading) {
        return
      }
      if (this.submitting) {
        return
      }
      // If you prevent default behavior in Mozilla Firefox prompt will always be shown
      e.preventDefault()
      // Chrome requires returnValue to be set
      e.returnValue = this.i18n.sureCancel
      return e.returnValue
    })
  }
}
</script>
