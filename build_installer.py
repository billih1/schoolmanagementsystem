"""
Build script for School Management System
Compiles Python to .exe using PyInstaller and creates Windows installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuration
PROJECT_NAME = "School Management System"
PROJECT_VERSION = "1.0.0"
MAIN_SCRIPT = "src/main.py"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
SPEC_DIR = "."

def clean_previous_builds():
    """Remove previous build artifacts"""
    print("Cleaning previous builds...")
    for directory in [BUILD_DIR, OUTPUT_DIR, "*.spec"]:
        if os.path.isdir(directory):
            shutil.rmtree(directory, ignore_errors=True)
            print(f"  Removed {directory}")
        elif os.path.isfile(directory):
            os.remove(directory)
            print(f"  Removed {directory}")

def create_pyinstaller_spec():
    """Create PyInstaller spec file for better control"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    [r'{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt6', 'reportlab'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{PROJECT_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{PROJECT_NAME}',
)
'''

    spec_file = Path("SchoolManagementSystem.spec")
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    print(f"Created spec file: {spec_file}")

def build_executable():
    """Build executable using PyInstaller"""
    print(f"\nBuilding {PROJECT_NAME} executable...")
    print("=" * 60)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "--name", PROJECT_NAME,
        "--distpath", OUTPUT_DIR,
        "--buildpath", BUILD_DIR,
        "--specpath", SPEC_DIR,
        "--icon", "NONE",
        "--add-data", f"src:.",
        MAIN_SCRIPT
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Executable built successfully")
        return True
    else:
        print("✗ Build failed:")
        print(result.stderr)
        return False

def verify_executable():
    """Verify that executable was created"""
    exe_path = Path(OUTPUT_DIR) / PROJECT_NAME / f"{PROJECT_NAME}.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable verified: {exe_path}")
        print(f"  Size: {size_mb:.1f} MB")
        return exe_path
    else:
        print("✗ Executable not found")
        return None

def create_installer_script():
    """Create Inno Setup installer script"""
    installer_script = f'''
[Setup]
AppName={PROJECT_NAME}
AppVersion={PROJECT_VERSION}
AppPublisher=School Administration
AppPublisherURL=https://example.com
AppSupportURL=https://example.com/support
AppUpdatesURL=https://example.com/updates
DefaultDirName={{autopf}}\\{PROJECT_NAME}
DefaultGroupName={PROJECT_NAME}
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename={PROJECT_NAME}_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={{app}}\\{PROJECT_NAME}.exe
LicenseFile=
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
DisableProgramChangeAssociation=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1,6.1

[Files]
Source: "dist\\{PROJECT_NAME}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{{app}}"; Flags: isreadme

[Icons]
Name: "{{group}}\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"
Name: "{{group}}\\{{cm:UninstallProgram,{PROJECT_NAME}}}"; Filename: "{{uninstallexe}}"
Name: "{{commondesktop}}\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"; Tasks: desktopicon
Name: "{{commonappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{PROJECT_NAME}"; Filename: "{{app}}\\{PROJECT_NAME}.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{PROJECT_NAME}.exe"; Description: "{{cm:LaunchProgram,{PROJECT_NAME}}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{{app}}"
Type: filesandordirs; Name: "{{app}}\\*"

[Registry]
Root: HKA; Subkey: "Software\\{PROJECT_NAME}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\\{PROJECT_NAME}"; Flags: uninsdeletekey

[InstallDelete]
Type: filesandordirs; Name: "{{app}}"
'''

    installer_file = Path("installer") / f"{PROJECT_NAME}.iss"
    installer_file.parent.mkdir(parents=True, exist_ok=True)

    with open(installer_file, 'w') as f:
        f.write(installer_script)

    print(f"\nCreated Inno Setup script: {installer_file}")
    return installer_file

def create_installer():
    """Create Windows installer using Inno Setup"""
    print(f"\nCreating Windows installer...")
    print("=" * 60)

    # Check if Inno Setup is installed
    inno_path = Path("C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe")
    if not inno_path.exists():
        print("⚠ Inno Setup not found at:", inno_path)
        print("  Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php")
        print("  Or install via: winget install JetBrains.InnoSetup")
        return False

    installer_script = create_installer_script()

    cmd = [str(inno_path), str(installer_script)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Installer created successfully")
        return True
    else:
        print("✗ Installer creation failed:")
        print(result.stderr)
        return False

def create_portable_zip():
    """Create portable ZIP distribution"""
    print(f"\nCreating portable ZIP distribution...")
    exe_dir = Path(OUTPUT_DIR) / PROJECT_NAME
    zip_path = Path(OUTPUT_DIR) / f"{PROJECT_NAME}_Portable_{PROJECT_VERSION}"

    if exe_dir.exists():
        shutil.make_archive(str(zip_path), 'zip', OUTPUT_DIR, PROJECT_NAME)
        zip_file = Path(f"{zip_path}.zip")
        if zip_file.exists():
            size_mb = zip_file.stat().st_size / (1024 * 1024)
            print(f"✓ Portable ZIP created: {zip_file}")
            print(f"  Size: {size_mb:.1f} MB")
            return zip_file
    return None

def print_summary(exe_path, installer_created, portable_zip):
    """Print build summary"""
    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)

    if exe_path:
        print(f"✓ Executable: {exe_path}")
    else:
        print("✗ Executable not created")

    if installer_created:
        installer_path = Path("dist") / f"{PROJECT_NAME}_Setup.exe"
        print(f"✓ Installer: {installer_path}")
    else:
        print("⚠ Installer not created (Inno Setup may not be installed)")

    if portable_zip:
        print(f"✓ Portable ZIP: {portable_zip}")

    print("\nNext steps:")
    print("1. Test the executable: dist\\{} \\{}.exe".format(PROJECT_NAME, PROJECT_NAME))
    print("2. Distribute the installer or portable ZIP")
    print("3. Users can run SchoolManagementSystem_Setup.exe to install")
    print("\nDatabase location on user's system:")
    print("  %LOCALAPPDATA%\\SchoolManagementSystem\\data\\school.db")
    print("\nReports export location:")
    print("  %USERPROFILE%\\Documents\\School_Reports\\")
    print("=" * 60)

def main():
    """Main build script"""
    print(f"\n{'=' * 60}")
    print(f"Building {PROJECT_NAME} v{PROJECT_VERSION}")
    print(f"{'=' * 60}\n")

    # Check Python version
    if sys.version_info < (3, 10):
        print("✗ Error: Python 3.10+ required")
        sys.exit(1)

    # Check required packages
    required_packages = ['PyQt6', 'reportlab', 'PyInstaller']
    print("Checking dependencies...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} not installed")
            print(f"    Run: pip install {package}")
            sys.exit(1)

    # Build process
    clean_previous_builds()
    build_executable()
    exe_path = verify_executable()

    if not exe_path:
        print("\n✗ Build failed")
        sys.exit(1)

    # Create distributions
    installer_created = create_installer()
    portable_zip = create_portable_zip()

    # Print summary
    print_summary(exe_path, installer_created, portable_zip)

    print("\n✓ Build completed successfully!")

if __name__ == "__main__":
    main()
