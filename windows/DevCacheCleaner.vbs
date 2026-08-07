Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
coreGuiPath = fso.BuildPath(scriptDir, "..\core\gui.py")

' Run pythonw silently without popping up command window
WshShell.Run "pythonw """ & coreGuiPath & """", 0, False
