@echo off
REM ダウンロード自動整理 watcher を起動します（ダブルクリックでOK）。
REM 止めるには、このウィンドウで Ctrl+C、またはウィンドウを閉じる。
cd /d "%~dp0.."
title PD Download Watcher
py scripts\download_watcher.py
pause
