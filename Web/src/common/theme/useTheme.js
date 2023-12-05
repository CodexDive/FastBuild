import { watch, ref } from 'vue';

import { useConfigStoreWithOut } from '@/store/modules/config';

import { ThemeConfigLight } from './light';
import { ThemeConfigDark } from './dark';

const themeStore = useConfigStoreWithOut();

// 系统监听变量
let matchMedia = '';
const watchSystemThemeChange = () => {
  // 仅需一次初始化
  if (matchMedia) return;
  // Window 的 matchMedia() 方法返回一个新的 MediaQueryList 对象，表示指定的媒体查询 (en-US)字符串解析后的结果。返回的 MediaQueryList 可被用于判定 Document 是否匹配媒体查询，或者监控一个 document 来判定它匹配了或者停止匹配了此媒体查询。
  matchMedia = window.matchMedia('(prefers-color-scheme: dark)');
  matchMedia.onchange = () => {
    changeTheme('system');
  };
};

const changeTheme = theme => {
  switch (theme) {
    case 'light':
      themeStore.setThemeConfig(ThemeConfigLight);
      break;
    case 'dark':
      themeStore.setThemeConfig(ThemeConfigDark);
      break;
    // case 'system':
    //   watchSystemThemeChange();
    //   break;
  }
};

export const useTheme = () => {
  watch(
    () => themeStore.themeType,
    val => {
      changeTheme(val);
    },
    {
      immediate: true,
    }
  );
};
