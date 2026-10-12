# SecureNotes

SecureNotes is an educational offline desktop application for managing encrypted personal notes. Built with Python and Dear PyGui, it demonstrates local data encryption, passphrase-based key derivation, and configurable read limits for sensitive information.

## Features

- **Local Note Encryption** – Note titles and contents are encrypted using AES-CBC before being saved to local JSON storage.
- **Passphrase-Derived Key** – The active GUI derives a 256-bit AES key from the user-provided master key using SHA-256.
- **Configurable Read Limits** – Notes can be configured with individual read limits and removed from the application's storage when the configured limit is exceeded.
- **Offline Operation** – The active desktop workflow does not require network connectivity.
- **Local Data Storage** – Encrypted note contents are stored in `notes_data.json`, while application preferences are stored in `settings.json`.
- **Customizable Interface** – Supports dark and light themes.

## Technology Stack

- Python 3.9+
- Dear PyGui
- PyCryptodome
- AES-CBC
- SHA-256
- JSON

## How It Works

### Encryption

The active GUI implementation derives an AES key by computing the SHA-256 digest of the user-provided master key. Notes are encrypted using AES-CBC with an initialization vector, and the IV and ciphertext are encoded in Base64 for storage.

### Storage

Note titles and contents are encrypted before being written to `notes_data.json`. Operational metadata, including read counters and configured read limits, remains in plaintext. The `settings.json` file stores application preferences and read-limit settings in plaintext.

### Read Limits and Deletion

Users can configure the maximum number of reads allowed for each note. When a note's read counter exceeds its configured limit, the application removes the note from its JSON-based storage.

This mechanism implements application-level deletion; it does not guarantee secure erasure of all copies or remnants from the underlying filesystem.

### Local Processing

The active GUI processes and stores notes locally without requiring a remote server or network connection. This reduces network exposure but does not, by itself, guarantee protection against local compromise or unauthorized access to the device.

## Project Structure

```text
SecureNotes-App/
├── app/
│   ├── gui/
│   │   ├── dialogs.py
│   │   ├── main_window.py
│   │   ├── styles.py
│   │   └── crypto_utils.py
│   ├── auth.py
│   ├── logic.py
│   ├── notes.py
│   └── utils.py
├── database/
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

**Implementation note:** `main.py` launches the GUI implemented in `app/gui/`. The repository also contains a separate SQLite-based implementation with authentication and Fernet encryption modules. These modules are not currently integrated into the GUI's execution path.

## Getting Started

### Requirements

- Python 3.9 or later
- pip

### Run from Source

Clone the repository and navigate to its directory. Then install the dependencies and start the application:

```bash
python -m pip install -r requirements.txt
python -m pip install pycryptodome
python main.py
```

## Build a Windows Executable

Install PyInstaller:

```bash
python -m pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile --windowed --icon=secure_notes.ico --name=SecureNotes main.py
```

The generated executable will be placed in the `dist/` directory.

## Security Scope and Limitations

SecureNotes is an educational project intended to demonstrate local encryption and desktop application development. The active GUI implementation currently has the following limitations:

- The passphrase-derived key uses direct SHA-256 hashing rather than a password-based key derivation function with a salt and configurable computational cost.
- AES-CBC does not provide built-in ciphertext authentication or integrity verification.
- Note metadata and application settings are stored in plaintext.
- The master key entered in the GUI is used as encryption input; it is not verified through a separate authentication mechanism.
- Read-limit deletion is an application-level mechanism, not guaranteed secure file erasure.

The application should not be treated as production-ready protection for highly sensitive information without further security improvements and testing.




