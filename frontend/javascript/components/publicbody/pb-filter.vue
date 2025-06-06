<template>
  <div class="filter-component">
    <h5 @click="toggleExpand" class="filter-heading">
      {{ config.label }}&nbsp;<i
        class="fa expand-icon"
        :class="{
          'fa-chevron-down': !expanded,
          'fa-chevron-up': expanded
        }"></i>
    </h5>
    <transition name="expand">
      <div v-show="expanded" class="filter-container">
        <select
          v-if="hasChoices"
          v-model="choice"
          @change="triggerSearch"
          class="form-select">
          <option
            v-for="opt in config.choices[1]"
            :key="opt[0]"
            :value="opt[0]"
            :selected="choice == opt[0]">
            {{ opt[1] }}
          </option>
        </select>
        <input
          v-if="hasSearch"
          type="search"
          class="form-control form-control-sm"
          :placeholder="i18n.searchPlaceholder"
          v-model="search"
          @keyup="triggerSearch"
          @keydown.enter.prevent="triggerSearch" />
        <div class="filter-list-container">
          <div
            v-if="loading"
            class="spinner-border text-secondary"
            role="status">
            <span class="visually-hidden">{{ i18n.loading }}</span>
          </div>
          <PbFilterList
            v-else
            :config="config"
            :i18n="i18n"
            :scope="scope"
            :has-more="hasMore"
            :items="orderedItems"
            :value="value"
            @remove-filter="removeFilter"
            @set-filter="setFilter"
            @load-more="loadMore"
            @load-children="loadChildren"></PbFilterList>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import debounce from 'lodash.debounce'

import { FroideAPI } from '../../lib/api'
import FilterMixin from './lib/filter-mixin'

import PbFilterList from './pb-filter-list'

export default {
  name: 'PbFilter',
  props: ['globalConfig', 'config', 'i18n', 'scope', 'value', 'expanded'],
  mixins: [FilterMixin],
  components: { PbFilterList },
  data() {
    let choice = null
    if (this.config.choices) {
      choice = this.config.choices[1][0][0]
    }
    return {
      items: [],
      search: '',
      choice,
      lastSearch: null,
      searchMeta: null,
      loading: false
    }
  },
  mounted() {
    this.runSearch()
  },
  computed: {
    hasSearch() {
      return this.config.hasSearch
    },
    hasChoices() {
      return this.config.choices
    },
    triggerSearch() {
      return debounce(this.runSearch, 300)
    },
    facetMap() {
      const facets = this.getScopedSearchFacets(this.scope)
      if (!facets) {
        return null
      }
      const counts = facets[this.config.key]
      if (counts) {
        const facetMap = {}
        counts.forEach((x) => {
          facetMap[x[0]] = x[1]
        })
        return facetMap
      }
      return null
    },
    orderedItems() {
      let items = this.items
      if (this.facetMap) {
        const applyFacetMap = function (facetMap, items) {
          return items.map((x) => {
            x.count = facetMap[x.id]
            if (x.subItems) {
              x.subItems = applyFacetMap(facetMap, x.subItems)
            }
            return x
          })
        }
        items = applyFacetMap(this.facetMap, items)
      }
      return items
    },
    searcher() {
      const searcher = new FroideAPI(this.globalConfig)
      return searcher
    },
    ...mapGetters(['getScopedSearchFacets'])
  },
  methods: {
    toggleExpand() {
      this.$emit('setFilterExpand', this.config, !this.expanded)
    },
    removeCurrentFilter(e) {
      e.preventDefault()
      this.removeFilter(this.value)
    },
    runSearch() {
      let filters = {}
      if (this.search === '') {
        filters = {
          ...filters,
          ...this.config.initialFilters
        }
      }
      if (this.config.choices && this.choice) {
        filters[this.config.choices[0]] = this.choice
      }
      const searchDump = JSON.stringify({
        q: this.search,
        ...filters
      })
      if (this.lastSearch === searchDump) {
        return
      }
      this.items = []
      this.lastSearch = searchDump
      this.loading = true
      this.getItems(this.search, filters)
    },
    getItems(q, filters) {
      this.search = q
      this.config.getItems(q, filters).then((result) => {
        this.searchMeta = result.meta
        this.loading = false
        this.items = this.processItems(result.objects)
      })
    },
    processItems(items) {
      if (this.config.itemFilter) {
        items = items.filter(this.config.itemFilter)
      }
      if (this.config.itemMap) {
        items = items.map(this.config.itemMap)
      }
      return items
    },
    loadMore() {
      if (!this.searchMeta) {
        return
      }
      if (!this.searchMeta.next) {
        return
      }
      this.searcher.getJson(this.searchMeta.next).then((result) => {
        this.searchMeta = result.meta
        this.items = [...this.items, ...this.processItems(result.objects)]
      })
    },
    loadChildren(item) {
      this.config.getItems(null, { parent: item.id }).then((result) => {
        const items = this.processItems(result.objects)
        item.subItems = items
      })
    },
    setFilter(item) {
      if (this.config.multi) {
        let val
        if (!this.value) {
          val = [item]
        } else if (!this.value.some((x) => item.id === x.id)) {
          val = [...this.value, item]
        }
        if (val) {
          this.$emit('update', this.config, val)
        }
      } else {
        this.$emit('update', this.config, item)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../../styles/variables';
.filter-heading {
  font-size: 0.9em;
  cursor: pointer;
}
.expand-icon {
  cursor: pointer;
  font-size: 0.8em;
}

.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.5s;
}
.expand-enter,
.expand-leave-to {
  opacity: 0;
  .filter-list-container {
    max-height: 0;
  }
}

@include media-breakpoint-only(sm) {
  .filter-heading {
    cursor: default;
    pointer-events: none;
  }
  .expand-icon {
    display: none;
  }
  .filter-container {
    display: block !important;
  }
}

.filter-list-container {
  transition: max-height 0.5s ease-in-out;
  padding: 5px;
  max-height: 200px;
  overflow-y: auto;
  position: relative;

  @include media-breakpoint-up(md) {
    max-height: 320px;
  }
}
.filter-container:after {
  content: ' ';
  pointer-events: none;
  position: absolute;
  left: 0;
  height: 3em;
  bottom: 0em;
  width: 100%;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0),
    rgba(var(--#{$prefix}body-bg-rgb), 0.95) 50%
  );
  z-index: 1;
}
</style>
