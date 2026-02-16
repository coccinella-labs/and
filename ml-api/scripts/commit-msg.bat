@echo off
REM Git commit-msg hook for Windows
REM Enforces conventional commit standards

setlocal enabledelayedexpansion

set "file=%1"
if not exist "%file%" (
    echo Error: Commit message file not found.
    exit /b 1
)

REM Read first line
set "first_line="
for /f "usebackq delims=" %%i in ("%file%") do (
    set "first_line=%%i"
    goto :check
)

:check
REM Check length
call :strlen result "%first_line%"
if %result% gtr 60 (
    echo Error: First line of commit message must be ≤60 characters.
    exit /b 1
)

REM Check if starts with type
echo %first_line% | findstr /r "^feat: ^fix: ^docs: ^style: ^refactor: ^test: ^chore: ^perf: ^ci: ^build: ^revert:" >nul
if errorlevel 1 (
    echo Error: Commit message must start with a conventional commit type followed by a space.
    exit /b 1
)

REM Check lowercase (approximate)
for /f "delims=" %%i in ('powershell -command "$s='%first_line%'; if ($s -ne $s.ToLower()) { exit 1 } else { exit 0 }"') do (
    if %%i equ 1 (
        echo Error: First line of commit message must be lowercase.
        exit /b 1
    )
)

exit /b 0

:strlen <resultVar> <stringVar>
(
    setlocal EnableDelayedExpansion
    set "s=!%~2!#"
    set "len=0"
    for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
        if "!s:~%%P,1!" NEQ "" (
            set /a "len+=%%P"
            set "s=!s:~%%P!"
        )
    )
    endlocal & set "%~1=%len%"
)
goto :eof