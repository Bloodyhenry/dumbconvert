/* DumbConvert.exe: starts the app with the Python that sits next to it (python\pythonw.exe -m simpleneg).
   Built by build.sh with zig; it only exists so there is a normal program to double-click, with an icon. */
#include <windows.h>
#include <stdio.h>
#include <wchar.h>

int WINAPI WinMain(HINSTANCE instance, HINSTANCE previous, LPSTR ansi_args, int show) {
    wchar_t dir[MAX_PATH];
    DWORD n = GetModuleFileNameW(NULL, dir, MAX_PATH);
    if (n == 0 || n >= MAX_PATH) return 1;
    wchar_t *slash = wcsrchr(dir, L'\\');
    if (slash) *slash = 0;

    /* what came after our own name on the command line (files dropped on the icon) */
    wchar_t *args = GetCommandLineW();
    if (*args == L'"') { args++; while (*args && *args != L'"') args++; if (*args) args++; }
    else { while (*args && *args != L' ' && *args != L'\t') args++; }
    while (*args == L' ' || *args == L'\t') args++;

    static wchar_t line[32768];
    _snwprintf(line, 32767, L"\"%ls\\python\\pythonw.exe\" -m simpleneg %ls", dir, args);
    line[32767] = 0;

    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof si);
    si.cb = sizeof si;
    if (!CreateProcessW(NULL, line, NULL, NULL, FALSE, 0, NULL, dir, &si, &pi)) {
        MessageBoxW(NULL, L"DumbConvert could not start: the python folder next to DumbConvert.exe is missing or damaged.",
                    L"DumbConvert", MB_ICONERROR | MB_OK);
        return 1;
    }
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return 0;
}
