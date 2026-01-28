const express = require('express')
const fs = require('fs')
const path = require('path')
const { spawn } = require('child_process')

const app = express()

app.use(express.static(__dirname + '/public'))
app.use('/build/', express.static(path.join(__dirname, 'node_modules/three/build')))
app.use('/jsm/', express.static(path.join(__dirname, 'node_modules/three/examples/jsm')))

function getEXRFiles(basePath, dir = '', arrayOfFiles = []) {
  const dirPath = basePath + dir
  if (!fs.existsSync(dirPath)) return [] 
  const files = fs.readdirSync(dirPath)

  files.forEach(function (file) {
    const fullPath = path.join(dirPath, file)
    const relPath = dir + file
    if (fs.statSync(fullPath).isDirectory())
      arrayOfFiles = getEXRFiles(basePath, relPath + '/', arrayOfFiles)
    else if (path.extname(file) === '.exr')
      arrayOfFiles.push(relPath)
  })
  return arrayOfFiles
}

app.get('/images', (req, res) => {
  const files = getEXRFiles(__dirname + '/public/textures/')
  res.json(files)
})

app.listen(3006, () => {
  console.log('Node Server: Visit http://127.0.0.1:3006')

  // --- PYTHON AUTOMATION ---

  // CORRECTION HERE:
  // If 'menu' is INSIDE the current folder (webapp), we use path.join without the '..'
  const menuPath = path.join(__dirname, 'menu');
  
  console.log(`📂 Looking for Python app in: ${menuPath}`);

  // 1. Detect Operating System
  const isWindows = process.platform === "win32";
  const pythonCmd = isWindows ? 'python' : 'python3';
  const pipCmd = isWindows ? 'pip' : 'pip3';

  // 2. Create the command
  const cdCmd = isWindows ? `cd /d "${menuPath}"` : `cd "${menuPath}"`;
  
  // Full command: enter directory -> install dependencies -> execute
  const fullCommand = `${cdCmd} && ${pipCmd} install nicegui fastapi uvicorn && ${pythonCmd} main.py`;

  console.log(`Executing command: ${fullCommand}`);

  const pythonProcess = spawn(fullCommand, {
    shell: true,
    stdio: 'inherit' 
  });

  pythonProcess.on('error', (err) => {
    console.error('Critical error launching process:', err);
  });

  pythonProcess.on('exit', (code) => {
    if (code !== 0 && code !== null) {
      console.error(`Python closed with error code: ${code}`);
      console.error(`   -> Check that the 'menu' folder actually exists inside 'webapp'.`);
    } else {
      console.log('Python closed successfully.');
    }
  });
})