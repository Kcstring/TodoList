Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

appDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = appDir

' 0 = hidden, False = do not wait
shell.Run "cmd /c python main.py 1>>run.log 2>&1", 0, False
