<script setup lang="ts">
import { computed } from 'vue'
import { ChevronDown, CircleDot } from 'lucide-vue-next'
import { time, titleCase } from '../learning'
import type { PivotField } from '../cases'
import type { EventRecord } from '../types'

const props = defineProps<{ events: EventRecord[]; pivots?: boolean }>()
const emit = defineEmits<{ pivot: [field: PivotField, value: string] }>()
const ordered = computed(() => [...props.events].sort((a, b) => Date.parse(a.event_timestamp) - Date.parse(b.event_timestamp)))
const optional = ['process', 'parent_process', 'command_line', 'source_ip', 'destination_ip', 'domain', 'url'] as const
</script>

<template>
  <ol class="timeline" aria-label="Evidence timeline in UTC">
    <li v-for="event in ordered" :key="event.record_id" :class="{ matched: event.alert_id }">
      <CircleDot class="timeline-dot" :size="17" aria-hidden="true" />
      <details>
        <summary>
          <time :datetime="event.event_timestamp">{{ time(event.event_timestamp) }} UTC</time>
          <span class="timeline-action">{{ titleCase(event.action) }}</span>
          <span class="event-result">{{ titleCase(event.outcome) }}</span>
          <span v-if="event.alert_id" class="evidence-label">Alert evidence</span>
          <ChevronDown class="expand-icon" :size="16" aria-hidden="true" />
        </summary>
        <dl class="event-fields">
          <div><dt>Source</dt><dd>{{ event.source }}</dd></div>
          <div><dt>Actor</dt><dd>{{ event.user ?? 'Unknown' }}</dd></div>
          <div><dt>Host / service</dt><dd>{{ event.host }}</dd></div>
          <div><dt>Event ID</dt><dd>{{ event.event_id }}</dd></div>
          <template v-for="key in optional" :key="key">
            <div v-if="event[key]"><dt>{{ titleCase(key) }}</dt><dd>{{ event[key] }}</dd></div>
          </template>
          <div v-for="(value, key) in event.observables" :key="key"><dt>{{ titleCase(key) }}</dt><dd>{{ value }}</dd></div>
          <div class="evidence-reference"><dt>Evidence reference</dt><dd><code>{{ event.evidence_reference }}</code></dd></div>
          <div v-if="event.alert_id"><dt>Alert ID</dt><dd><code>{{ event.alert_id }}</code></dd></div>
        </dl>
        <div v-if="pivots" class="actions evidence-pivots">
          <button class="button secondary" @click="emit('pivot', 'host', event.host)">Pivot by host</button>
          <button v-if="event.user" class="button secondary" @click="emit('pivot', 'user', event.user)">Pivot by actor</button>
          <button class="button secondary" @click="emit('pivot', 'source', event.source)">Pivot by source</button>
        </div>
      </details>
    </li>
  </ol>
</template>
