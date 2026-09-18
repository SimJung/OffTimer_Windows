# OffTimer_Windows

Simple Windows shutdown timer.

## Features

- Add 10 minutes
- Add 1 hour
- Live remaining-time countdown
- Shows scheduled shutdown time
- Cancel scheduled shutdown
- Shut down immediately with confirmation
- Closing OffTimer normally cancels the scheduled Windows shutdown

## Build without installing anything

This repository includes a GitHub Actions workflow.

1. Upload the project files to the repository root.
2. Open **Actions** on GitHub.
3. Select **Build OffTimer**.
4. Click **Run workflow**.
5. When the run finishes, download the **OffTimer-Windows-x64** artifact.
6. Extract it to get `OffTimer.exe`.

The EXE is published as a self-contained Windows x64 single-file application.
