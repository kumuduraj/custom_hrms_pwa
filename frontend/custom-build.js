const fs = require("fs-extra");
const path = require("path");
const { execSync } = require("child_process");

const hrmsFrontendPath = path.resolve(__dirname, "../../hrms/frontend");
const srcPath = path.resolve(__dirname, "./src");
const overridePath = path.resolve(__dirname, "./src_override");

console.log("=== Custom HRMS PWA Build ===\n");

// Step 1: Copy original HRMS frontend src
console.log("Step 1: Copying HRMS frontend source...");
if (fs.existsSync(srcPath)) {
  fs.removeSync(srcPath);
}
fs.copySync(path.join(hrmsFrontendPath, "src"), srcPath);
console.log("  ✓ HRMS source copied\n");

// Step 2: Apply overrides
console.log("Step 2: Applying overrides...");
if (fs.existsSync(overridePath)) {
  fs.copySync(overridePath, srcPath, { overwrite: true });
  console.log("  ✓ Overrides applied\n");
} else {
  console.log("  ⚠ No overrides found, using original source\n");
}

// Step 3: Install dependencies
console.log("Step 3: Installing dependencies...");
try {
  execSync("yarn install", { stdio: "inherit" });
  console.log("  ✓ Dependencies installed\n");
} catch (e) {
  console.log("  ⚠ Dependency installation had issues\n");
}

// Step 4: Build
console.log("Step 4: Building frontend...");
try {
  execSync("yarn build", { stdio: "inherit" });
  console.log("  ✓ Build complete\n");
} catch (e) {
  console.log("  ⚠ Build had issues\n");
}

console.log("=== Build Process Complete ===");
