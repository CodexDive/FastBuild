import { createPinia } from 'pinia';

import { useConfigStoreWithOut } from './modules/config';

const store = createPinia();

// 设置 store
export function setupStore(app) {
  app.use(store);
}

// 初始化数据
export function initStore(initialData = {}) {
  const { theme, locale } = initialData;
  const configStore = useConfigStoreWithOut();

  // 设置配置信息
  configStore.setThemeType(theme);
  configStore.setLocaleType(locale);
}

export { store };
