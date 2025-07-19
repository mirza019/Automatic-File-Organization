# File Organizer GUI

A simple and intuitive graphical user interface (GUI) application to help you organize your files.

## Features

*   **Organize Today's Files:** Automatically moves files created on the current day into categorized folders (Documents, Images, Videos, Music, Archives, Installers, Applications, Others).
*   **Undo Last Organization:** Reverts the changes made by the most recent organization, moving files back to their original locations.
*   **Progress Bar:** Provides visual feedback on the organization process.
*   **Activity Log:** Displays real-time messages about files being moved.

## Requirements

*   Python 3.x
*   `tkinter` (usually included with Python installations)

## How to Use

1.  **Download the Script:**
    Save the `fileorg_gui.py` file to your desired directory (e.g., your Downloads folder).

2.  **Run the Application:**
    Open your terminal or command prompt, navigate to the directory where you saved the script, and run the following command:

    ```bash
    python3 fileorg_gui.py
    ```

    A new window titled "File Organizer" will appear.

3.  **Organize Today's Files:**
    Click the "Organize Today's Files" button. The application will scan the directory where the script is located and move files created on the current day into their respective subfolders. Progress will be shown in the progress bar, and details will appear in the activity log.

4.  **Undo Last Organization:**
    If you need to revert the last organization, click the "Undo Last Organization" button. This will move the files back to their original locations based on the last successful organization log.

## Developed by

Mirza Shaheen Iqubal
