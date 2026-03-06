import os
import shutil

def build_deploy():
    deploy_dir = "deploy"
    
    # 1. Clean up old deploy folder if it exists
    if os.path.exists(deploy_dir):
        print(f"Cleaning up old '{deploy_dir}' folder...")
        shutil.rmtree(deploy_dir)
    
    os.makedirs(deploy_dir)
    print(f"Created fresh '{deploy_dir}' folder.")

    # 2. List exactly what needs to go to the server
    items_to_copy = [
        "main.py",
        "requirements.txt",
        "public", # Your Three.js frontend and textures
        "menu"    # Your NiceGUI assets (if this is a separate folder)
        # Add any other specific Python files or folders here if you have them
    ]

    # 3. Copy the items
    for item in items_to_copy:
        if os.path.exists(item):
            dest = os.path.join(deploy_dir, item)
            if os.path.isdir(item):
                shutil.copytree(item, dest)
                print(f"📁 Copied directory: {item}")
            else:
                shutil.copy2(item, dest)
                print(f"📄 Copied file: {item}")
        else:
            print(f"⚠️  Warning: '{item}' not found locally, skipping.")

    print("\n✅ Build complete! Your 'deploy' folder is ready.")
    print("Run your rsync command to push it to the server.")

if __name__ == "__main__":
    build_deploy()