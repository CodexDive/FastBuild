import { t } from '@/common/locale/useI18n';

export const validaRepoName = (rule, value, nameCn = '镜像名称') => {
  const reg = /^(?![.\-_/])[0-9a-z.\-_/]*(?<![.\-_/])$/;
  if (value === '' || !value) {
    return Promise.reject(`${nameCn}不能为空`);
  } else if (!reg.test(value)) {
    return Promise.reject(t('RepoNamePlaceholder'));
  } else {
    return Promise.resolve();
  }
};

// 不包含中文
export const codeValidator = async (rule, value) => {
  const reg = /^[^\u4e00-\u9fa5]+$/g;
  if (value === '' || !value) {
    return Promise.reject('请输入');
  } else if (!reg.test(value)) {
    return Promise.reject('不支持包含中文');
  } else {
    return Promise.resolve();
  }
};

export const versionValidator = async (rule, value) => {
  const reg = /^[^\u4e00-\u9fa5]+$/g;
  if (value === '' || !value) {
    return Promise.resolve();
  } else {
    if (!reg.test(value)) {
      return Promise.reject('不支持包含中文');
    } else {
      return Promise.resolve();
    }
  }
};

export const validatePassword = async (rule, value) => {
  const reg = /^[^\u4e00-\u9fa5]+$/g;
  if (!value || value === '') {
    return Promise.resolve();
  } else if (value.length < 6 || value.length > 50) {
    return Promise.reject('请输入6-50位字符');
  } else if (!reg.test(value)) {
    return Promise.reject('不支持包含中文');
  } else {
    return Promise.resolve();
  }
};

// 禁止输入空格
export const handleNoSpace = event => {
  if (event.keyCode == 32) {
    event.returnValue = false;
  }
};

export const renderOption = (arr = []) => {
  return arr.map(item => ({ label: item, value: item }));
};

export const renderCascaderOption = (arr = []) => {
  return arr.map(item => ({
    value: item?.type,
    label: item?.type,
    children: item?.name.map(i => ({ value: i, label: i })),
  }));
};

// aes 加密的 key 和 iv(偏移量)
export const aesKey = 'c7e71f37dda040fd';
export const aesIv = '0000000000000000';
