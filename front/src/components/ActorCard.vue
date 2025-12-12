<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
      v-bind="props"
      class="actor-card"
      :elevation="isHovering ? 8 : 2"
      @click="$emit('click')"
      max-width="150"
    >
      <v-img
        :src="actor.photo_url || actor.photo"
        aspect-ratio="2/3"
        class="actor-photo"
      >
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular indeterminate color="grey lighten-5" />
          </v-row>
        </template>
      </v-img>
      
      <v-card-text class="pa-3 text-center">
        <div class="actor-name">{{ actor.name }}</div>
        <div v-if="actor.role" class="actor-role text-caption text-grey">
          {{ actor.role }}
        </div>
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script setup>
defineProps({
  actor: {
    type: Object,
    required: true,
    default: () => {}
  }
})

defineEmits(['click'])
</script>

<style scoped>
.actor-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.actor-card:hover {
  transform: translateY(-4px);
}

.actor-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.2;
  margin-bottom: 4px;
}

.actor-role {
  font-size: 0.8rem;
  line-height: 1.1;
}
</style>