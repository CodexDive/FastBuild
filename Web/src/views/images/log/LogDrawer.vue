<template>
  <a-drawer v-model:open="open" :title="$t('BuildLog')" placement="right" size="large">
    <a-spin tip="Loading..." :spinning="loading">
      <a-timeline v-if="logData.length > 0">
        <div v-for="(item, index) in logData" :key="index" class="time-line">
          <div class="item-label">{{ actionMap[item?.action] }}</div>
          <div class="item-line">
            <a-timeline-item>
              <template #dot>
                <component :is="statusMap[item?.status]"></component>
              </template>
              <span>
                {{ formatTime(item?.start_time) }}
              </span>
              <br />
              <span>
                {{ $t('Log') }}:
                <a class="preview-btn" :href="item?.log_url" target="_blank">{{ $t('Preview') }}</a>
                <span
                  class="download-btn"
                  @click="() => downloadLog(item?.log_url, `${item?.action}_log`)"
                  >{{ $t('Download') }}
                </span>
              </span>
              <span v-if="item?.action === 'prepare'" class="docker-item">
                Dockerfile:
                <a class="preview-btn" :href="item?.dockerfile_url" target="_blank">{{
                  $t('Preview')
                }}</a>
                <span
                  class="download-btn"
                  @click="() => downloadLog(item?.dockerfile_url, 'Dockerfile_log')"
                  >{{ $t('Download') }}
                </span>
              </span>
            </a-timeline-item>
          </div>
        </div>
      </a-timeline>
      <a-empty v-else />
    </a-spin>
  </a-drawer>
</template>
<script setup>
import { ref, h } from 'vue';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons-vue';
import moment from 'moment';
import { buildDetail } from '@/api/modules/images';
import { actionMap } from '@/common/enums/index';
import { downloadByBlob } from '@/utils/util';

const statusMap = {
  success: h(CheckCircleOutlined, { style: 'font-size: 16px; color:#52C41A' }),
  fail: h(CloseCircleOutlined, { style: 'font-size: 16px; color: #FF4D4F' }),
};

const formatTime = timestamp => {
  return timestamp ? moment(timestamp).format('YYYY-MM-DD HH:mm:ss') : '-';
};

const open = ref(false);
const show = task_id => {
  if (!task_id) {
    return;
  }
  getProgress(task_id);
  open.value = true;
};

const close = () => {
  open.value = false;
  logData.value = [];
};

const logData = ref([]);
const loading = ref(false);
const getProgress = task_id => {
  loading.value = true;
  buildDetail({ task_id: task_id })
    .then(json => {
      const { progress = [] } = json;
      logData.value = progress;
    })
    .finally(() => {
      loading.value = false;
    });
};

const downloadLog = (url, fileName) => {
  downloadByBlob(url, fileName);
};

defineExpose({ show, close });
</script>
<style lang="less" scoped>
.time-line {
  display: flex;
  .item-label {
    margin-right: 12px;
    margin-top: -5px;
    width: 120px;
    word-wrap: break-word;
    text-align: right;
  }
  .item-line {
    flex: 1;
  }
  .ant-timeline-item {
    padding-top: 2px;
  }
  .docker-item {
    margin-left: 10px;
  }

  .preview-btn {
    margin-right: 10px;
    margin-left: 10px;
    color: #52c41a;
    cursor: pointer;
  }
  .download-btn {
    color: #1890ff;
    cursor: pointer;
  }
}
:deep(.ant-timeline-item-last .ant-timeline-item-tail) {
  border: 0 !important;
}
</style>
