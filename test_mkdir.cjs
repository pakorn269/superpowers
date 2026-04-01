const fs = require('fs');
async function test() {
  await fs.promises.mkdir('/tmp/test_dir_mkdir', { recursive: true });
  await fs.promises.mkdir('/tmp/test_dir_mkdir', { recursive: true });
  console.log("Success!");
}
test();
