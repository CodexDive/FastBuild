<template>
  <prism-editor v-model="modelCode" class="prism-editor" :highlight="highlighter" v-bind="$attrs" />
</template>

<script>
import { computed } from 'vue';
import { PrismEditor } from 'vue-prism-editor';
import 'vue-prism-editor/dist/prismeditor.min.css';

import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-json';

export default {
  name: 'PrismCodeEditor',
  components: {
    PrismEditor,
  },
  props: {
    language: {
      type: String,
      default: 'bash',
    },
    code: {
      type: String,
    },
  },
  emits: ['update:code'],
  setup(props, { emit }) {
    const highlighter = code => {
      return highlight(code, languages[props.language]);
    };

    const modelCode = computed({
      get: () => props.code,
      set: value => emit('update:code', value),
    });

    return {
      highlighter,
      modelCode,
    };
  },
};
</script>
<style src="./style.less" />
