<template>
  <a-form layout="inline" :model="formState">
    <a-form-item>
      <a-input-search
        v-model:value="formState.name"
        :placeholder="$t('ImageName')"
        allowClear
        @search="search"
      />
    </a-form-item>
    <a-form-item v-if="!props.isImageList">
      <a-select
        v-model:value="formState.status"
        style="width: 200px"
        :options="imageStatusOptions"
        allowClear
        :placeholder="$t('BuildStatus')"
        @change="search"
      />
    </a-form-item>
    <a-form-item v-if="props.isImageList">
      <a-select
        v-model:value="formState.image_type"
        style="width: 200px"
        :options="imageTypeOptions"
        allowClear
        :placeholder="$t('ImageType')"
        @change="search"
      />
    </a-form-item>
    <a-form-item>
      <a-space>
        <a-button type="primary" @click="search">{{ $t('Search') }}</a-button>
        <a-button @click="reset">{{ $t('Reset') }}</a-button>
      </a-space>
    </a-form-item>
  </a-form>
</template>
<script setup>
import { reactive, watch } from 'vue';
import { bool, string } from 'vue-types';
import { cloneDeep } from 'lodash';
import { imageStatusOptions, imageTypeOptions } from '@/common/enums/index';

const props = defineProps({
  isImageList: bool(),
  imageType: string(),
});

watch(
  () => props.isImageList,
  next => {
    resetCondition();
  }
);

const emit = defineEmits(['search']);

const formState = reactive({
  name: undefined,
  status: undefined,
  image_type: props.imageType || undefined,
});

const search = () => {
  emit('search', cloneDeep(formState));
};

const resetCondition = () => {
  formState.name = undefined;
  formState.status = undefined;
  formState.image_type = undefined;
};

const reset = () => {
  resetCondition();
  search();
};
</script>
