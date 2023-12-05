<template>
  <div>
    <a-button type="primary" @click="changeTheme">切换皮肤</a-button>
    <a-button type="primary" @click="changeLocale">切换多语言</a-button>
    <span>{{ $t('title') }}</span>
    <a-date-picker v-model:value="value1" />
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="../../assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>
<script setup>
import { ref, computed } from 'vue';

import HelloWorld from '@/components/HelloWorld.vue';
import { useConfigStoreWithOut } from '@/store/modules/config';

const value1 = ref();

const configStore = useConfigStoreWithOut();
const themeType = computed(() => configStore.getThemeType);
const localeType = computed(() => configStore.getLocaleType);

const changeTheme = () => {
  const color = ['dark', 'light'].find(item => item !== themeType.value);
  configStore.setThemeType(color);
};

const changeLocale = () => {
  const lang = ['enUS', 'zhCN'].find(item => item !== localeType.value);
  configStore.setLocaleType(lang);
};
</script>

<style lang="less" scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
