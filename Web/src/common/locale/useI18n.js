import { watch, computed } from 'vue';
import { createI18n } from 'vue-i18n';

import { useConfigStoreWithOut } from '@/store/modules/config';
import { messageCn } from './zhCN';
import { messageEn } from './enUS';

const configStore = useConfigStoreWithOut();
const localeType = computed(() => configStore.getLocaleType);

const messages = {
  enUS: messageEn,
  zhCN: messageCn,
};

export const i18n = new createI18n({
  locale: localeType,
  messages,
});

export const useI18n = () => {
  watch(
    () => configStore.localeType,
    val => {
      i18n.global.locale = val;
    },
    {
      immediate: true,
    }
  );
};

// 新增
export function t(key, args) {
  if (!i18n) return key;
  return i18n.global.tc(key, args);
}
