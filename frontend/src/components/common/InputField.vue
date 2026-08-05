<template>
    <div>
      <label :for="id" class="block text-sm font-medium text-gray-900">{{ label }}</label>
      <input
        :id="id"
        :type="type"
        :autocomplete="autocomplete"
        :required="required"
        :placeholder="placeholder"
        :value="modelValue"
        class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </div>
  </template>
  
  <script setup>
  defineProps({
    modelValue: {
      type: String,
      default: '',
    },
    id: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: 'text',
    },
    autocomplete: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
    required: {
      type: Boolean,
      default: false,
    },
  })
  
  defineEmits(['update:modelValue'])
  </script>