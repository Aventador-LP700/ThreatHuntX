<script setup lang="ts">
import { computed } from 'vue'
import { Search } from 'lucide-vue-next'
import type { EventFilter } from '../cases'
import type { EventRecord } from '../types'

const props = defineProps<{ events: EventRecord[] }>()
const filters = defineModel<EventFilter>({ required: true })
const fields = ['host', 'user', 'source', 'outcome'] as const
const labels = { host: 'Host or service', user: 'Actor', source: 'Source', outcome: 'Outcome' }
const options = computed(() => Object.fromEntries(fields.map(field => [field,
  [...new Set(props.events.map(event => event[field]).filter((value): value is string => Boolean(value)))].sort(),
])))
</script>

<template>
  <div class="evidence-filters">
    <label class="search-field"><Search :size="17" aria-hidden="true" /><span class="sr-only">Search event fields</span><input v-model="filters.text" type="search" placeholder="Search evidence, record ID, or observable" /></label>
    <div class="filters-grid"><label v-for="field in fields" :key="field" class="field">{{ labels[field] }}<select v-model="filters[field]"><option value="">Any</option><option v-for="value in options[field]" :key="value">{{ value }}</option></select></label></div>
  </div>
</template>
