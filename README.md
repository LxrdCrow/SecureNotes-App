# 🔐 SecureNotes

A lightweight, secure, and offline-friendly desktop application for managing encrypted personal notes. Powered by **Python**, **Dear PyGui**, and a touch of cryptographic magic.

> ✨ Developed with a focus on privacy, usability, and self-destruction of sensitive notes after a set number of reads.

---

## 📦 Features

- 🔑 **Master Key Encryption** – Notes are locally encrypted using a key derived from your password.
- 📋 **Per-Note Read Limits** – Configure how many times each note can be read before it auto-deletes.
- 🎨 **Dark & Light Themes** – Switch between light and dark mode from the settings.
- 🧠 **No Internet Required** – Everything runs 100% locally.
- 🧼 **Secure Data Storage** – Notes and settings are stored in JSON files, encrypted with AES.

---

## 🚀 How to Run

### 🔧 Option 1: Run the `.exe` (recommended for end users)

1. Download the latest `SecureNotes.exe` from the `dist/` folder or release page.
2. Double click to launch.
3. If Windows Defender blocks it:
   - Click **"More Info"**
   - Then click **"Run Anyway"**

✅ No installation needed. No admin rights required.

---

### 💻 Option 2: Run from source (for developers)

#### Requirements
- Python 3.9+
- `pip install -r requirements.txt`

```bash
python main.py
````

---

## 🔒 How it Works

* **Encryption**: Notes are encrypted with AES using a key derived from the Master Key via PBKDF2.
* **Storage**: Notes are saved in `notes_data.json`, and app settings in `settings.json`. Both are plaintext but contain encrypted data.
* **Auto-deletion**: Once a note exceeds its max read count, will be deleted permanently from the app.
* **Everything happens locally** – no servers, no network, no data leaks.

---

## 📁 Project Structure

```
SecureNotes-App/
│
├── app/
│   ├── auth.py
│   ├── notes.py
│   ├── utils.py
│   ├── logic.py
│   └── gui/
│       ├── dialogs.py
│       ├── main_window.py
│       ├── styles.py
│       └── crypto_utils.py
│
├── database/
│   ├── database.py
│   ├── init_db.py
│   └── schema_sqlite.sql
│
├── config.py
├── main.py
├── .env
├── secure_notes.ico
├── README.md
```

---

## 🧪 Developer Notes

### Build executable with PyInstaller:

```bash
pyinstaller --onefile --windowed --icon=secure_notes.ico --name=SecureNotes main.py
```

### Notes:

* If the app is blocked on Windows SmartScreen, instruct users to click **"More info" > Run anyway**.
* To avoid triggering antivirus false positives, you can sign the executable (optional, but requires a certificate).




