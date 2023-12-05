import { t } from '@/common/locale/useI18n';

export const imageStatusEnums = {
  QUEUED: { text: t('QUEUED'), status: 'default' },
  STARTED: { text: t('STARTED'), status: 'warning' },
  BUILD_SUCCESS: { text: t('PUSH_RUNNING'), status: 'warning' },
  BUILD_FAILED: { text: t('BUILD_FAILED'), status: 'error' },
  PUSH_SUCCESS: { text: t('PUSH_SUCCESS'), status: 'success' },
  PUSH_FAILED: { text: t('PUSH_FAILED'), status: 'error' },
  BUILD_ABORT: { text: t('BUILD_ABORT'), status: 'error' },
};

export const imageStatusOptions = [
  { value: 'QUEUED', label: t('QUEUED') },
  { value: 'STARTED', label: t('STARTED') },
  { value: 'BUILD_SUCCESS', label: t('PUSH_RUNNING') },
  { value: 'BUILD_FAILED', label: t('BUILD_FAILED') },
  { value: 'PUSH_SUCCESS', label: t('PUSH_SUCCESS') },
  { value: 'PUSH_FAILED', label: t('PUSH_FAILED') },
  { value: 'BUILD_ABORT', label: t('BUILD_ABORT') },
];

export const imageTypeEnums = {
  Base: { text: t('BaseImage'), status: 'success' },
  Customized: { text: t('CustomizedImage'), status: 'processing' },
};

export const imageTypeOptions = [
  { value: 'Base', label: t('BaseImage') },
  { value: 'Customized', label: t('CustomizedImage') },
];

export const actionMap = {
  pull: t('LogPull'),
  check: t('LogCheck'),
  prepare: t('LogPrepare'),
  build: t('LogBuild'),
  push: t('LogPush'),
};
