import tkinter as tk
from tkinter import simpledialog, filedialog
import os

DATA_FOLDER = "data"

def run_action(action):
    print("Running:", action)

    os.system("python Video_inserted/live_child.py")
    os.system(f"python Video_inserted/compare_live.py {action}")


def start_training():
    actions = os.listdir(DATA_FOLDER) 

    win = tk.Toplevel(root)
    win.title("Choose Action")

    for action in actions:
        btn = tk.Button(win, text=action,
                        command=lambda a=action: run_action(a))
        btn.pack(pady=5)


def add_action():
    action_name = simpledialog.askstring("Action Name", "Enter action name:")

    if not action_name:
        return

    choice = simpledialog.askstring(
        "Add Action",
        "1 = Record Video\n2 = Choose File"
    )

    video_path = ""

    if choice == "1":
        print("Recording video...")
        os.system(f'python Video_from_parent/record_video.py "{action_name}"')
        video_path = f"Videos/{action_name}.mp4"
       

    elif choice == "2":
        file_path = filedialog.askopenfilename(
            title="Choose Video",
            filetypes=[("Video Files", "*.mp4 *.avi")]
        )

        if not file_path:
            return

        video_path = file_path

    else:
        return

    print("Building reference...")

    os.system(f'python Video_inserted/build_reference.py "{video_path}" "{action_name}"')

root = tk.Tk()
root.title("AI Training App")

tk.Button(root, text="Start Training", command=start_training).pack(pady=20)
tk.Button(root, text="Add New Action", command=add_action).pack(pady=20)

root.mainloop()