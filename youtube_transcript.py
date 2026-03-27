"""
Notevera AI – YouTube transcript extraction
"""
import re


def extract_youtube_transcript(url: str) -> str:
    """Extract transcript from a YouTube video URL."""
    # Extract video ID
    video_id = None
    patterns = [
        r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pat in patterns:
        match = re.search(pat, url)
        if match:
            video_id = match.group(1)
            break

    if not video_id:
        return ""

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript_list])
        return text
    except ImportError:
        return f"[YouTube transcript extraction requires youtube-transcript-api package. Video ID: {video_id}]"
    except Exception as e:
        return f"[Could not extract transcript for video {video_id}: {str(e)}]"
