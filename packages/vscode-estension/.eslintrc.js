module.exports = {
  env: {
    es2021: true,
    node: true,
  },
  extends: ['airbnb'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    'no-use-before-define': 0,
    'import/no-extraneous-dependencies': 0,
    'import/extensions': 0,
    'linebreak-style': 0,
  },
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.ts'],
      },
    },
  },
};
