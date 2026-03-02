import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from moviepy.editor import VideoFileClip, concatenate_videoclips
import threading
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

video_list = []


def add_videos():
    files = filedialog.askopenfilenames(
        filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv")]
    )

    for f in files:
        video_list.append(f)
        listbox.insert(tk.END, os.path.basename(f))


def remove_video():
    selected = listbox.curselection()
    if not selected:
        return

    index = selected[0]
    listbox.delete(index)
    video_list.pop(index)


def move_up():
    i = listbox.curselection()
    if not i:
        return
    i = i[0]
    if i == 0:
        return

    video_list[i], video_list[i - 1] = video_list[i - 1], video_list[i]

    text = listbox.get(i)
    listbox.delete(i)
    listbox.insert(i - 1, text)
    listbox.select_set(i - 1)


def move_down():
    i = listbox.curselection()
    if not i:
        return
    i = i[0]
    if i == len(video_list) - 1:
        return

    video_list[i], video_list[i + 1] = video_list[i + 1], video_list[i]

    text = listbox.get(i)
    listbox.delete(i)
    listbox.insert(i + 1, text)
    listbox.select_set(i + 1)


def merge_video():
    if not video_list:
        messagebox.showwarning("Lỗi", "Chưa chọn video")
        return

    output = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4", "*.mp4")]
    )

    if not output:
        return

    threading.Thread(target=process_merge, args=(output,)).start()


def process_merge(output):
    try:
        progress["value"] = 0
        root.update_idletasks()

        clips = []
        total = len(video_list)

        for i, path in enumerate(video_list):
            clips.append(VideoFileClip(path))
            progress["value"] = (i + 1) / total * 50
            root.update_idletasks()

        final = concatenate_videoclips(clips)

        progress["value"] = 70
        root.update_idletasks()

        final.write_videofile(output)

        progress["value"] = 100
        messagebox.showinfo("Xong", "Ghép video thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# ===== GUI =====
root = tk.Tk()
root.title("Auto Ghép Video")
root.geometry("500x400")

listbox = tk.Listbox(root, width=60, height=12)
listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Thêm Video", command=add_videos).grid(row=0, column=0)
tk.Button(btn_frame, text="Xóa", command=remove_video).grid(row=0, column=1)
tk.Button(btn_frame, text="↑", command=move_up).grid(row=0, column=2)
tk.Button(btn_frame, text="↓", command=move_down).grid(row=0, column=3)

tk.Button(root, text="GHÉP VIDEO", height=2,
          command=merge_video).pack(pady=10)

progress = Progressbar(root, length=400)
progress.pack(pady=10)

root.mainloop()