import os
import srt
import time
from google.cloud import speech
credential_path = r"C:\Users\MANOJ KUMAR\Downloads\CODIIS\subtitle\subtitleapi\srtfile-319808-3672863852d9.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def long_running_recognize(args):

    # Transcribe long audio file from Cloud Storage using asynchronous speech recognition
    # Args: storage_uri URI for audio file in GCS, e.g. gs://[BUCKET]/[FILE]

    print("Transcribing {} ...".format(args.storage_uri))
    client = speech.SpeechClient()

    # Encoding of audio data sent.
    encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "enable_word_time_offsets": True,
        "enable_automatic_punctuation": True,
        "audio_channel_count": 2,
        "sample_rate_hertz": args.sample_rate_hertz,
        "language_code": args.language_code,
        "encoding": encoding,
    }
    audio = {"uri": args.storage_uri}

    operation = client.long_running_recognize(
        request={
            "config": config,
            "audio": audio,
        }
    )
    response = operation.result()

    subs = []

    for result in response.results:
        # First alternative is the most probable result
        subs = break_sentences(args, subs, result.alternatives[0])

    print("Transcribing completed")
    return subs


def break_sentences(args, subs, alternative):
    firstword = True
    charcount = 0
    idx = len(subs) + 1
    content = ""

    for w in alternative.words:
        if firstword:
            # first word in sentence, record start time
            start_hhmmss = time.strftime('%H:%M:%S', time.gmtime(
                w.start_time.seconds))
            start_ms = int(w.start_time.microseconds / 1000)
            start = start_hhmmss + "," + str(start_ms)

        charcount += len(w.word)
        content += " " + w.word.strip()

        if ("." in w.word or "!" in w.word or "?" in w.word or
                charcount > args.max_chars or
                ("," in w.word and not firstword)):
            # break sentence at: . ! ? or line length exceeded
            # also break if , and not first word
            end_hhmmss = time.strftime('%H:%M:%S', time.gmtime(
                w.end_time.seconds))
            end_ms = int(w.end_time.microseconds / 1000)
            end = end_hhmmss + "," + str(end_ms)
            subs.append(srt.Subtitle(index=idx,
                        start=srt.srt_timestamp_to_timedelta(start),
                        end=srt.srt_timestamp_to_timedelta(end),
                        content=srt.make_legal_content(content)))
            firstword = True
            idx += 1
            content = ""
            charcount = 0
        else:
            firstword = False
    return subs


def write_srt(args, subs):
    srt_file = args.out_file + ".srt"
    print("Writing {} subtitles to: {}".format(args.language_code, srt_file))
    f = open(srt_file, 'w')
    f.writelines(srt.compose(subs))
    f.close()
    return


def write_txt(args, subs):
    txt_file = args.out_file + ".txt"
    print("Writing text to: {}".format(txt_file))
    f = open(txt_file, 'w')
    for s in subs:
        f.write(s.content.strip() + "\n")
    f.close()
    return


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default="gs://bucket-in-1/test1.wav",
    )
    parser.add_argument(
        "--language_code",
        type=str,
        default="en-US",
    )
    parser.add_argument(
        "--sample_rate_hertz",
        type=int,
        default=44100,
    )
    parser.add_argument(
        "--out_file",
        type=str,
        default="test1",
    )
    parser.add_argument(
        "--max_chars",
        type=int,
        default=40,
    )

    args = parser.parse_args()

    subs = long_running_recognize(args)
    write_srt(args, subs)
    write_txt(args, subs)


if __name__ == "__main__":
    main()
