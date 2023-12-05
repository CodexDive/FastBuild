module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ['plugin:vue/vue3-recommended', 'eslint:recommended', 'prettier'],
  parser: 'vue-eslint-parser',
  parserOptions: {
    // parser: 'vue-eslint-parser',
    ecmaVersion: 2020,
    sourceType: 'module',
    jsxPragma: 'React',
    warnOnUnsupportedTypeScriptVersion: false,
    ecmaFeatures: {
      jsx: true,
    },
    // babelOptions: {
    //   presets: ['@vue/babel-preset-jsx'],
    // },
  },
  plugins: ['vue', 'prettier'],
  rules: {
    'prettier/prettier': [
      'error',
      {
        printWidth: 100,
        semi: true,
        singleQuote: true,
        trailingComma: 'es5',
      },
    ],
    'vue/require-default-prop': 'off',
    'vue/attribute-hyphenation': 'off',
    'vue/no-v-html': 'off',
    'vue/multi-word-component-names': 'off',
    'no-console': ['error', { allow: ['warn', 'error', 'info'] }],
    'no-unused-vars': 'off',
    'vue/v-on-event-hyphenation': 'off',
  },
};
