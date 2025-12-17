<template>
  <v-alert
    v-if="show"
    :type="type"
    :title="title"
    :text="message"
    closable
    @click:close="dismiss"
    class="error-display"
  >
    <template v-if="action" v-slot:append>
      <v-btn
        :color="type"
        variant="text"
        @click="handleAction"
        size="small"
      >
        {{ action.text }}
      </v-btn>
    </template>
  </v-alert>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  error: {
    type: [Error, String, Object],
    default: null
  },
  title: {
    type: String,
    default: 'Ошибка'
  },
  dismissible: {
    type: Boolean,
    default: true
  },
  action: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['dismiss', 'action'])

const dismissed = ref(false)

const show = computed(() => {
  return !dismissed.value && props.error
})

const type = computed(() => {
  if (props.error?.response?.status === 404) return 'warning'
  if (props.error?.response?.status === 401) return 'warning'
  if (props.error?.response?.status >= 500) return 'error'
  return 'error'
})

const message = computed(() => {
  if (!props.error) return ''
  
  if (typeof props.error === 'string') return props.error
  if (props.error.message) return props.error.message
  if (props.error.response?.data?.message) return props.error.response.data.message
  
  return 'Произошла неизвестная ошибка'
})

const dismiss = () => {
  dismissed.value = true
  emit('dismiss')
}

const handleAction = () => {
  if (props.action?.handler) {
    props.action.handler()
  }
  emit('action', props.action)
}
</script>

<style scoped>
.error-display {
  margin-bottom: 16px;
}
</style>