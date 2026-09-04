# How to Run the School Management System

## Option 1: Using Batch File (Recommended for Windows)

Simply double-click:
```
run.bat
```

This will:
1. Activate the virtual environment
2. Run the application
3. Open the GUI window

## Option 2: Using PowerShell

```powershell
.\run.ps1
```

(You may need to allow script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)

## Option 3: Manual Command Line (PowerShell)

```powershell
cd C:\Users\Ali\SchoolManagementSystem
.\venv\Scripts\Activate.ps1
python src/main.py
```

## First Time Setup

If you haven't installed dependencies yet:

```powershell
cd C:\Users\Ali\SchoolManagementSystem
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py
```

## What Should Happen

1. A command window opens (briefly)
2. The application initializes (you'll see messages)
3. The School Management System GUI window appears
4. You can now use the application!

## Troubleshooting

**"Command not found"** - Make sure you're in the correct directory: `C:\Users\Ali\SchoolManagementSystem`

**"venv not found"** - Create it first:
```powershell
python -m venv venv
```

**"Module not found"** - Install dependencies:
```powershell
pip install -r requirements.txt
```

## Database & Data

On first run:
- Database created at: `%LOCALAPPDATA%\SchoolManagementSystem\data\school.db`
- Backups saved to: `%LOCALAPPDATA%\SchoolManagementSystem\backups\`
- Reports exported to: `%USERPROFILE%\Documents\School_Reports\`

All data persists between sessions!
