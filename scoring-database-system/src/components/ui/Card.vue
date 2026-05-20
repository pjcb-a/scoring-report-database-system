<script setup>

defineProps({

  hoverable: {
    type: Boolean,
    default: false
  },

  padding: {
    type: String,
    default: 'md'
  }
})

</script>

<template>

  <div
    class="card"
    :class="[
      padding,
      { hoverable }
    ]"
  >

    <div
      v-if="$slots.header"
      class="card-header"
    >
      <slot name="header" />
    </div>

    <div class="card-body">

      <slot />

    </div>

    <div
      v-if="$slots.footer"
      class="card-footer"
    >
      <slot name="footer" />
    </div>

  </div>

</template>

<style scoped>

.card {

  background-color:
    var(--white);

  border:
    1px solid var(--border-color);

  border-radius:
    var(--radius-lg);

  box-shadow:
    var(--shadow-sm);

  transition:
    var(--transition-fast);
}

.card.hoverable:hover {

  transform:
    translateY(-2px);

  box-shadow:
    var(--shadow-md);
}

.sm {

  padding: 14px;
}

.md {

  padding: 20px;
}

.lg {

  padding: 28px;
}

.card-header {

  margin-bottom: 18px;
}

.card-footer {

  margin-top: 18px;
}

</style>