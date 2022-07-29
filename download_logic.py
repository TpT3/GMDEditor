import pytube
import os
import random

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# code written by Paranoik, edited by ppds

def get_channel_name(url):
    channel = pytube.Channel(url)
    return channel.channel_name


def download(showcases_length, showcases_resolution, showcases_channel, rand):
    while True:
        try:
            channel = pytube.Channel(showcases_channel)

            i = 0
            total = 0
            urls = list()
            while total < showcases_length:
                if rand:
                    video = channel.videos[random.randint(0, channel.videos.__len__() - 1)]
                else:
                    print(type(channel.videos))
                    video = channel.videos[i]
                total += video.length
                urls.append(video.watch_url)
                i += 1

                video = video.streams
                for v in video:
                    print(showcases_resolution)
                    if v.type == 'video' and v.resolution == showcases_resolution:
                        f = os.path.join(os.getcwd(), 'Showcases')
                        if not os.path.exists(f): os.mkdir(f)
                        v.download(f)
                        break

            return f'Done!\nYour total downloaded showcase time {total // 60} minutes {total % 60} seconds.'

        except Exception as err:
            return f'Oops! Some errors occurred:\n{err}'