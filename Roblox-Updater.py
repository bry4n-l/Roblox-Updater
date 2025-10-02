import os
import shutil
import time
import subprocess
import glob
import json

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

# Function to overwrite a file with retries for sharing violations
def overwrite_file(filepath, content, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            with open(filepath, 'w') as file:
                file.write(content)
            print(f"Overwritten: {filepath}")
            return True
        except PermissionError as e:
            if "sharing violation" in str(e).lower() or e.errno == 32:  # ERROR_SHARING_VIOLATION
                time.sleep(0.1)
                retries += 1
            else:
                print(f"Error overwriting {filepath}: {e}")
                return False
        except Exception as e:
            print(f"Error overwriting {filepath}: {e}")
            return False
    print(f"Failed to overwrite {filepath} after {max_retries} retries")
    return False

# Function to overwrite Roblox storage files for all users to autologout accounts
def overwrite_user_storage_files():
    json_placeholder = '{"placeholder": true}'
    dat_placeholder = '{"CookiesVersion":"1","CookiesData":""}'
    
    # Get all user directories
    user_dirs = glob.glob(r"C:\Users\*")
    
    for user_dir in user_dirs:
        if not os.path.isdir(user_dir):
            continue
        user_name = os.path.basename(user_dir)
        if user_name in ['.', '..', 'Public', 'Default']:  # Skip system dirs
            continue
        
        local_storage = os.path.join(user_dir, "AppData", "Local", "Roblox", "LocalStorage")
        if not os.path.exists(local_storage):
            continue
        
        # Overwrite appStorage.json
        app_storage_path = os.path.join(local_storage, "appStorage.json")
        if os.path.exists(app_storage_path):
            overwrite_file(app_storage_path, json_placeholder)
        
        # Overwrite memProfStorage*.json
        mem_prof_pattern = os.path.join(local_storage, "memProfStorage*.json")
        for mem_prof_file in glob.glob(mem_prof_pattern):
            if os.path.isfile(mem_prof_file):
                overwrite_file(mem_prof_file, json_placeholder)
        
        # Overwrite *.dat files
        dat_pattern = os.path.join(local_storage, "*.dat")
        for dat_file in glob.glob(dat_pattern):
            if os.path.isfile(dat_file):
                overwrite_file(dat_file, dat_placeholder)

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

# Overwrite storage files for all users to autologout
overwrite_user_storage_files()

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
