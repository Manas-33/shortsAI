from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def process_transcript(input_data):
    processed_data = []
    i = 0

    while i < len(input_data):
        merged_text = []
        start_time = input_data[i]['start']
        for j in range(i, min(i + 3, len(input_data))):
            merged_text.append(input_data[j]['text'])

        if i + 3 < len(input_data):
            end_time = input_data[i + 3]['start']
        else:
            end_time = input_data[-1]['start'] + input_data[-1]['duration']

        processed_data.append([" ".join(merged_text), start_time, end_time])

        i += 3
    return processed_data

def get_transcript(url):
    video_id = extract_video_id(url)
    languages_array = [
        'en',
        'hi', 'bn', 'ta', 'te', 'mr', 'gu', 'pa', 'ml', 'kn', 'or', 'ur', 'as', 'bho', 'sa', 'ne', 'mai', 'sd', 'new', 'kha',
        'es', 'fr', 'de', 'zh-Hans', 'zh-Hant', 'ja', 'ru', 'ar', 'pt', 'tr', 'it', 'ko',
        'nl', 'pl', 'sv', 'el', 'da', 'fi', 'no', 'cs', 'hu', 'ro', 'bg', 'hr', 'sk', 'sl', 'uk', 'sr', 'mk', 'bs', 'is', 'ga', 'cy', 'mt', 'eo', 'gl', 'et', 'lv', 'lt',
        'fa', 'he', 'ku', 'ps', 'tg', 'tk', 'ky', 'uz', 'kk', 'az', 'hy', 'ka', 'ug',
        'vi', 'th', 'id', 'ms', 'tl', 'my', 'km', 'lo', 'mn',
        'sw', 'am', 'yo', 'ig', 'ha', 'zu', 'xh', 'rw', 'so', 'ss', 'st', 'tn', 'ts', 've', 'sn', 'rn', 'lg', 'sg',
        'sm', 'haw', 'mi', 'to', 'fj', 'dv', 'iu', 'om', 'ay', 'qu', 'war', 'pam', 'crs',
        'fo', 'fy', 'lb', 'mt', 'gd', 'gv', 'ny', 'ln', 'lg', 'ee', 'ak', 'br', 'co', 'os', 'tt', 'bo', 'ti', 'ts', 'tum', 'lua', 'luo', 'kri', 'gaa', 'mfe', 'nso', 'ab', 'aa', 'ba', 'dz', 'gn', 'ht', 'hmn', 'jv', 'kl', 'la', 'mg', 'om', 'oc', 'sd', 'su', 'yi', 'wo'
    ]
    segments = YouTubeTranscriptApi.get_transcript(video_id, languages=languages_array)
    processed_data = process_transcript(segments)
    return processed_data
