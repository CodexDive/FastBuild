import { defineStore } from 'pinia';

import { store } from '@/store';

export const useConfigStore = defineStore({
  id: 'config',
  state: () => ({
    themeType: '',
    themeConfig: {},
    localeType: '',
    localeConfig: {},
  }),
  getters: {
    getThemeType() {
      return this.themeType;
    },
    getThemeConfig() {
      return this.themeConfig;
    },
    getLocaleType() {
      return this.localeType;
    },
    getLocaleConfig() {
      return this.localeConfig;
    },
  },
  actions: {
    setThemeType(themeType) {
      this.themeType = themeType;
    },
    setThemeConfig(themeConfig) {
      this.themeConfig = themeConfig;
    },
    setLocaleType(localeType) {
      this.localeType = localeType;
    },
    setLocaleConfig(localeConfig) {
      this.localeConfig = localeConfig;
    },
  },
});

// 在组件setup函数外使用
export function useConfigStoreWithOut() {
  return useConfigStore(store);
}
