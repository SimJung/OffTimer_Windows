import subprocess
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

shutdown_at = None


def run_shutdown(*args):
    subprocess.run(
        ["shutdown", *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def schedule_shutdown(add_seconds):
    global shutdown_at

    if shutdown_at is not None:
        remaining = max(0, int(shutdown_at - time.time()))
    else:
        remaining = 0

    total_seconds = remaining + add_seconds
    shutdown_at = time.time() + total_seconds

    run_shutdown("/a")
    run_shutdown("/s", "/t", str(total_seconds))
    update_display()


def cancel_shutdown():
    global shutdown_at
    run_shutdown("/a")
    shutdown_at = None
    update_display()


def shutdown_now():
    if messagebox.askyesno("시스템 종료", "정말 지금 컴퓨터를 종료하시겠습니까?"):
        run_shutdown("/s", "/t", "0")


def update_display():
    global shutdown_at

    if shutdown_at is None:
        time_label.config(text="00:00:00")
        status_label.config(text="예약된 종료 없음")
    else:
        remaining = max(0, int(shutdown_at - time.time()))

        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        shutdown_time = datetime.fromtimestamp(shutdown_at)
        status_label.config(text=f"종료 예정  {shutdown_time:%H:%M:%S}")

        if remaining <= 0:
            shutdown_at = None

    root.after(500, update_display)


def on_closing():
    global shutdown_at
    # 정상 종료 시 Windows 예약 종료도 초기화
    run_shutdown("/a")
    shutdown_at = None
    root.destroy()


root = tk.Tk()
root.title("OffTimer")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(
    root, text="OffTimer", font=("맑은 고딕", 18, "bold")
).pack(pady=(25, 5))

tk.Label(
    root, text="남은 시간", font=("맑은 고딕", 10)
).pack()

time_label = tk.Label(
    root, text="00:00:00", font=("Consolas", 32, "bold")
)
time_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="+ 10분",
    width=12,
    height=2,
    command=lambda: schedule_shutdown(10 * 60),
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="+ 1시간",
    width=12,
    height=2,
    command=lambda: schedule_shutdown(60 * 60),
).grid(row=0, column=1, padx=5)

action_frame = tk.Frame(root)
action_frame.pack()

tk.Button(
    action_frame, text="예약 취소", width=12, command=cancel_shutdown
).grid(row=0, column=0, padx=5)

tk.Button(
    action_frame, text="지금 종료", width=12, command=shutdown_now
).grid(row=0, column=1, padx=5)

status_label = tk.Label(
    root, text="예약된 종료 없음", font=("맑은 고딕", 10)
)
status_label.pack(pady=15)

root.protocol("WM_DELETE_WINDOW", on_closing)
update_display()
root.mainloop()
