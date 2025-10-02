# Roblox Version Updater and Cleanup Script

## Overview
This Python script automates the process of updating Roblox (specifically the Player and Studio Beta versions) by running the latest `RobloxPlayerInstaller.exe`, waiting for the update to complete, and then cleaning up old version folders to save disk space. It targets folders in the Roblox Versions directory that follow the pattern `version-[random-string]`.

Additionally, it overwrites Roblox storage files (`appStorage.json`, `memProfStorage*.json`, and `*.dat`) for **all users** on the system to force autologout of accounts, clearing persistent login data.

The script is designed to:
- Avoid deleting the active or newly created version folders during updates.
- Handle both `RobloxPlayerBeta.exe` and `RobloxStudioBeta.exe` independently.
- Use folder modification times to determine which versions are "oldest" (not the random numbers in folder names).
- Apply autologout changes across multiple user profiles safely with retries for file locks.

**Note:** This script assumes Roblox is installed on drive `W:\Roblox\AppData\Local\Roblox`. Adjust paths if your setup differs. The autologout feature affects all users—use with caution in multi-user environments.

## Requirements
- Python 3.x
- Standard libraries: `os`, `shutil`, `time`, `subprocess`, `glob`, `json` (all included by default)

No external packages needed.

## Usage
1. Save the script as `roblox_updater.py` (or similar).
2. Run it via command line:
3. The script will:
- Copy `appStorage.json` from `W:\Roblox\` to the Roblox LocalStorage directory.
- Overwrite storage files for all users to force autologout.
- Locate and run the most recent `RobloxPlayerInstaller.exe`.
- Wait for the installer to finish (this triggers the update).
- Delete old version folders for Player and Studio Beta, keeping only the newest one for each.

**Output Example:**
```
Running installer: W:\Roblox\AppData\Local\Roblox\Versions\version-494828652c274712-12\RobloxPlayerInstaller.exe
Installer completed.
Deleted old version folder for RobloxPlayerBeta.exe: W:\Roblox\AppData\Local\Roblox\Versions\version-31fc142272764f02
Deleted old version folder for RobloxPlayerBeta.exe: W:\Roblox\AppData\Local\Roblox\Versions\version-494828652c274712-12
```

## How It Works
### 1. File Copy (appStorage.json)
- Copies a custom `appStorage.json` file to Roblox's LocalStorage to override settings (e.g., for custom configurations).
- Uses `shutil.copy2` to preserve metadata.

### 2. Overwrite Storage Files for Autologout
- Scans all user directories in `C:\Users\*`.
- For each user, overwrites:
  - `appStorage.json` with `{"placeholder": true}`.
  - `memProfStorage*.json` files with the same placeholder.
  - `*.dat` files with `{"CookiesVersion":"1","CookiesData":""}`.
- Includes retries for file sharing violations (e.g., if Roblox is running).

### 3. Locate and Run Installer
- Scans the `Versions` directory for folders starting with `version-`.
- Finds the first folder containing `RobloxPlayerInstaller.exe` (assumed to be the current/latest one).
- Launches it using `subprocess.Popen` and waits with `process.wait()` to ensure the update completes before proceeding.

### 4. Cleanup Old Versions
- For each target executable (`RobloxPlayerBeta.exe` and `RobloxStudioBeta.exe`):
  - Collects all `version-` folders containing that `.exe`.
  - Sorts them by folder modification time (newest first) using `os.path.getmtime`.
  - Deletes all but the most recent folder using `shutil.rmtree`.
- This prevents accidental deletion of the active/newly updated folder.

### Key Functions
- **`delete_old_versions_for_exe(versions_path, target_exe)`**: Core cleanup logic. Filters folders by the presence of the target `.exe`, sorts by mod time, and removes extras.
- **`overwrite_user_storage_files()`**: Handles autologout by overwriting storage files across all users.
- **`overwrite_file(filepath, content)`**: Writes content to a file with retries for locks.
- **`copy_and_replace(source_path, destination_path)`**: Simple file copy with overwrite.

## Potential Issues & Notes
- **Permissions:** Run as administrator if Roblox folders are locked or to access other users' data.
- **Multi-User Impact:** The autologout feature modifies all users' Roblox storage—test in a controlled environment.
- **No New Folder Check:** If the update fails to create a new folder, the script might delete the current one—monitor the first run.
- **Customization:** 
  - Add more executables by calling `delete_old_versions_for_exe` with new targets.
  - Change paths at the top of the script.
  - Modify placeholders in `overwrite_user_storage_files` for different behaviors.
- **Why Mod Time?** Folder names use random strings (e.g., `version-494828652c274712`), so timestamps provide a reliable "age" indicator.

## License
Feel free to use/modify for personal use. Credit if shared!

---

*Last Updated: October 02, 2025*
