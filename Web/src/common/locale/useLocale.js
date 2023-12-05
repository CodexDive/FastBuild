import { watch } from 'vue';

import { useConfigStoreWithOut } from '@/store/modules/config';
import { en_US } from './enUS';
import { zh_CN } from './zhCN';

const configStore = useConfigStoreWithOut();

const changeLocale = locale => {
  switch (locale) {
    case 'enUS':
      configStore.setLocaleConfig(en_US);
      break;
    case 'zhCN':
      configStore.setLocaleConfig(zh_CN);
      break;
  }
};

export const useLocale = () => {
  watch(
    () => configStore.localeType,
    val => {
      changeLocale(val);
    },
    {
      immediate: true,
    }
  );
};
