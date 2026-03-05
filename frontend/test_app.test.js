const { escapeHtml } = require('./utils.cjs');

test('escapeHtml échappe les caractères spéciaux', () => {
  expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
  expect(escapeHtml('"&<>')).toBe('&quot;&amp;&lt;&gt;');
});
