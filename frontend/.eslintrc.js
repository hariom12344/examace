module.exports = {
  parser: 'babel-eslint',
  extends: ['react-app'],
  rules: {
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'no-console': ['warn', { allow: ['warn', 'error'] }],
  },
}
