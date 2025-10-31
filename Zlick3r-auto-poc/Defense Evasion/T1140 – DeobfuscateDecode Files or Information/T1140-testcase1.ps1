certutil -encode C:\Windows\System32\calc.exe %temp%\T1140_calc.txt
certutil -decode %temp%\T1140_calc.txt %temp%\T1140_calc_decoded.exe

