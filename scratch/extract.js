const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (match) {
  fs.writeFileSync('scratch/module_test.js', match[1]);
  console.log('Extracted successfully, bytes:', match[1].length);
} else {
  console.log('No module script found');
}
