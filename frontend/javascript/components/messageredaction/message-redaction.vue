<template>
  <div>
    <template v-if="message">
      <div v-if="message.subject" class="row mb-3">
        <div class="col-md-3">
          <h5>{{ i18n.subject }}</h5>
        </div>
        <div class="col-md-9">
          <MessageRedactionField
            field-name="subject"
            :redacted-parts="
              message.redacted_subject
            "></MessageRedactionField>
        </div>
      </div>
      <div v-if="message.content" class="mb-3">
        <h5>
          {{ i18n.message }}
        </h5>
        <div>
          <MessageRedactionField
            field-name="content"
            :redacted-parts="message.redacted_content"
            :blocked-patterns="
              config.settings.blockedPatterns
            "></MessageRedactionField>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="text-center">
        <h3>
          {{ i18n.messageLoading }}
        </h3>
        <div class="spinner-border" role="status"></div>
      </div>
    </template>
  </div>
</template>

<script>
import { getData } from '../../lib/api.js'

import MessageRedactionField from './message-redaction-field.vue'

export default {
  name: 'MessageRedaction',
  props: {
    config: {
      type: Object,
      required: true
    },
    messageUrl: {
      type: String,
      required: true
    }
  },
  components: {
    MessageRedactionField
  },
  provide() {
    return {
      config: this.config
    }
  },
  data() {
    return {
      message: null
    }
  },
  created() {
    getData(this.messageUrl).then((message) => {
      this.message = message
    })
  },
  computed: {
    i18n() {
      return this.config.i18n
    }
  }
}
</script>
