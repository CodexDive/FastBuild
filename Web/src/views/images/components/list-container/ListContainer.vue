<template>
  <a-tabs v-if="!isModuleMode" v-model:activeKey="activeTab" type="card">
    <a-tab-pane v-for="item in tabs" :key="item.value" :tab="item.label"></a-tab-pane>
  </a-tabs>
  <SearchForm :isImageList="isImageList" :imageType="imageType" @search="handleSearch"></SearchForm>
  <a-button
    v-if="activeTab === 'buildTaskList' && !isModuleMode"
    type="primary"
    class="mt-8"
    @click="handleAdd"
  >
    {{ $t('CreateImage') }}
  </a-button>
  <ImageList
    ref="imageListRef"
    :imageType="imageType"
    :isModuleMode="isModuleMode"
    :isImageList="isImageList"
    :rowSelection="rowSelection"
  ></ImageList>
  <CreateDrawer ref="createDrawerRef" @create="refresh"></CreateDrawer>
</template>
<script setup>
import { ref, computed } from 'vue';
import { string } from 'vue-types';
import { t } from '@/common/locale/useI18n';
import SearchForm from './SearchForm.vue';
import ImageList from './ImageList.vue';
import CreateDrawer from '../../create/CreateDrawer.vue';

const tabs = [
  { value: 'buildTaskList', label: t('BuildTaskList') },
  { value: 'imageList', label: t('ImageList') },
];

const props = defineProps({
  importMode: string().def('page'), //page | modules
  imageType: string(),
});

const isModuleMode = computed(() => props.importMode === 'modules');

const activeTab = ref(isModuleMode.value ? 'imageList' : 'buildTaskList');

const isImageList = computed(() => activeTab.value === 'imageList');

const imageListRef = ref(null);
const handleSearch = param => {
  imageListRef.value.request(param);
};

const createDrawerRef = ref(null);
const handleAdd = () => {
  createDrawerRef.value.show();
};

const emits = defineEmits(['selectRow']);
const handleSelect = record => {
  emits('selectRow', record);
};
const rowSelection = computed(() => {
  return isModuleMode.value ? { type: 'radio', onSelect: handleSelect } : undefined;
});

const refresh = () => {
  imageListRef.value.request();
};
</script>
