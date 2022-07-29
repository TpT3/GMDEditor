import random
from moviepy.editor import *

class MainLogic():
    def __init__(self):
        self.is_transition = True
        self.fade_speed = 1
        self.transition_duration = 5

        self.showcase_scale = 1.3
        self.showcase_speed = 1

        self.music_volume = 0.05
        self.voice_volume = 1

        self.add_audio = True
        self.add_video = True

        self.audio_name = "output_audio"
        self.video_name = "output_video"

        self.height = 1080
        self.fps = 60

    def get_random(self, folder, file_list):
        if folder == "Showcases":
            get = f"Showcases/{file_list[random.randint(0, len(file_list) - 1)]}"
            while not get.endswith(".mp4"):
                get = f"Showcases/{file_list[random.randint(0, len(file_list) - 1)]}"

            out = VideoFileClip(get)
            out = out.crop(
                x_center=out.size[0] / 2,
                y_center=out.size[1] / 2,
                width=out.size[0] / self.showcase_scale,
                height=out.size[1] / self.showcase_scale)
            out = out.speedx(factor=self.showcase_speed)
            return out
        else:
            get = f"{folder}/{file_list[random.randint(0, len(file_list) - 1)]}"
            while not get.endswith(".mp3"):
                get = f"{folder}/{file_list[random.randint(0, len(file_list) - 1)]}"

            return AudioFileClip(get)

    def compose_multiple(self, duration, folder, file_list):
        current = self.get_random(folder, file_list)
        additional = self.get_random(folder, file_list)

        while current.duration < duration:
            if folder == "Showcases":
                additional = additional.fadein(self.fade_speed)
                current = current.fadeout(self.fade_speed * 1)

                current = concatenate_videoclips([current, additional])
            else:
                additional = additional.audio_fadein(self.fade_speed * 2)
                current = current.audio_fadeout(self.fade_speed * 2)

                current = concatenate_audioclips([current, additional])

        current = current.subclip(0, duration + 3)
        return current

    def generate_transition(self):
        transition_music = self.compose_multiple(2, "TransitionMusic", os.listdir("TransitionMusic"))
        transition_music = transition_music.audio_fadeout(self.fade_speed * 1)

        transition = os.listdir("TransitionPreview")[random.randint(0, len(os.listdir("TransitionPreview")) - 1)]
        while not (transition.endswith(".png") or transition.endswith(".jpg")):
            transition = os.listdir("TransitionPreview")[random.randint(0, len(os.listdir("TransitionPreview")) - 1)]

        transition = ImageClip(f"TransitionPreview/{transition}", duration=self.transition_duration)
        transition.audio = transition_music

        return transition.fadein(self.fade_speed * 1).fadeout(self.fade_speed * 1)

    def main(self):

        voices = sorted(os.listdir("Voice"))
        music = os.listdir("Music")
        showcases = os.listdir("Showcases")

        if len(voices) == 0 or len(showcases) == 0:
            return "Add content to folders!"

        result = None
        for i in voices:
            if not (i.endswith(".mp3") or i.endswith(".wav")): continue

            if not (i == "00.mp3") and self.is_transition and len(
                    os.listdir("TransitionPreview")) > 0:  # or i == "00.wav"
                result = concatenate_videoclips([result, self.generate_transition()])

            cur_voice = AudioFileClip(f"Voice/{i}")
            cur_voice = cur_voice.set_start(1)

            cur_showcase = self.compose_multiple(cur_voice.duration + 1, "Showcases", showcases)
            cur_showcase = cur_showcase.fadein(self.fade_speed * 1).fadeout(self.fade_speed * 3)

            cur_music = self.compose_multiple(cur_voice.duration + 1, "Music", music)
            cur_music = cur_music.volumex(self.music_volume)

            cur_showcase.audio = CompositeAudioClip([cur_voice, cur_music])

            if result is not None:
                result = concatenate_videoclips([result, cur_showcase])
                continue

            result = cur_showcase

        if result == None:
            return "No voice files! Use '.mp3' and '.wav'"

        width = int(int(self.height) * 1.77777777778)
        result = result.resize((width, self.height))

        if self.add_audio:
            result.audio.write_audiofile(
                f"{self.audio_name}.mp3",
                fps=44100
            )

        if self.add_video:
            result.write_videofile(
                f"{self.video_name}.mp4",
                fps=self.fps,
                audio=True, audio_fps=44100,
                codec="libx264",
                threads=4, logger=None
            )

        result.close()
        return "Done!"
