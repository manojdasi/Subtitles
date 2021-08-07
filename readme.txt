Subtile generation to english movies:
  Generation of subtitles to any english movie in real time.

Requirements:
     1. srt library used for parsing, modifying and composing SRT files.
     2. Time is a library for dealing with time conversions between universal time and arbitrary timezones.
     3. google-cloud is a API client library for Google Cloud.
     4. Moviepy is a video editing with python.

This generation of subtitles to a video is done in 3 steps:
    1. Convert video to audio(.wav) by changing file format.
    2. Convert audio file to srt(SubRip Subtitle)
    3. Add srt file to the original video which displays subtiles in the end

Generation of srt file:
1. Open google cloud platform account and enable billing for "Cloud-speech-to-text" and then create buckets in cloud storage to upload videos over there. Follow this link to set up everything: https://www.youtube.com/watch?v=uBzp5xGSZ6o
2. Run speech2srt.py to get srt file.
3. Run srtsubs_video.py to add srt file to the video.
