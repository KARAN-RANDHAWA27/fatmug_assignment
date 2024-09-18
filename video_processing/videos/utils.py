import pysrt

def convert_srt_to_vtt(srt_file_path, vtt_file_path):
    subs = pysrt.open(srt_file_path)
    with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
        vtt_file.write("WEBVTT\n\n")
        for sub in subs:
            start_time = sub.start.to_time().strftime('%H:%M:%S.%f')[:-3]
            end_time = sub.end.to_time().strftime('%H:%M:%S.%f')[:-3]
            vtt_file.write(f"{start_time} --> {end_time}\n{sub.text}\n\n")
