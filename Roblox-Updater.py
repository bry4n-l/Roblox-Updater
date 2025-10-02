import os
import shutil
import time
import subprocess

# Function to delete old Roblox version folders for a specific executable, keeping the most recent one
def delete_old_versions_for_exe(versions_path, target_exe):
    version_folders = []
    
    # Get all folders starting with "version-" in the Versions directory
    for folder in os.listdir(versions_path):
        if folder.startswith("version-"):
            folder_path = os.path.join(versions_path, folder)
            if os.path.isdir(folder_path) and target_exe in os.listdir(folder_path):
                # Store folder path and its last modification time
                mtime = os.path.getmtime(folder_path)
                version_folders.append((folder_path, mtime))
    
    # Sort folders by modification time (newest first)
    version_folders.sort(key=lambda x: x[1], reverse=True)
    
    # Keep the most recent folder, delete the rest
    if len(version_folders) > 1:
        for folder_path, _ in version_folders[1:]:  # Skip the first (newest) folder
            try:
                shutil.rmtree(folder_path)
                print(f"Deleted old version folder for {target_exe}: {folder_path}")
            except Exception as e:
                print(f"Error deleting {folder_path}: {e}")

# Original code follows (copy and replace first)
def copy_and_replace(source_path, destination_path):
    if os.path.exists(destination_path):
        os.remove(destination_path)
    shutil.copy2(source_path, destination_path)

# Source and destination file paths
source_file = 'W:\\Roblox\\appStorage.json'
destination_file = 'W:\\Roblox\\AppData\\Local\\Roblox\\LocalStorage\\appStorage.json'

# Copy and replace
copy_and_replace(source_file, destination_file)

time.sleep(0.5)

# Path to Roblox Versions directory
versions_path = "W:\\Roblox\\AppData\\Local\\Roblox\\Versions"

verList = os.listdir(versions_path)

path = ""

for i in verList:
    prefix = i.split("-")[0]
    
    if prefix == "version":
        candidate_path = os.path.join(versions_path, i)
        
        if "RobloxPlayerInstaller.exe" in os.listdir(candidate_path):
            path = candidate_path
            break

# Run the installer and wait for it to complete
if path:
    installer_path = os.path.join(path, "RobloxPlayerInstaller.exe")
    print(f"Running installer: {installer_path}")
    process = subprocess.Popen([installer_path])
    process.wait()  # Wait for the installer to finish
    print("Installer completed.")

# Now delete old version folders after update
delete_old_versions_for_exe(versions_path, "RobloxPlayerBeta.exe")
delete_old_versions_for_exe(versions_path, "RobloxStudioBeta.exe")
