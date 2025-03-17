from openai import OpenAI
import openai
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("OPENAI_API")
client = OpenAI(api_key=api_key)


def extract_times(json_string):
    try:
        data = json.loads(json_string)
        times = []
        for highlight in data:
            start_time = float(highlight["start"])
            end_time = float(highlight["end"])
            start_time_int = int(start_time)
            end_time_int = int(end_time)
            if start_time_int != end_time_int and start_time_int <  end_time_int:
                times.append((start_time_int, end_time_int))
        return times
    except Exception as e:
        print(f"Error in extract_times: {e}")
        return []


system = """
Based on the Transcription user provides extract 2 attention-grabbing highlights. 
Each highlight should be a short, engaging, and standalone segment that would perform well as a TikTok clip. 
Ensure that each clip is continuous and does not exceed a reasonable short-form content length. 
Prioritize moments with high emotional impact, surprising insights, humor, or compelling storytelling or something which is catchy and intersting to be viral. 

Follow this Format and return in valid json 
[{
start: "Start time of the clip",
content: "Highlight Text",
end: "End Time for the highlighted clip"
},
....
]

Use timestamps exactly as provided in the transcript. The response should strictly adhere to the specified JSON format, with no additional symbols, newline characters, or extraneous information. Dont say anything else, just return Proper Json. no explanation etc,

IF YOU DONT HAVE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESNT WORK THEN...
"""

User = """
Any Example
"""


def get_highlight(transcript):
    print("Getting Highlight from transcript ")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": transcript + system},
            ],
        )
        json_string = response.choices[0].message.content
        print(json_string)
        json_string = json_string.replace("json", "")
        json_string = json_string.replace("```", "")
        times = extract_times(json_string)
        if len(times) == 0:
            Ask = input("Error - Get Highlights again (y/n) -> ").lower()
            if Ask == "y":
                times = get_highlight(transcript)
        return times
    except Exception as e:
        print(f"Error in get_highlight: {e}")
        return []
