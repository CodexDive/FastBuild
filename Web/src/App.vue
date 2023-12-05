<template>
  <a-config-provider :locale="locale" :theme="themeConfig">
    <router-view></router-view>
  </a-config-provider>
</template>
<script setup>
import { computed } from 'vue';

import { useTheme } from '@/common/theme/useTheme';
import { useLocale } from '@/common/locale/useLocale';
import { useI18n } from '@/common/locale/useI18n';
import { useConfigStoreWithOut } from '@/store/modules/config';

const configStore = useConfigStoreWithOut();
const themeConfig = computed(() => configStore.getThemeConfig);

const locale = computed(() => {
  const name = configStore.localeConfig;
  return name;
});

useTheme();
useLocale();
useI18n();
</script>
