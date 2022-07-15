import random
from moviepy.editor import *


def get_random(folder, file_list):
    if folder == "Showcases":
        get = f"Showcases/{file_list[random.randint(0, len(file_list) - 1)]}"
        while not get.endswith(".mp4"):
            get = f"Showcases/{file_list[random.randint(0, len(file_list) - 1)]}"

        out = VideoFileClip(get)
        out = out.crop(
            x_center=out.size[0] / 2,
            y_center=out.size[1] / 2,
            width=out.size[0] / showcase_scale,
            height=out.size[1] / showcase_scale)
        out = out.speedx(factor=showcase_speed)
        return out
    else:
        get = f"{folder}/{file_list[random.randint(0, len(file_list) - 1)]}"
        while not get.endswith(".mp3"):
            get = f"{folder}/{file_list[random.randint(0, len(file_list) - 1)]}"

        return AudioFileClip(get)


def compose_multiple(duration, folder, file_list):
    current = get_random(folder, file_list)
    additional = get_random(folder, file_list)

    while current.duration < duration:
        if folder == "Showcases":
            additional = additional.fadein(fade_speed)
            current = current.fadeout(fade_speed * 1)

            current = concatenate_videoclips([current, additional])
        else:
            additional = additional.audio_fadein(fade_speed * 2)
            current = current.audio_fadeout(fade_speed * 2)

            current = concatenate_audioclips([current, additional])

    current = current.subclip(0, duration + 3)
    return current


def generate_transition():
    transition_music = compose_multiple(2, "TransitionMusic", os.listdir("TransitionMusic"))
    transition_music = transition_music.audio_fadeout(fade_speed * 1)

    transition = os.listdir("TransitionPreview")[random.randint(0, len(os.listdir("TransitionPreview")) - 1)]
    while not (transition.endswith(".png") or transition.endswith(".jpg")):
        transition = os.listdir("TransitionPreview")[random.randint(0, len(os.listdir("TransitionPreview")) - 1)]

    transition = ImageClip(f"TransitionPreview/{transition}", duration=5)
    transition.audio = transition_music

    return transition.fadein(fade_speed * 1).fadeout(fade_speed * 1)

is_transition = 1
showcase_scale = 1.3
showcase_speed = 1
music_volume = 0.05
fade_speed = 1


def logic(is_transition_i, showcase_scale_i, showcase_speed_i, music_volume_i, fade_speed_i, height, fps):
    is_transition = is_transition_i
    showcase_scale = showcase_scale_i
    showcase_speed = showcase_speed_i
    music_volume = music_volume_i
    fade_speed = fade_speed_i

    voices = sorted(os.listdir("Voice"))
    music = os.listdir("Music")
    showcases = os.listdir("Showcases")

    if len(voices) == 0 or len(showcases) == 0:
        return "Add content to folders !"

    result = None
    for i in voices:
        if not i.endswith(".mp3"): continue

        if not i == "00.mp3" and is_transition > 0:
            result = concatenate_videoclips([result, generate_transition()])

        cur_voice = AudioFileClip(f"Voice/{i}")
        cur_voice = cur_voice.set_start(1)

        cur_showcase = compose_multiple(cur_voice.duration + 1, "Showcases", showcases)
        cur_showcase = cur_showcase.fadein(fade_speed * 1).fadeout(fade_speed * 3)

        cur_music = compose_multiple(cur_voice.duration + 1, "Music", music)
        cur_music = cur_music.volumex(music_volume)

        cur_showcase.audio = CompositeAudioClip([cur_voice, cur_music])

        if result is not None:
            result = concatenate_videoclips([result, cur_showcase])
            continue

        result = cur_showcase

    width = int(height * 1.77777777778)
    result = result.resize((width, height))

    result.audio.write_audiofile('output.mp3', fps=44100)
    result.write_videofile('output.mp4', fps=fps, audio=False, threads=4, logger=None)

    result.close()
    return "Done!"
