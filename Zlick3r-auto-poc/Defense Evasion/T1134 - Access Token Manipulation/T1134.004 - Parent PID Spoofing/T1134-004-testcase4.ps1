Get-CimInstance -ClassName Win32_Process -Property Name, CommandLine, ProcessId -Filter "Name = 'svchost.exe' AND CommandLine LIKE '%'" | Select-Object -First 1 | Start-ATHProcessUnderSpecificParent -FilePath $Env:windir\System32\WindowsPowerShell\v1.0\powershell.exe -CommandLine '-Command Start-Sleep 10'

