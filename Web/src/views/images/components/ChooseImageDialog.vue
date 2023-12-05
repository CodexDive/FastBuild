<template>
  <a-modal v-model:open="open" width="90%" :title="$t('ChooseImage')" @ok="handleOk">
    <ListContainer
      v-if="open"
      ref="listContainerRef"
      importMode="modules"
      imageType="Base"
      @selectRow="handleSelect"
    ></ListContainer>
  </a-modal>
</template>
<script setup>
import { ref } from 'vue';
import ListContainer from './list-container/ListContainer.vue';

const open = ref(false);
const show = () => {
  open.value = true;
};
const close = () => {
  open.value = false;
};

const listContainerRef = ref(null);

const secletedData = ref(null);
const handleSelect = record => {
  secletedData.value = record;
};

const emits = defineEmits(['ok']);
const handleOk = () => {
  if (!secletedData.value) return;
  emits('ok', secletedData.value);
  close();
};

defineExpose({ show, close });
</script>
