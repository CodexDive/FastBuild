<template>
  <div class="flex interactionItem flex-space">
    <a-form-item :label="$t('InteractionType')" name="interaction">
      <a-checkbox-group v-model:value="formModel.interaction">
        <div class="check flex">
          <a-checkbox value="WEB_SSH" class="checkbox-custom"> WebSSH </a-checkbox>
          <a-checkbox value="JUPYTER_LAB" class="checkbox-custom check-other">
            JupyterLab
          </a-checkbox>
        </div>
      </a-checkbox-group>
    </a-form-item>

    <div class="flex secret">
      <a-form-item
        name="webSSHSecret"
        :label="$t('Password')"
        :rules="[
          {
            required: sshAble,
            message: $t('InputPlease'),
            trigger: ['blur', 'change'],
          },
          {
            validator: (rule, value) => validatePassword(rule, value),
            trigger: ['blur', 'change'],
          },
        ]"
        :labelCol="{ style: { width: '70px' } }"
        :wrapperCol="{ style: { width: '330px' } }"
      >
        <a-input
          v-model:value="formModel.webSSHSecret"
          :disabled="!sshAble"
          :placeholder="$t('InputPasswordPlease')"
          @keydown="handleNoSpace"
        />
      </a-form-item>

      <a-form-item
        name="jupyterLabSecret"
        :label="$t('Password')"
        :rules="[
          {
            required: jupyterAble,
            message: $t('InputPlease'),
            trigger: ['blur', 'change'],
          },
          {
            validator: (rule, value) => validatePassword(rule, value),
            trigger: ['blur', 'change'],
          },
        ]"
        :labelCol="{ style: { width: '70px' } }"
        :wrapperCol="{ style: { width: '330px' } }"
      >
        <a-input
          v-model:value="formModel.jupyterLabSecret"
          :disabled="!jupyterAble"
          :placeholder="$t('InputPasswordPlease')"
          @keydown="handleNoSpace"
        />
      </a-form-item>
    </div>
  </div>
</template>
<script setup>
import { reactive, watch, computed } from 'vue';
import { cloneDeep } from 'lodash';
import { handleNoSpace, validatePassword } from './util.js';
const formModel = reactive({
  interaction: [],
  webSSHSecret: '',
  jupyterLabSecret: '',
});
const sshAble = computed(() => formModel.interaction.includes('WEB_SSH'));
const jupyterAble = computed(() => formModel.interaction.includes('JUPYTER_LAB'));

watch(sshAble, next => {
  formModel.webSSHSecret = next ? 'Abc12345' : '';
});
watch(jupyterAble, next => {
  formModel.jupyterLabSecret = next ? 'Abc12345' : '';
});

const emits = defineEmits(['update']);
watch(formModel, next => {
  emits('update', cloneDeep(next));
});
</script>
<style lang="less">
.flex {
  display: flex;
}
.flex-space {
  justify-content: space-between;
}
.interactionItem {
  .secret {
    flex-direction: column;
    align-items: flex-end;
  }
}
.check {
  flex-direction: column;
  .checkbox-custom {
    height: 32px;
    line-height: 32px;
    margin-bottom: 24px;
  }
  .check-other {
    margin-left: 0;
    margin-bottom: 0;
  }
}
</style>
