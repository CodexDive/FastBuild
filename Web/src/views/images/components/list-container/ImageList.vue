<template>
  <a-table
    :columns="columns"
    rowKey="id"
    :data-source="dataSource"
    :loading="loading"
    style="margin-top: 8px"
    :scroll="{ x: 1200 }"
    :rowSelection="props.rowSelection"
    :pagination="pagination"
    @change="handleTableChange"
  >
    <template #bodyCell="{ text, record, index, column }">
      <template v-if="['state', 'status'].includes(column.dataIndex)">
        <a-tag :color="imageStatusEnums[text]?.status">{{
          imageStatusEnums[text]?.text || text
        }}</a-tag>
      </template>
      <template v-if="column.dataIndex === 'type'">
        {{ imageTypeEnums[text]?.text || text }}
      </template>
      <template v-if="column.dataIndex === 'interaction'">
        <a-tooltip>
          <template #title>WebSSH</template>
          <img v-if="text?.includes('WebSSH')" class="w-20 h-20" src="@/assets/images/ssh.png" />
        </a-tooltip>
        <a-tooltip>
          <template #title>JupyterLab</template>
          <img
            v-if="text?.includes('JupyterLab')"
            class="ml-8 w-20 h-20"
            src="@/assets/images/jupyter.png"
          />
        </a-tooltip>
      </template>
      <template v-if="column.dataIndex === 'operate'">
        <a-button
          v-if="record.type !== 'Base'"
          class="ml--15"
          type="link"
          danger
          @click="handleDelete(record)"
        >
          {{ $t('Delete') }}
        </a-button>
        <a-button v-if="!isImageList" type="link" @click="handleLog(record)">{{
          $t('BuildLog')
        }}</a-button>
      </template>
    </template>
  </a-table>
  <LogDrawer ref="logDrawerRef"></LogDrawer>
</template>
<script setup>
import { onMounted, ref, computed, createVNode, watch } from 'vue';
import { bool, string } from 'vue-types';
import { Modal, message } from 'ant-design-vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { getImageList, delImage, getBuildList, delBuild } from '@/api/modules/images';
import { getColumns } from './column';
import { imageStatusEnums, imageTypeEnums } from '@/common/enums';
import { t } from '@/common/locale/useI18n';
import LogDrawer from '../../log/LogDrawer.vue';

const props = defineProps({
  isImageList: bool(),
  isModuleMode: bool(),
  rowSelection: undefined,
  imageType: string(),
});

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
});

const columns = computed(() => getColumns(props.isImageList, props.isModuleMode));

const loading = ref(null);
const dataSource = ref(null);
let firstLoad = true;
const request = params => {
  loading.value = true;
  if (!props.isImageList) {
    return queryBuildList(params);
  }
  const param = {
    page: params?.current || 1,
    page_size: params?.pageSize || 10,
    keyword: params?.name || undefined,
    image_type: firstLoad && props.isModuleMode ? props.imageType : params?.image_type || undefined,
  };
  return getImageList(param)
    .then(json => {
      const { image_list = [], page } = json;
      dataSource.value = image_list;
      Object.assign(pagination.value, {
        current: page.current,
        pageSize: page.page_size,
        total: page.total,
      });
      return json;
    })
    .finally(() => {
      firstLoad = false;
      loading.value = false;
    });
};
onMounted(() => {
  request();
});
watch(
  () => props.isImageList,
  () => {
    request();
  }
);

const queryBuildList = params => {
  const param = {
    page: params?.current || 1,
    page_size: params?.pageSize || 10,
    image_name: params?.name || undefined,
    task_status: params?.status || undefined,
  };
  return getBuildList(param)
    .then(json => {
      const { task_list = [], page } = json;
      Object.assign(pagination.value, {
        current: page.current,
        pageSize: page.page_size,
        total: page.total,
      });
      dataSource.value = task_list;
      return json;
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleTableChange = page => {
  request(page);
};

const handleDelete = record => {
  Modal.confirm({
    title: t('DeleteConfirm'),
    icon: createVNode(ExclamationCircleOutlined),
    okText: t('Confirm'),
    cancelText: t('Cancel'),
    onOk: async () => {
      try {
        await deleteImage(record);
        message.success(t('DeleteSuccess'));
        request();
      } catch (error) {
        message.error(error.message);
      }
      request({ current: 1 });
    },
  });
};

const deleteImage = ({ task_id, name, tag }) => {
  if (props.isImageList) {
    return delImage({ image_name: `${name}:${tag}` });
  }
  return delBuild({ task_id: task_id });
};

const logDrawerRef = ref(null);
const handleLog = record => {
  logDrawerRef.value.show(record.task_id);
};

defineExpose({ request });
</script>
