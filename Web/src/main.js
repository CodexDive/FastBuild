import { createApp } from 'vue';
import './style.less';
import App from './App.vue';

import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

import { initStore } from './store';
import { i18n } from '@/common/locale/useI18n';

import router from './router/index';

const app = createApp(App);
app.use(Antd);
app.use(i18n);
app.use(router);

initStore({ theme: 'light', locale: 'zhCN' });

app.mount('#app');
