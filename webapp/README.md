# Application
## Install
1. Clone repository
2. pip install nicegui
3. `npm install` (to install three.js) TODO: Check if npm start is still needed for some configs?
Copy node_modules/three/build/three.module.js into it.

Copy the entire node_modules/three/examples/jsm folder into public.

## Run (dev mode)
`python main.py`

## Deploy
local machine
1. python deploy.py
2. rsync -avz --progress -e "ssh -J USERDPT@login1.cs.upc.edu" deploy/ USERUPC@mysgi.cs.upc.edu:/home/virvig/ASGI/mural-lighting
3. ssh USERDPT@login1.cs.upc.edu
4. ssh USERUPC@mysgi.cs.upc.edu
5. cd /home/virvig/ASGI/mural-lighting
6. sudo -u virvig bash
7. source /home/virvig/venv311/bin/activate
8. ENV=production python main.py



