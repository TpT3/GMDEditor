from tkinter import *
from logic import logic
import os
import json


root = Tk()
bg_c = '#2F3136'
root['bg'] = bg_c
text_c = 'white'
root.title('GMD Editor')
root.resizable(width=False, height=False)


def parameter(text, default, row=0, column=0):
    Label(
        text=text, font="Arial 15",
        fg=text_c, bg=bg_c,
    ).grid(row=row, column=column, columnspan=1, padx=3, pady=4)

    entry = Entry(
        width=10, bd=4,
        relief=FLAT,
        highlightthickness=0,
        highlightcolor=text_c,
        fg=text_c, bg='#3d4047'
    )
    entry.insert(0, default)
    entry.grid(row=row, column=column + 1)

    return entry


def check_folder(folder):
    cwd = os.getcwd()
    dir = os.path.join(cwd, folder)
    if not os.path.exists(dir): os.mkdir(dir)


def start_logic():
    with open('parameters.json', 'w') as wf:
        wf.write(json.dumps({
            'transition': is_transition_i.get(),
            'scale': showcase_scale_i.get(),
            'speed': showcase_speed_i.get(),
            'volume': music_volume_i.get(),
            'fade': fade_speed_i.get(),
            'height': height_i.get(),
            'fps': fps_i.get()
        }))
        wf.close()

    Label(text=logic(
        int(is_transition_i.get()),
        float(showcase_scale_i.get()),
        float(showcase_speed_i.get()),
        float(music_volume_i.get()),
        float(fade_speed_i.get()),
        int(height_i.get()),
        int(fps_i.get())
    ), bg=bg_c, fg=text_c).grid(row=11, column=0, pady=4)


def setup_folders():
    check_folder("Voice")
    check_folder("Showcases")
    check_folder("Music")
    check_folder("TransitionMusic")
    check_folder("TransitionPreview")


if not os.path.exists('parameters.json'):
    with open('parameters.json', 'w') as wf:
        wf.write(json.dumps({
            'transition': '1',
            'scale': '1.3',
            'speed': '1',
            'volume': '0.05',
            'fade': '1',
            'height': '1080',
            'fps': '60'
        }))
        wf.close()

data = ""
with open('parameters.json', 'r', encoding='utf-8') as sf:
    data = json.load(sf)
    sf.close()

print(data)

Label(text="Setup your Video", font="Arial 20 bold", bg=bg_c, fg=text_c).grid(row=1, column=0, pady=4)


Label(
    text="Add transitions", font="Arial 15",
    fg=text_c, bg=bg_c,
).grid(row=2, column=0, columnspan=1, padx=3, pady=4)

is_transition_i = BooleanVar()
is_transition_i.set(data['transition'])
Checkbutton(
    variable=is_transition_i, text="T/F", fg=text_c,
    onvalue=1, offvalue=0, width=11, bd=4,
    relief=FLAT, highlightthickness=0, highlightcolor=text_c,  bg='#3d4047'
).grid(row=2, column=1)


showcase_scale_i = parameter("Showcase size",  data['scale'], row=3, column=0)
showcase_speed_i = parameter("Showcase speed", data['speed'], row=4, column=0)
music_volume_i = parameter("Music volume", data['volume'], row=5, column=0)
fade_speed_i = parameter("Fade speed", data['fade'], row=6, column=0)

Label(text="Setup Render", font="Arial 20 bold", bg=bg_c, fg=text_c).grid(row=7, column=0, pady=4)

height_i = parameter("Video width (144, 240, 360 etc.)", data['height'], row=8, column=0)
fps_i = parameter("Frame rate", data['fps'], row=9, column=0)

sf.close()

Button(
    text="Start",
    width=5, height=2,
    command=start_logic,
    highlightthickness=0,
).grid(row=10, column=1, pady=4, padx=4)

Button(
    text="Setup folders for content",
    height=2,
    command=setup_folders,
    highlightthickness=0,
).grid(row=10, column=0, pady=4, padx=4)

root.mainloop()
