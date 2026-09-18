import subprocess
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

remaining_seconds = 0
shutdown_at = None
running = False

def run_shutdown(*args):
    subprocess.run(["shutdown", *args],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL,
                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

def add_time(seconds):
    global remaining_seconds, shutdown_at
    if running and shutdown_at is not None:
        remaining_seconds = max(0, int(shutdown_at - time.time()))
    remaining_seconds += seconds
    if running:
        shutdown_at = time.time() + remaining_seconds
        run_shutdown("/a")
        run_shutdown("/s", "/t", str(max(1, remaining_seconds)))
    update_display()

def start_timer():
    global running, shutdown_at
    if remaining_seconds <= 0:
        messagebox.showinfo("OffTimer", "먼저 +10분 또는 +1시간으로 시간을 설정해주세요.")
        return
    if running:
        return
    running = True
    shutdown_at = time.time() + remaining_seconds
    run_shutdown("/a")
    run_shutdown("/s", "/t", str(max(1, remaining_seconds)))
    update_display()

def pause_timer():
    global running, remaining_seconds, shutdown_at
    if not running:
        return
    if shutdown_at is not None:
        remaining_seconds = max(0, int(shutdown_at - time.time()))
    run_shutdown("/a")
    running = False
    shutdown_at = None
    update_display()

def cancel_timer():
    global running, remaining_seconds, shutdown_at
    run_shutdown("/a")
    running = False
    remaining_seconds = 0
    shutdown_at = None
    update_display()

def update_display():
    global remaining_seconds, running, shutdown_at
    if running and shutdown_at is not None:
        remaining_seconds = max(0, int(shutdown_at - time.time()))

    h = remaining_seconds // 3600
    m = (remaining_seconds % 3600) // 60
    s = remaining_seconds % 60
    time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    if running and shutdown_at is not None:
        status_label.config(text=f"실행 중 · 종료 예정 {datetime.fromtimestamp(shutdown_at):%H:%M:%S}")
    elif remaining_seconds > 0:
        status_label.config(text="일시정지")
    else:
        status_label.config(text="시간을 설정해주세요")

    root.after(250, update_display)

def on_closing():
    run_shutdown("/a")
    root.destroy()

root = tk.Tk()
root.title("OffTimer")
root.geometry("440x330")
root.resizable(False, False)

tk.Label(root, text="OffTimer", font=("맑은 고딕", 20, "bold")).pack(pady=(22, 3))
tk.Label(root, text="남은 시간", font=("맑은 고딕", 10)).pack()

time_label = tk.Label(root, text="00:00:00", font=("Consolas", 34, "bold"))
time_label.pack(pady=(3, 12))

time_buttons = tk.Frame(root)
time_buttons.pack()
tk.Button(time_buttons, text="+ 10분", width=14, height=2,
          command=lambda: add_time(600)).grid(row=0, column=0, padx=6)
tk.Button(time_buttons, text="+ 1시간", width=14, height=2,
          command=lambda: add_time(3600)).grid(row=0, column=1, padx=6)

control_buttons = tk.Frame(root)
control_buttons.pack(pady=14)
tk.Button(control_buttons, text="시작", width=10, height=2,
          command=start_timer).grid(row=0, column=0, padx=4)
tk.Button(control_buttons, text="일시정지", width=10, height=2,
          command=pause_timer).grid(row=0, column=1, padx=4)
tk.Button(control_buttons, text="취소", width=10, height=2,
          command=cancel_timer).grid(row=0, column=2, padx=4)

status_label = tk.Label(root, text="시간을 설정해주세요", font=("맑은 고딕", 10))
status_label.pack(pady=4)

root.protocol("WM_DELETE_WINDOW", on_closing)
update_display()
root.mainloop()
