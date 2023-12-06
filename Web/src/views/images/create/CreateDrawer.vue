<template>
  <a-drawer
    v-model:open="open"
    :destroyOnClose="true"
    :maskClosable="false"
    :closable="false"
    :title="$t('CreateImage')"
    placement="right"
    size="large"
  >
    <a-form
      ref="formRef"
      :model="formModel"
      :rules="rules"
      :labelCol="{ style: { width: '150px' } }"
      :wrapperCol="{ span: 19 }"
    >
      <a-spin :spinning="checkLoading">
        <a-form-item :label="$t('ChooseImage')" name="baseImage">
          <a-button :loading="checkLoading" @click="chooseImage">{{ $t('ChooseImage') }}</a-button>
        </a-form-item>
        <div class="prism-editor-wrap">
          <PrismEditor v-model:code="imageInfoText" readonly language="text"></PrismEditor>
        </div>

        <a-form-item :label="$t('ImageName')" name="repoName" :extra="$t('ImageNameExtra')">
          <a-input
            v-model:value="formModel.repoName"
            show-count
            :maxlength="50"
            autocomplete="off"
            :placeholder="$t('RepoNamePlaceholder')"
          />
        </a-form-item>
        <a-form-item :label="$t('ImageVersion')" name="tag">
          <a-input
            v-model:value="formModel.tag"
            show-count
            :maxlength="50"
            autocomplete="off"
            :placeholder="$t('RepoNamePlaceholder')"
          />
        </a-form-item>
        <a-form-item :label="$t('ImageDesc')" name="description">
          <a-textarea
            v-model:value="formModel.description"
            :placeholder="$t('DescriptionPlaceholder')"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>
        <Installer
          v-if="baseImageInfoObj.val"
          ref="installerRef"
          :baseImageInfoObj="baseImageInfoObj"
          @update="updateForm"
        ></Installer>
        <Interaction v-if="baseImageInfoObj.val" @update="updateForm"></Interaction>
      </a-spin>
    </a-form>
    <template #footer>
      <a-button :loading="loading" type="primary" @click="sure">{{ $t('Sure') }}</a-button>
      <a-button style="margin-left: 8px" @click="close">{{ $t('Cancel') }}</a-button>
    </template>
  </a-drawer>
  <ChooseImageDialog ref="chooseImageDialogRef" @ok="handleImageOk"></ChooseImageDialog>
</template>
<script setup>
import { ref, reactive, createVNode } from 'vue';
import { Modal, message } from 'ant-design-vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { cloneDeep } from 'lodash';
import { validaRepoName } from './util.js';
import PrismEditor from '@/components/prism-editor/index.vue';
import ChooseImageDialog from '../components/ChooseImageDialog.vue';
import { parseImageInfo, buildImage } from '@/api/modules/images';
import Installer from './Installer.vue';
import Interaction from './Interaction.vue';
import { t } from '@/common/locale/useI18n';
import { aesKey, aesIv } from './util.js';
import { encryptByAES } from '@/utils/util.js';
const emits = defineEmits(['create']);
const defaultForm = {
  baseImage: '',
  baseTag: '',
  repoName: '',
  tag: '',
  description: '',
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
  interaction: [],
  webSSHSecret: '',
  jupyterLabSecret: '',
};

const imageInfoText = ref('');

const open = ref(false);
const show = () => {
  open.value = true;
};

const reset = () => {
  imageInfoText.value = '';
  baseImageInfoObj.val = null;
  Object.assign(formModel, cloneDeep(defaultForm));
  console.log('formModel=======', formModel);
};

const close = () => {
  Modal.confirm({
    title: () => `已填写的信息将不再保存，是否确认？`,
    icon: () => createVNode(ExclamationCircleOutlined),
    width: '460px',
    okText: () => '确定',
    cancelText: () => '取消',
    onOk() {
      open.value = false;
      reset();
      return false;
    },
    onCancel() {},
  });
};

const formModel = reactive(cloneDeep(defaultForm));

const rules = {
  baseImage: [{ required: true, message: '请选择镜像', trigger: ['blur', 'change'] }],
  repoName: [
    {
      required: true,
      validator: (rule, value) => validaRepoName(rule, value, '镜像名称'),
      trigger: ['blur', 'change'],
    },
  ],
  tag: [
    {
      required: true,
      validator: (rule, value) => validaRepoName(rule, value, '镜像版本'),
      trigger: ['blur', 'change'],
    },
  ],
};

const chooseImageDialogRef = ref(null);
const chooseImage = () => {
  chooseImageDialogRef.value.show();
};

const handleImageOk = record => {
  Object.assign(formModel, cloneDeep(defaultForm));
  formModel.baseImage = record.name;
  formModel.baseTag = record.tag;
  checkImage(`${record.name}:${record.tag}`);
  formRef.value.validateFields('baseImage');
};

const formatText = data => {
  const {
    image_name = '',
    kernel = {},
    os = {},
    package_manager = {},
    python = {},
    pip = {},
    conda = {},
    jupyter_lab = {},
    sshd = {}, // webSSH
  } = data;
  let str = `镜像:${image_name}\n\n内核:${kernel?.name}:${kernel?.version}\n\n操作系统：${os?.name}:${os?.version}\n\n`;

  const packageManageStr = package_manager?.available
    ? `${package_manager?.name}:${package_manager?.version}${
        package_manager?.source?.length > 0 ? ' 安装源:' + package_manager?.source?.join(';') : ''
      }\n\n`
    : '';

  const pipStr = pip?.available
    ? `pip:${Array.isArray(pip?.version) ? pip?.version?.join(';') : pip?.version}${
        pip?.source?.length > 0 ? ' 安装源:' + pip?.source?.join(';') : ''
      }\n\n`
    : 'pip:未安装\n\n';

  const condaStr = conda?.available
    ? `conda:${Array.isArray(conda?.version) ? conda?.version?.join(';') : conda?.version}  ${
        conda?.source?.length > 0 ? ' 安装源:' + conda?.source?.join(';') : ''
      } \n\n`
    : 'conda:未安装\n\n';

  const pythonStr = python?.available
    ? `python:${python?.version?.join(';')}\n\n`
    : 'python:未安装\n\n';

  const jupyterLabStr = jupyter_lab?.available
    ? `JupyterLab:${jupyter_lab?.version}\n\n`
    : 'JupyterLab:未安装\n\n';

  const webSshStr = sshd?.available ? `WebSSH:${sshd?.version}` : 'WebSSH:未安装';

  imageInfoText.value =
    str + packageManageStr + pipStr + condaStr + pythonStr + jupyterLabStr + webSshStr;
};

const checkLoading = ref(false);
const baseImageInfoObj = reactive({ val: null });
const checkImage = imageName => {
  checkLoading.value = true;
  parseImageInfo(imageName)
    .then(json => {
      if (json && JSON.stringify(json) !== '{}') {
        Object.assign(baseImageInfoObj, { val: json });
        // 解析基础镜像信息
        formatText(json);
      }
    })
    .catch(err => {
      baseImageInfoObj.val = undefined;
      imageInfoText.value = '';
    })
    .finally(() => {
      checkLoading.value = false;
    });
};

const updateForm = obj => {
  Object.assign(formModel, obj);
};

const formRef = ref(null);
const installerRef = ref(null);
const loading = ref(false);
const sure = async () => {
  if (!(await validateForm())) return;
  const params = formatParam();
  loading.value = true;
  buildImage(params)
    .then(json => {
      message.success(t('CreateSuccess'));
      open.value = false;
      reset();
      emits('create');
    })
    .catch(err => {
      message.error(err.message);
    })
    .finally(() => {
      loading.value = false;
    });
};

const validateForm = async () => {
  const v1 = await formRef.value.validate();
  const v2 = await installerRef.value.validate();
  return true;
};

const formatParam = () => {
  const present_python_obj = baseImageInfoObj?.val?.python;
  /** 包管理安装工具（apt || yum） */
  const present_package_manager_obj = baseImageInfoObj?.val?.package_manager;
  const present_pip_obj = baseImageInfoObj?.val?.pip;
  const present_conda_obj = baseImageInfoObj?.val?.conda;
  return {
    dockerfile_json: {
      base_image: `${formModel.baseImage}:${formModel.baseTag}`,
      maintainer: 'admin',
      image_installer_config: {
        python_env: {
          present: present_python_obj?.available ? present_python_obj?.version : [], //check返回的version
          target: formModel.python_env || '',
          install_loc: '/usr/local/dros/python', //跟原来保持不变
        },
        package_manager_installer_config: {
          installer_name: formModel?.packageManage?.install?.[0] || '',
          install: {
            present: present_package_manager_obj?.available
              ? present_package_manager_obj?.version
              : [], //检测的
            target: '', //固定传空
          },
          source: {
            type: formModel?.packageManage?.source?.[0] || '', //安装源
            file_name: formModel?.packageManage?.source?.[1] || '',
          },
          software_list: getSoftware(present_package_manager_obj.name),
          python_version: [], //--- 现有的没传
        },
        pip_installer_config: {
          installer_name: 'pip',
          install: {
            present: present_pip_obj?.available ? present_pip_obj?.version : [], // check 返回的version
            target: formModel?.pip?.install || '', // 安装器的安装包
          },
          source: {
            installer_name: formModel?.pip?.install || '', // ?
            type: formModel?.pip?.source?.[0] || '', //安装器的安装源
            file_name: formModel?.pip?.source?.[1] || '',
          },
          software_list: getSoftware('pip'), // 软件安装 选择了pip安装器时候的软件名和版本，名称：版本？
          python_version: [], //取值优先级： 页面选择的python版本 > check的
        },
        conda_installer_config: {
          installer_name: 'conda',
          install: {
            present: present_conda_obj?.available ? present_conda_obj?.version : [],
            target: formModel?.conda?.install || '',
          },
          source: {
            type: formModel?.conda?.source?.[0] || '',
            file_name: formModel?.conda?.source?.[1] || '',
          },
          software_list: getSoftware('conda'),
        },
      },
    },
    image_data: {
      target_image_name: `${formModel.repoName}:${formModel.tag}`, //formModel.repoName,
      tag: formModel.tag,
      image_desc: formModel.description,
      webSSHSecret: encryptByAES(formModel.webSSHSecret, aesKey, aesIv),
      jupyterLabSecret: encryptByAES(formModel.jupyterLabSecret, aesKey, aesIv),
      task_name: '', //传空，后面去掉
      callback_url: '', //传空，后面去掉
    },
  };
};

const getSoftware = installerName => {
  let result = [];
  const temp = formModel.software.filter(item => item.install === installerName);
  result = temp.map(i => ({
    name: i?.name,
    version: i?.version,
  }));
  return result;
};

defineExpose({ show, close });
</script>
<style lang="less">
.prism-editor-wrap {
  margin-bottom: 16px;
  margin-left: 142px;
}
</style>
