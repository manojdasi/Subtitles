# Created by: Arjith, Ram and Manoj
# Date:19-06-2021
# Purpose:Generating subtitles for videos using srt file

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip


def generator(txt): return TextClip(
    txt, font='Arial', fontsize=16, color='white')


subtitles = SubtitlesClip("test1.srt", generator)

video = VideoFileClip("test1.mov")
result = CompositeVideoClip([video, subtitles.set_pos(('center', 'bottom'))])

result.write_videofile("test1_sub.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a",
                       remove_temp=True, codec="libx264", audio_codec="aac")
