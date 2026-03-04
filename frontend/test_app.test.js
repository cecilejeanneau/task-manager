// Test simple du frontend avec Jest ou un navigateur (exemple)
test('escapeHtml échappe les caractères spéciaux', () => {
  const { escapeHtml } = require('./app.js');
  expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
  expect(escapeHtml('"&<>')).toBe('&quot;&amp;&lt;&gt;');
});
