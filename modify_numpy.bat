@echo off
setlocal enabledelayedexpansion

REM Define the starting directory (current directory)
set start_dir=%cd%

REM Define variables to store directory paths
set skvideo_io_dir=

REM Search for the skvideo\io directory
echo Searching for skvideo\io directory in %start_dir% and its subdirectories...

for /r "%start_dir%" %%d in (skvideo) do (
    if exist "%%d\io" (
        set skvideo_io_dir=%%d\io
        echo Found skvideo\io directory at %%d\io
        goto :found_skvideo_io
    )
)

echo skvideo\io directory not found.
goto :end

:found_skvideo_io
REM Traverse the skvideo\io directory to find abstract.py
echo Searching for abstract.py in %skvideo_io_dir% and its subdirectories...

for /r "%skvideo_io_dir%" %%f in (abstract.py) do (
    echo Found abstract.py at %%f. Modifying...
    powershell -Command "(Get-Content %%f) -replace 'np.int', 'int' -replace 'np.float', 'float' | Set-Content %%f"
)

echo Modification complete.

:end
endlocal
