<script setup>

defineProps({

  label: {
    type: String,
    required: true
  },

  variant: {
    type: String,
    default: 'primary'
  }
})

</script>

<template>

  <span
    class="badge"
    :class="variant"
  >

    {{ label }}

  </span>

</template>

<style scoped>

.badge {

  display: inline-flex;

  align-items: center;

  justify-content: center;

  padding: 6px 12px;

  border-radius:
    var(--radius-sm);

  font-size: 12px;

  font-weight: 700;
}

.primary {

  background-color:
    var(--adnu-blue-light);

  color:
    var(--adnu-blue-dark);
}

.success {

  background-color:
    var(--adnu-gold);

  color:
    var(--text-main);
}

.live {

  background-color:
    var(--adnu-live-red);

  color:
    var(--white);
}

.danger {

  background-color:
    var(--adnu-danger-light);

  color:
    var(--adnu-danger);
}

</style>