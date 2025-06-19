# 📂 File Organizer Script (`fileorg.py`)

A simple Python script that organizes files in the same folder where it is placed. It categorizes files into subfolders like Documents, Images, Videos, etc., based on file extensions.

---

## 🧠 What It Does

- Organizes files in the **current folder** where `fileorg.py` is located.
- Automatically moves files into categorized subfolders:
  - **Documents**: `.txt`, `.pdf`, `.doc`, `.docx`
  - **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`
  - **Videos**: `.mp4`, `.mov`, `.avi`
  - **Music**: `.mp3`, `.wav`
  - **Archives**: `.zip`, `.rar`, `.7z`
  - **Installers**: `.dmg`, `.pkg`
  - **Applications**: `.app` (macOS bundles)
  - **Others**: Any other file types
- Skips organizing itself (`fileorg.py`)
- Creates folders automatically if they don’t exist
- Does **not** delete or modify file contents

---

## 🚀 How to Use

1. **Copy `fileorg.py`** into the unorganized folder you want to clean up.
2. **⚠️ Do not rename** the script — it must remain as `fileorg.py`.
3. Open a terminal and navigate to that folder:

    ```bash
    cd /path/to/your/unorganized-folder
    ```

4. Run the script:

    ```bash
    python3 fileorg.py
    ```

✅ Your files will be sorted into folders inside the same directory.

---

## 📦 Requirements

- Python 3.x
- No external libraries required (uses `os` and `shutil`)

---

## 📝 Notes

- Works on macOS, and can be adapted for Windows or Linux.
- `.app` files are treated as directories and moved accordingly.
- Only affects the contents of the folder it’s in.
