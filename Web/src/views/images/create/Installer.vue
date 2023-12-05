<template>
  <a-form ref="formRef" :model="formModel" :labelCol="{ style: { width: '150px' } }">
    <div class="flex flex-space">
      <a-form-item
        :label="$t('PackageManageTool')"
        :name="['packageManage', 'install']"
        :labelCol="{ style: { width: '152px' } }"
        style="margin-bottom: 0"
      >
        <a-checkbox-group
          v-model:value="formModel.packageManage.install"
          @change="changePacInstall"
        >
          <a-checkbox :value="packageManageName">{{ packageManageName }}</a-checkbox>
        </a-checkbox-group>
      </a-form-item>
      <a-form-item
        :label="$t('InstallSource')"
        :name="['packageManage', 'source']"
        :rules="[
          {
            required: formModel.packageManage.install?.length > 0,
            message: $t('InputPlease'),
          },
        ]"
        :labelCol="{ style: { width: '100px' } }"
        style="margin-bottom: 0"
      >
        <a-cascader
          v-model:value="formModel.packageManage.source"
          :disabled="formModel.packageManage.install?.length === 0"
          :placeholder="$t('ChooseInstallSourcePlease')"
          :options="packageManageSource[packageManageName]"
          allowClear
          style="width: 340px"
        />
        <template #extra>
          <span class="notice"> <ExclamationCircleFilled />{{ $t('InstallSourceNotice') }} </span>
        </template>
      </a-form-item>
    </div>

    <a-form-item :label="$t('PythonInstall')" name="python_env">
      <a-select
        v-model:value="formModel.python_env"
        :placeholder="$t('ChoosePythonPlease')"
        :options="pythonOptions"
        allowClear
      />
      <template #extra>
        <span class="notice"> <ExclamationCircleFilled />{{ $t('PythonNotice') }} </span>
      </template>
    </a-form-item>

    <div class="flex install-item flex-space">
      <a-form-item :label="$t('InstallerInstall')" name="install">
        <a-checkbox-group v-model:value="formModel.install">
          <div class="flex check">
            <a-checkbox value="pip" class="checkbox-custom" @change="e => toggleInstall(e)">
              pip
            </a-checkbox>
            <a-checkbox
              value="conda"
              class="checkbox-custom check-other"
              @change="e => toggleInstall(e)"
            >
              conda
            </a-checkbox>
          </div>
        </a-checkbox-group>
      </a-form-item>
      <div class="flex col-group">
        <a-form-item name="pip" :style="{ marginBottom: 0 }">
          <a-form-item
            :label="$t('InstallPackage')"
            :name="['pip', 'install']"
            :style="{ width: '200px', marginBottom: '24px' }"
            :rules="[
              {
                required: formModel.install.includes('pip'),
                message: $t('InputPlease'),
              },
            ]"
          >
            <a-select
              v-model:value="formModel.pip.install"
              :disabled="!formModel.install.includes('pip')"
              :placeholder="$t('ChoosePlease')"
              :options="pipInstallOptions"
              allowClear
              style="max-width: 130px"
            />
          </a-form-item>
        </a-form-item>
        <a-form-item name="conda" style="margin-bottom: 0">
          <a-form-item
            :label="$t('InstallPackage')"
            :name="['conda', 'install']"
            :style="{ width: '200px', marginBottom: '24px' }"
            :rules="[
              {
                required: formModel.install.includes('conda'),
                message: $t('InputPlease'),
              },
            ]"
          >
            <a-select
              v-model:value="formModel.conda.install"
              :disabled="!formModel.install.includes('conda')"
              :placeholder="$t('ChoosePlease')"
              :options="condaInstallOptions"
              allowClear
              style="max-width: 130px"
            />
          </a-form-item>
        </a-form-item>
      </div>
      <div class="flex col-group">
        <a-form-item name="pip" style="margin-bottom: 0">
          <a-form-item
            :label="$t('InstallSource')"
            :name="['pip', 'source']"
            :style="{ width: '200px', marginBottom: '24px' }"
            :rules="[
              {
                required: formModel.install.includes('pip'),
                message: $t('InputPlease'),
              },
            ]"
          >
            <a-cascader
              v-model:value="formModel.pip.source"
              :disabled="!formModel.install.includes('pip')"
              :placeholder="$t('ChoosePlease')"
              :options="pipSourceOptions"
              allowClear
              style="max-width: 130px"
            />
          </a-form-item>
        </a-form-item>
        <a-form-item name="conda" style="margin-bottom: 0">
          <a-form-item
            :label="$t('InstallSource')"
            :name="['conda', 'source']"
            :style="{ width: '200px', marginBottom: '24px' }"
            :rules="[
              {
                required: formModel.install.includes('conda'),
                message: $t('InputPlease'),
              },
            ]"
          >
            <a-cascader
              v-model:value="formModel.conda.source"
              :disabled="!formModel.install.includes('conda')"
              :placeholder="$t('ChoosePlease')"
              :options="condaSourceOptions"
              allowClear
              style="max-width: 130px"
            />
          </a-form-item>
        </a-form-item>
      </div>
    </div>

    <a-form-item :label="$t('SoftwareInstall')" name="software">
      <div class="notice-software">{{ $t('SoftwareNotice') }}</div>
      <div
        v-for="(item, index) in formModel.software"
        :key="item.id"
        class="card-container flex-space"
      >
        <a-form-item
          :name="['software', index, 'name']"
          :rules="[
            {
              required: true,
              validator: (rule, value) => codeValidator(rule, value),
              trigger: ['change'],
            },
          ]"
          style="width: 120px"
        >
          <a-input
            v-model:value="item.name"
            autoComplete="off"
            :placeholder="$t('InputSoftwarePlease')"
          />
        </a-form-item>
        <span> == </span>
        <a-form-item
          :name="['software', index, 'version']"
          style="width: 120px"
          :rules="[
            {
              validator: async (rule, value) => versionValidator(rule, value),
            },
          ]"
        >
          <a-input
            v-model:value="item.version"
            autoComplete="off"
            :placeholder="$t('InputVersionPlease')"
          />
        </a-form-item>
        <a-form-item
          :name="['software', index, 'install']"
          :label="$t('Installer')"
          :rules="[
            {
              required: true,
              message: $t('ChoosePlease'),
            },
          ]"
          style="width: 200px"
        >
          <a-select
            v-model:value="item.install"
            :options="dynamicOptions"
            :placeholder="$t('ChoosePlease')"
          />
        </a-form-item>
        <div class="delete-btn">
          <MinusCircleOutlined @click="() => removeItem(item)" />
        </div>
      </div>

      <a-form-item style="width: 100%">
        <a-button type="dashed" block class="add-btn" @click="addItem">
          <PlusOutlined />
          {{ $t('AddSoftware') }}
        </a-button>
      </a-form-item>
    </a-form-item>
  </a-form>
</template>
<script setup>
import { ref, reactive, onMounted, nextTick, watch, computed } from 'vue';
import { object } from 'vue-types';
import { cloneDeep } from 'lodash';
import { PlusOutlined, ExclamationCircleFilled, MinusCircleOutlined } from '@ant-design/icons-vue';
import { renderOption, renderCascaderOption, codeValidator, versionValidator } from './util.js';
import { parseImageInfo, fetchSourceList, fetchSoftwareList } from '@/api/modules/images';

const props = defineProps({
  baseImageInfoObj: object(),
});

const emits = defineEmits(['update']);

const defaultForm = {
  packageManage: {
    install: [], // 包管理安装工具：apt、yum
    source: undefined, // 包管理安装工具- 安装源
  },
  python_env: undefined, // python 安装
  install: [], //安装器安装
  pip: {
    install: undefined, // 安装包
    source: undefined, // 安装源
  },
  conda: {
    install: undefined, // 安装包
    source: undefined, // 安装源
  },
  software: [],
};

const formModel = reactive(cloneDeep(defaultForm));

watch(formModel, next => {
  emits('update', cloneDeep(next));
});

onMounted(() => {
  fetchSoftwareResult();
  fetchSourceResult();
});

// 软件工具安装包信息查询
const pythonOptions = ref([]);
const pipInstallOptions = ref([]);
const condaInstallOptions = ref([]);
const fetchSoftwareResult = async () => {
  const result = (await fetchSoftwareList()) || {};
  const { python = [], pip = [], conda = [] } = result['software_list'];
  pythonOptions.value = renderOption(python);
  pipInstallOptions.value = renderOption(pip);
  condaInstallOptions.value = renderOption(conda);
};

// 源文件信息查询
const pipSourceOptions = ref([]);
const condaSourceOptions = ref([]);
const packageManageSource = reactive({
  pip: [],
  conda: [],
});
const fetchSourceResult = async () => {
  const result = (await fetchSourceList()) || {};
  const { conda = [], pip = [], apt = [], yum = [] } = result['source_list'];
  pipSourceOptions.value = renderCascaderOption(pip);
  condaSourceOptions.value = renderCascaderOption(conda);
  packageManageSource.apt = renderCascaderOption(apt);
  packageManageSource.yum = renderCascaderOption(yum);
};

const toggleInstall = e => {
  const current = e.target.value;
  nextTick(() => {
    const install = formModel.install;
    // 不选择
    if (!install.includes(current)) {
      formModel[current] = { install: undefined, source: undefined };
    }
  });
};

const addItem = () => {
  formModel.software.push({
    name: '',
    version: '',
    install: undefined,
    id: Date.now(),
  });
};
const removeItem = item => {
  let index = formModel.software.indexOf(item);
  if (index !== -1) {
    formModel.software.splice(index, 1);
  }
};

const changePacInstall = () => {
  formModel.packageManage.source = undefined;
};

const packageManageName = ref(); //'apt'
const baseSource = reactive({ val: [] });
watch(
  () => props.baseImageInfoObj.val,
  newVal => {
    if (newVal) {
      Object.assign(formModel, cloneDeep(defaultForm));
      const { package_manager } = newVal;
      packageManageName.value = package_manager?.name;
      const options = [
        { label: newVal?.package_manager?.name || '', value: newVal?.package_manager?.name || '' },
      ];
      if (newVal?.pip?.available) {
        options.push({ label: 'pip', value: 'pip' });
      }
      if (newVal?.conda?.available) {
        options.push({ label: 'conda', value: 'conda' });
      }
      baseSource.val = options;
    }
  },
  { deep: true, immediate: true }
);
const dynamicOptions = computed(() => {
  const baseSet = baseSource.val.map(i => i.value);
  const tmp = [...new Set([...baseSet, ...formModel.install])];
  return tmp.map(i => ({ value: i, label: i }));
});

const formRef = ref();
const validate = () => {
  formRef.value.validate();
};

defineExpose({ validate });
</script>
<style lang="less" scoped>
.flex {
  display: flex;
}
.flex-space {
  justify-content: space-between;
}
.notice {
  color: #faad14;
  font-size: 14px;
  font-weight: 400;
  margin-top: 4px;
  margin-bottom: 24px;
}
.install-item {
  :deep(> .ant-form-item) {
    margin-bottom: 0px;
  }
  .col-group {
    flex-direction: column;
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
    margin-top: 24px;
  }
}
.notice-software {
  padding-top: 5px;
  padding-bottom: 5px;
}
.notice-width {
  width: 820px;
  align-items: flex-start;

  @apply bg-lightgreen;
  :deep(.ant-alert-icon) {
    color: rgba(0, 0, 0, 0.65);
  }
  .btn {
    padding: 0 5px;
    text-decoration: underline;
    cursor: pointer;
  }
}
.card-container {
  display: flex;
  :deep(.ant-card-body) {
    padding: 10px;
  }
  .delete-btn {
    align-self: flex-end;
    margin-left: 10px;
    margin-bottom: 30px;
  }
}
</style>
