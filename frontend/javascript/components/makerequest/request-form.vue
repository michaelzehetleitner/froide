<template>
  <div>
    <slot name="request-legend-title" />

    <div
      v-if="multiRequest && canBatchRequest"
      class="publicbody-summary-container">
      <div class="publicbody-summary">
        <p>
          <template v-if="publicBodies.length < 20">
            <ul>
              <li v-for="pb in publicBodies" :key="pb.id">
                {{ pb.name }}
                <div v-if="pb.request_note_html" class="col-lg-8 alert alert-warning pb-0" v-html="pb.request_note_html" />
              </li>
            </ul>
          </template>
          <template v-else>
            {{ i18n._('toMultiPublicBodies', { count: publicBodies.length }) }}
          </template>
          <span v-if="!hidePublicbodyChooser">
            <a
              class="pb-change-link badge rounded-pill text-bg-primary ms-3"
              :href="config.url.makeRequest"
              @click.prevent="$emit('setStepSelectPublicBody')">
              {{ i18n.change }}
            </a>
          </span>
        </p>
      </div>
    </div>
    <div v-if="multiRequest && !canBatchRequest" class="mb-5 mt-5">
      <p>{{ i18n._('toMultiPublicBodies', { count: publicBodies.length }) }}</p>
      <div class="publicbody-summary-list">
        <ul>
          <li v-for="pb in publicBodies" :key="pb.id">
            {{ pb.name }}
          </li>
        </ul>
      </div>
      <small>{{ i18n.batchRequestDraftOnly }}</small>
    </div>

    <div v-if="!multiRequest" class="publicbody-summary-container">
      <div class="row">
        <div class="col-lg-12 publicbody-summary">
          <p>
            {{ i18n._('toPublicBody', { name: publicBody.name }) }}
            <a :href="publicBody.site_url" target="_blank">
              <span class="fa fa-info-circle" />
            </a>
            <span v-if="!hidePublicbodyChooser">
              <a
                class="pb-change-link badge rounded-pill text-bg-primary ms-3"
                :href="config.url.makeRequest"
                @click.prevent="$emit('setStepSelectPublicBody')">
                {{ i18n.change }}
              </a>
            </span>
          </p>
        </div>
      </div>
      <div v-if="hasLawNotes" class="row">
        <div class="col-lg-8">
          <div class="alert alert-warning" v-html="lawNotes" />
        </div>
      </div>
      <div v-if="hasPublicBodyNotes" class="row">
        <div class="col-lg-8">
          <div class="alert alert-warning" v-html="publicBodyNotes" />
        </div>
      </div>
    </div>

    <input
      v-for="pb in publicBodies"
      :key="pb.id"
      type="hidden"
      name="publicbody"
      :value="pb.id" />
    <input type="hidden" name="law_type" :value="lawType" />

    <div class="row">
      <div class="col-md-12">
        <div v-if="nonFieldErrors.length > 0" class="alert alert-danger">
          <p v-for="error in nonFieldErrors" :key="error" v-html="error" />
        </div>

        <div class="mb-3">
          <label
            class="form-check-label"
            for="id_request_type"
            :class="{ 'text-danger': errors.request_type }">
            {{ i18n.subject }}
          </label>
          <div
            v-if="
              editingDisabled && !(errors.request_type && errors.request_type.length > 0)
            ">
            <input type="hidden" name="request_type" :value="request_type" />
            <strong>{{ request_type }}</strong>
            <button
              class="btn btn-sm btn-white float-end"
              @click.prevent="editingDisabled = false">
              <small class="d-none d-md-block">{{ i18n.reviewEdit }}</small>
              <small class="d-md-none fa fa-edit">
                <span class="visually-hidden">{{ i18n.reviewEdit }}</span>
              </small>
            </button>
          </div>
          <template v-else>
            <div
              v-if="errors.request_type && errors.request_type.length > 0"
              class="alert alert-danger">
              <p v-for="error in errors.request_type" :key="error.message">
                {{ error.message }}
              </p>
            </div>
            <div v-if="!isMeaningfulSubject" class="alert alert-warning">
              {{ i18n.enterMeaningfulSubject }}
            </div>
            <select
              id="id_request_type"
              v-model="request_type"
              name="request_type"
              class="form-select"
              :class="{ 'is-invalid': errors.request_type }">
              <option
                v-for="choice in formFields.request_type.choices"
                :key="choice.value"
                :value="choice.value">
                {{ choice.label }}
              </option>
            </select>
          </template>
        </div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-body">
        <div v-if="fullText && warnFullText" class="alert alert-warning">
          <p>
            {{ i18n.warnFullText }}
          </p>
        </div>
        <div class="row">
          <div v-if="!editingDisabled" class="col-md-4 order-md-2">
            <transition name="saved-full-text">
              <div v-if="savedFullTextBody">
                <h6>
                  {{ i18n.savedFullTextChanges }}
                </h6>
                <textarea
                  v-model="savedFullTextBody"
                  class="saved-body"
                  readonly />
              </div>
            </transition>
            <slot name="request-hints" />
            <div
              v-if="submitting && bodyCustomErrors.length > 0"
              class="alert alert-warning">
              <ul class="list-unstyled">
                <li v-for="error in bodyCustomErrors" :key="error">
                  {{ error }}
                </li>
              </ul>
            </div>
            <button
              v-if="fullTextDisabled"
              class="btn btn-outline-secondary btn-sm"
              @click.prevent="resetFullText">
              {{ i18n.resetFullText }}
            </button>
          </div>
          <div class="col-md-8 order-1">
            <div
              v-if="errors.body && errors.body.length > 0"
              class="alert alert-danger">
              <p v-for="error in errors.body" :key="error.message">
                {{ error.message }}
              </p>
            </div>
            <div v-if="!fullText" class="body-text" v-text="letterStart" />
            <div v-if="editingDisabled" class="body-text-em" v-text="body" />
            <textarea
              v-show="!editingDisabled"
              id="id_body"
              v-model="body"
              minlength="8"
              name="body"
              ref="body"
              class="form-control body-textarea"
              :class="{ 'is-invalid': errors.body, attention: !hasBody }"
              :rows="bodyRows"
              :placeholder="formFields.body.placeholder"
              required
              @keyup="bodyChanged" />
            <div
              v-if="allowFullText && !editingDisabled"
              class="form-check form-check-inline float-end">
              <input
                id="full_text_checkbox"
                class="form-check-input"
                v-model="fullText"
                type="checkbox"
                name="full_text_checkbox"
                :disabled="fullTextDisabled" />
              <label
                for="full_text_checkbox"
                class="form-check-label small text-body-secondary">
                <i
                  v-if="warnFullText"
                  class="fa fa-exclamation-triangle"
                  aria-hidden="true" />
                {{ formFields.full_text.label }}
              </label>
            </div>
            <input v-model="fullText" type="hidden" name="full_text" />
            <div v-if="!fullText" class="body-text">
              <template v-if="!fullLetter">
                <a
                  class="show-full-letter"
                  href="#"
                  @click.prevent="showFullLetter"
                  v-text="'[…]'" />
                <template v-if="true">{{ letterEndShort }}</template>
              </template>
              <template v-else>{{ letterEnd }}</template>
            </div>
            <div v-if="letterSignature" class="body-text">
              <em>{{ letterSignature }}</em>
            </div>
            <div
              v-if="!letterSignature && fullText"
              class="body-text"
              v-text="letterSignatureName" />
          </div>
        </div>
        <div v-if="!hasUser" class="row">
          <div class="col-md-8">
            <div class="mb-3 row">
              <div
                class="col-sm-6"
                :class="{ 'text-danger': usererrors.first_name }">
                <label
                  class="form-label field-required"
                  for="id_first_name"
                  :class="{ 'text-danger': usererrors.first_name }">
                  {{ i18n.yourFirstName }}
                </label>
                <input
                  id="id_first_name"
                  v-model="first_name"
                  type="text"
                  name="first_name"
                  class="form-control"
                  :class="{ 'is-invalid': usererrors.first_name }"
                  :placeholder="userformFields.first_name.placeholder"
                  required />
                <p v-for="e in usererrors.first_name" :key="e.message">
                  {{ e.message }}
                </p>
              </div>

              <div
                class="col-sm-6"
                :class="{ 'text-danger': usererrors.last_name }">
                <label
                  class="form-label field-required"
                  for="id_last_name"
                  :class="{ 'text-danger': usererrors.last_name }">
                  {{ i18n.yourLastName }}
                </label>
                <input
                  id="id_last_name"
                  v-model="last_name"
                  type="text"
                  name="last_name"
                  class="form-control"
                  :class="{ 'is-invalid': usererrors.last_name }"
                  :placeholder="userformFields.last_name.placeholder"
                  required />
                <p v-for="e in usererrors.last_name" :key="e.message">
                  {{ e.message }}
                </p>
              </div>
            </div>
          </div>
          <div v-if="usePseudonym" class="col-md-4 mt-md-4">
            <small
              v-if="userformFields.last_name.help_text"
              v-html="userformFields.last_name.help_text" />
          </div>
        </div>

        <div
          v-if="config.settings.user_can_hide_web && !hasUser"
          class="row mt-2">
          <div class="col-md-8">
            <div class="form-check">
              <input
                id="id_private"
                class="form-check-input"
                v-model="userPrivate"
                type="checkbox"
                name="private" />
              <label for="id_private" class="form-check-label">
                {{ userformFields.private.label }}
              </label>
              <p class="help-block" v-html="userformFields.private.help_text" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="hasUser && proofForm" class="card mb-3">
      <div class="card-body">
        <div class="row">
          <div class="col-lg-8 col-md-10">
            <template v-if="proofRequired">
              <h5>{{ i18n.includeProof }}</h5>
              <ProofForm
                :form="proofForm"
                :required="proofRequired"
                :config="config.proof_config"></ProofForm>
            </template>
            <details v-else>
              <summary>{{ i18n.includeProof }}</summary>
              <ProofForm
                :form="proofForm"
                :required="proofRequired"
                :config="config.proof_config"></ProofForm>
            </details>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LetterMixin from './lib/letter-mixin'
import I18nMixin from '../../lib/i18n-mixin'

import ProofForm from '../proofupload/proof-form.vue'

const PLACEHOLDER_MARKER = '…'
const MAX_BODY_ROWS = 12
const MIN_BODY_ROWS = 3

export default {
  name: 'RequestForm',
  mixins: [I18nMixin, LetterMixin],
  components: {
    ProofForm
  },
  props: {
    config: {
      type: Object
    },
    publicbodies: {
      type: Array,
      default: null
    },
    user: {
      type: Object,
      default: null
    },
    defaultLaw: {
      type: Object,
      default: null
    },
    requestForm: {
      type: Object
    },
    userForm: {
      type: Object
    },
    lawType: {
      type: String,
      default: ''
    },
    showDraft: {
      type: Boolean,
      default: false
    },
    hidePublicbodyChooser: {
      type: Boolean,
      default: false
    },
    hideFullText: {
      type: Boolean,
      default: true
    },
    hideEditing: {
      type: Boolean,
      default: false
    },
    multiRequest: {
      type: Boolean,
      default: false
    },
    usePseudonym: {
      type: Boolean,
      default: true
    },
    initialSubject: {
      type: String,
      default: ''
    },
    initialBody: {
      type: String,
      default: ''
    },
    initialFullText: {
      type: Boolean,
      default: false
    },
    initialFirstName: {
      type: String,
      default: ''
    },
    initialLastName: {
      type: String,
      default: ''
    },
    proofForm: {
      type: Object,
      default: null
    },
    proofRequired: {
      type: Boolean,
      default: false
    },
    submitting: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      bodyRows: MIN_BODY_ROWS,
      bodyBeforeChange: '',
      bodyCustomErrors: [],
      savedFullTextBody: '',
      fullTextDisabled: false,
      editingDisabled: this.hideEditing,
      fullLetter: false,
      requestTypeValue: this.initialSubject || '',
      bodyValue: this.initialBody || '',
      fullTextValue: this.initialFullText,
      firstNameValue:
        this.initialFirstName || (this.user && this.user.first_name) || '',
      lastNameValue:
        this.initialLastName || (this.user && this.user.last_name) || '',
      privateValue:
        this.initialPrivate || (this.user && this.user.private) || false
    }
  },
  computed: {
    nonFieldErrors() {
      return this.form.nonFieldErrors
    },
    form() {
      return this.requestForm
    },
    formFields() {
      return this.form.fields
    },
    errors() {
      return this.form.errors
    },
    userformFields() {
      return this.userForm.fields
    },
    usererrors() {
      return this.userForm.errors
    },
    hasLawNotes() {
      if (this.defaultLaw) {
        return !!this.defaultLaw.request_note_html
      }
      // FIXME: find all notes of all public body default laws?
      return false
    },
    hasPublicBodyNotes() {
      if (this.publicBody) {
        return !!this.publicBody.request_note_html
      }
      // FIXME: find all notes of all public body default laws?
      return false
    },
    lawNotes() {
      if (this.hasLawNotes) {
        return this.defaultLaw.request_note_html
      }
      return ''
    },
    publicBodyNotes() {
      if (this.hasPublicBodyNotes) {
        return this.publicBody.request_note_html
      }
      return ''
    },
    canBatchRequest() {
      return this.config.settings.user_can_create_batch
    },
    nonMeaningfulSubjects() {
      return this.config.settings.non_meaningful_subject_regex.map(
        (x) => new RegExp(x, 'i')
      )
    },
    hasUser() {
      return this.user && this.user.id
    },
    request_type: {
      get() {
        return this.requestTypeValue
      },
      set(value) {
        this.requestTypeValue = value
        this.$emit('update:initialSubject', value)
      }
    },
    hasBody() {
      return this.body && this.body.length > 0
    },
    body: {
      get() {
        return this.bodyValue
      },
      set(value) {
        this.bodyValue = value
        this.$emit('update:initialBody', value)
      }
    },
    allowFullText() {
      return this.hasUser && !this.hideFullText
    },
    warnFullText() {
      return this.allowFullText && this.multipleLaws
    },
    multipleLaws() {
      return this.defaultLaw === null
    },
    fullText: {
      get() {
        return this.fullTextValue
      },
      set(value) {
        this.fullTextValue = value
        this.$emit('update:initialFullText', value)
        if (value) {
          this.bodyBeforeChange = this.body
          this.body = `${this.letterStart}\n${this.body}\n\n${this.letterEndNoName}`
        } else {
          if (!this.fullTextDisabled) {
            this.body = this.bodyBeforeChange
          }
        }
        const newLineCount = (this.body.match(/\n/g) || []).length
        this.bodyRows = Math.max(
          MIN_BODY_ROWS,
          Math.min(newLineCount + 1, MAX_BODY_ROWS)
        )
      }
    },
    first_name: {
      get() {
        return this.firstNameValue
      },
      set(value) {
        this.firstNameValue = value
        this.$emit('update:initialFirstName', value)
      }
    },
    last_name: {
      get() {
        return this.lastNameValue
      },
      set(value) {
        this.lastNameValue = value
        this.$emit('update:initialLastName', value)
      }
    },
    userPrivate: {
      get() {
        return this.privateValue
      },
      set(value) {
        this.privateValue = value
        this.$emit('update:initialPrivate', value)
      }
    },
    hasPublicBodies() {
      return this.publicBodies.length > 0
    },
    publicBody() {
      return this.publicbodies[0]
    },
    publicBodies() {
      // FIXME
      return this.publicbodies
    },
    isMeaningfulSubject() {
      for (const re of this.nonMeaningfulSubjects) {
        if (re.test(this.request_type)) {
          return false
        }
      }
      return true
    }
  },
  mounted() {
    this.bodyChanged()
    this.populateBodyFromRequestType()
  },
  watch: {
    request_type() {
      this.populateBodyFromRequestType()
    }
  },
  methods: {
    resetFullText() {
      this.savedFullTextBody = this.body
      this.fullTextDisabled = false
      this.fullText = false
    },
    bodyChanged() {
      if (this.fullText) {
        this.fullTextDisabled = true
      }
      const ta = this.$refs.body
      while (ta.scrollHeight > ta.clientHeight && ta.rows < MAX_BODY_ROWS) {
        ta.style.overflow = 'hidden'
        ta.rows += 1
      }
      if (ta.scrollHeight > ta.clientHeight) {
        ta.style.overflow = 'auto'
      }
      this.bodyRows = ta.rows
      if (this.body.includes(PLACEHOLDER_MARKER)) {
        this.bodyCustomErrors = [this.i18n.replacePlaceholderMarker]
        ta.setCustomValidity(this.i18n.replacePlaceholderMarker)
      } else {
        this.bodyCustomErrors = []
        ta.setCustomValidity('')
      }
    },
    populateBodyFromRequestType() {
      if (
        this.config.request_body_map &&
        this.config.request_body_map[this.request_type]
      ) {
        this.body = this.config.request_body_map[this.request_type]
      }
    },
    showFullLetter() {
      this.fullLetter = true
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../../styles/variables';

.make-request-container {
  padding-bottom: 1rem;
}

.container-multi {
  /* Allow container to wider than normal to allow for more space */
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
  max-width: 1400px;
}

legend {
  padding: 2rem 0 2rem;
  font-size: 2rem;
}

.small a {
  color: $blue;
}

.request-hints {
  color: $gray-700;
  font-size: $font-size-sm;
  ul {
    padding-left: $spacer;
  }
}

.publicbody-summary-container {
  margin: 0 0 $spacer * 2;
}

.publicbody-summary {
  font-size: $font-size-lg;
}

.publicbody-summary-list {
  max-height: 5rem;
  border: 1px solid #aaa;
  overflow: auto;
}

.pb-change-link {
  font-weight: normal;
  font-size: $font-size-sm;
}

.body-text,
.body-text-em {
  hyphens: none;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #999;
}

.body-text-em {
  color: #555;
}

.body-textarea {
  width: 100%;
}

.body-textarea {
  padding-left: 0;
  margin-left: -5px;
  padding: 5px;
}
.body-textarea.attention {
  border-left: 3px solid #faa;
}

.saved-body {
  width: 100%;
  height: 5em;
}

.saved-full-text-enter-active,
.saved-full-text-leave-active {
  transition: opacity 0.5s;
}
.saved-full-text-enter,
.saved-full-text-leave-to {
  opacity: 0;
}

.show-full-letter {
  color: #999;
  text-decoration: underline;
}
</style>
