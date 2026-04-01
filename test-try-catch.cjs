const fs = require('fs');
const path = require('path');
const serverPath = path.join(process.cwd(), 'skills/brainstorming/scripts/server.cjs');
let code = fs.readFileSync(serverPath, 'utf8');

code = code.replace(
  /if \(require\.main === module\) \{\n  startServer\(\)\.catch\(err => \{\n    console\.error\('Failed to start server:', err\);\n    process\.exit\(1\);\n  \}\);\n\}/,
  `if (require.main === module) {
  try {
    const result = startServer();
    if (result && typeof result.catch === 'function') {
      result.catch(err => {
        console.error('Failed to start server:', err);
        process.exit(1);
      });
    }
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
}`
);

fs.writeFileSync(serverPath, code);
