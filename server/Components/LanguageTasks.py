import openai
from dotenv import load_dotenv
import os
import json
from moviepy.editor import VideoFileClip

load_dotenv()

openai.api_key = os.getenv("OPENAI_API")

if not openai.api_key:
    raise ValueError(
        "API key not found. Make sure it is defined in the .env file.")


def extract_times(json_string):
    try:
        data = json.loads(json_string)

        # Check if we have highlights data
        if not data or len(data) == 0:
            print("No highlights data found in JSON")
            return 0, 0

        # For now, just return the first highlight (will be expanded later)
        start_time = float(data[0]["start"])
        end_time = float(data[0]["end"])

        start_time_int = int(start_time)
        end_time_int = int(end_time)
        return start_time_int, end_time_int
    except Exception as e:
        print(f"Error in extract_times: {e}")
        return 0, 0


def extract_all_highlights(json_string):
    """Extract all highlights from the JSON response"""
    try:
        data = json.loads(json_string)

        if not data or len(data) == 0:
            print("No highlights data found in JSON")
            return []

        highlights = []
        for highlight in data:
            try:
                start_time = int(float(highlight["start"]))
                end_time = int(float(highlight["end"]))
                content = highlight.get("content", "")

                if start_time != end_time:
                    highlights.append((start_time, end_time, content))
            except (KeyError, ValueError) as e:
                print(f"Error processing highlight: {e}")

        return highlights
    except Exception as e:
        print(f"Error in extract_all_highlights: {e}")
        return []


def get_system_prompt(num_highlights):
    return f"""
Based on the Transcription user provides extract {num_highlights} attention-grabbing highlights. 
Each highlight should be a short, engaging, and standalone segment that would perform well as a TikTok clip. 
Ensure that each clip is continuous and does not exceed a reasonable short-form content length. 
Prioritize moments with high emotional impact, surprising insights, humor, or compelling storytelling or something which is catchy and intersting to be viral. 

Follow this Format and return in valid json 
[{{
start: "Start time of the clip",
content: "Highlight Text",
end: "End Time for the highlighted clip"
}},
....
]
Make sure that each clip is atleast 30 seconds long and no less than that.
Use timestamps exactly as provided in the transcript. The response should strictly adhere to the specified JSON format, with no additional symbols, newline characters, or extraneous information. Dont say anything else, just return Proper Json. no explanation etc,

IF YOU DONT HAVE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESNT WORK THEN...
"""


User = """
Any Example
"""


def get_video_duration(video_path):
    """Get the duration of the video in minutes"""
    try:
        video = VideoFileClip(video_path)
        duration_minutes = video.duration / 60
        video.close()
        return duration_minutes
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0


def determine_highlight_count(duration_minutes):
    """Determine number of highlights based on video duration"""
    if duration_minutes < 3:
        return 2
    elif 3 <= duration_minutes < 10:
        return 2
    elif 10 <= duration_minutes < 20:
        return 3
    else:  # 20+ minutes
        return 5  # Using maximum value for longer videos


def GetHighlight(Transcription, video_path=None, num_highlights=None):
    print("Getting Highlight from Transcription")
    try:
        # Determine number of highlights based on video length if path is provided
        if num_highlights is None:
            if video_path:
                duration_minutes = get_video_duration(video_path)
                num_highlights = determine_highlight_count(duration_minutes)
                print(
                    f"Video duration: {duration_minutes:.2f} minutes, extracting {num_highlights} highlights")
            else:
                # Default to 2 highlights if no video path or explicit count provided
                num_highlights = 2
                print(
                    f"No video path provided, defaulting to {num_highlights} highlights")

        system = get_system_prompt(num_highlights)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": Transcription + system},
            ],
        )

        json_string = response.choices[0].message.content
        json_string = json_string.replace("json", "").replace("```", "")
        print("Json String: ", json_string)

        # Get all highlights
        all_highlights = extract_all_highlights(json_string)

        # If we have valid highlights, return the first one for backward compatibility
        if all_highlights:
            # In the future, we'll return all highlights
            start, end, _ = all_highlights[0]
            return start, end

        # Fallback to original extract_times if we couldn't get highlights
        Start, End = extract_times(json_string)
        if Start == End:
            # Retry up to 3 times automatically
            for i in range(3):
                print(f"Retrying highlight extraction (attempt {i+1}/3)")
                response = client.chat.completions.create(
                    model="gpt-4o",
                    # Increase temperature slightly each time
                    temperature=0.7 + (i * 0.1),
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": Transcription + system},
                    ],
                )
                json_string = response.choices[0].message.content
                json_string = json_string.replace(
                    "json", "").replace("```", "")

                # Try to extract all highlights again
                all_highlights = extract_all_highlights(json_string)
                if all_highlights:
                    start, end, _ = all_highlights[0]
                    return start, end

                # Fallback
                Start, End = extract_times(json_string)
                if Start != End:
                    break
        return Start, End

    except Exception as e:
        print(f"Error in GetHighlight: {e}")
        return 0, 0


# Add a new function to get all highlights at once
def GetAllHighlights(Transcription, video_path=None, num_highlights=None):
    """Get all highlights at once for a video"""
    print("Getting all highlights from Transcription")
    try:
        # Determine number of highlights based on video length if path is provided
        if num_highlights is None:
            if video_path:
                duration_minutes = get_video_duration(video_path)
                num_highlights = determine_highlight_count(duration_minutes)
                print(
                    f"Video duration: {duration_minutes:.2f} minutes, extracting {num_highlights} highlights")
            else:
                # Default to 2 highlights if no video path or explicit count provided
                num_highlights = 2
                print(
                    f"No video path provided, defaulting to {num_highlights} highlights")

        system = get_system_prompt(num_highlights)
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": Transcription + system},
            ],
        )

        json_string = response.choices[0].message.content
        json_string = json_string.replace("json", "").replace("```", "")
        print("Json String: ", json_string)

        # Get all highlights
        all_highlights = extract_all_highlights(json_string)

        # If no valid highlights found, retry
        if not all_highlights:
            for i in range(3):
                print(f"Retrying highlight extraction (attempt {i+1}/3)")
                response = client.chat.completions.create(
                    model="gpt-4o",
                    # Increase temperature slightly each time
                    temperature=0.7 + (i * 0.1),
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": Transcription + system},
                    ],
                )
                json_string = response.choices[0].message.content
                json_string = json_string.replace(
                    "json", "").replace("```", "")

                # Try to extract all highlights again
                all_highlights = extract_all_highlights(json_string)
                if all_highlights:
                    break

        return all_highlights

    except Exception as e:
        print(f"Error in GetAllHighlights: {e}")
        return []


if __name__ == "__main__":
    print(GetHighlight(User))
