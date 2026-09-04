[Setup]
AppName=School Management System
AppVersion=1.0.0
AppPublisher=School Administration
AppPublisherURL=https://schoolmanagementsystem.local
AppSupportURL=https://schoolmanagementsystem.local/support
AppUpdatesURL=https://schoolmanagementsystem.local/updates
DefaultDirName={autopf}\School Management System
DefaultGroupName=School Management System
AllowNoIcons=no
OutputDir=dist
OutputBaseFilename=SchoolManagementSystem_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\SchoolManagementSystem.exe
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
DisableProgramChangeAssociation=yes
WizardStyle=modern
WizardResizable=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1,6.1
Name: "createstartmenu"; Description: "Create Start Menu shortcuts"; Flags: checked

[Files]
Source: "dist\School Management System\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\School Management System"; Filename: "{app}\SchoolManagementSystem.exe"; Comment: "School Management System"
Name: "{group}\{cm:UninstallProgram,School Management System}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\School Management System"; Filename: "{app}\SchoolManagementSystem.exe"; Tasks: desktopicon; Comment: "School Management System"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\School Management System"; Filename: "{app}\SchoolManagementSystem.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\SchoolManagementSystem.exe"; Description: "Launch School Management System"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"

[Registry]
Root: HKCU; Subkey: "Software\School Management System"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\School Management System"; ValueType: string; ValueName: "DisplayName"; ValueData: "School Management System"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\School Management System"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "1.0.0"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\School Management System"; ValueType: string; ValueName: "UninstallString"; ValueData: "{app}\unins000.exe"

[Code]
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;
