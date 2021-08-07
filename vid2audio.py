# Created by: Manoj
# Date:18-06-2021
# Purpose:Generating audio from video

import moviepy.editor
video = moviepy.editor.VideoFileClip("sample.mp4")
audio = video.audio
audio.write_audiofile("sample.wav")
