import os
import json
from collections import defaultdict
from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import VideosSearch

def seconds_to_minute(seconds):
    return int(seconds // 60)

def combine_transcripts_by_minute(transcript):
    combined_transcript = defaultdict(str)

    for entry in transcript:
        minute = seconds_to_minute(entry['start'])
        combined_transcript[str(minute)] += f"{entry['text']} "

    return combined_transcript

def get_top_k_video_ids(query, keywords, k=15, min_duration_minutes=15):
    combined_queries = [query + " " + keyword for keyword in keywords]
    results = []

    for combined_query in combined_queries:
        search_results = VideosSearch(combined_query, limit=k * 5)
        
        for result in search_results.result()['result']:
            duration_parts = result['duration'].split(":")
            total_seconds = 0

            # Convert time to seconds
            for part in duration_parts:
                total_seconds = total_seconds * 60 + int(part)

            if total_seconds >= (min_duration_minutes * 60):
                video_info = {
                    "video_id": result['id'],
                    "title": result['title'],
                    "link": result['link'],
                    "duration": result['duration'],
                    "channel_name": result['channel']['name'],
                }
                results.append(video_info)

            if len(results) == k:  # Stop if we have enough results after filtering
                break

    return results

def get_and_save_transcripts(query, k=15, min_duration_minutes=15, keywords=[]):
    video_data = get_top_k_video_ids(query, keywords, k, min_duration_minutes)
    
    directory = os.path.join("youtube", query.replace(" ", "-"))
    if not os.path.exists(directory):
        os.makedirs(directory)

    for video_info in video_data:
        video_id = video_info["video_id"]
        title = video_info["title"]
        filename = os.path.join(directory, f"{title}.json".replace("/", "-"))  # Ensure filename is valid

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            combined_transcript = combine_transcripts_by_minute(transcript)
            
            # Combine video info (metadata) with transcript
            output = {
                "metadata": video_info,
                "transcript": combined_transcript
            }
            
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(output, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing video ID {video_id} titled {title}: {e}")

def main():
    handles = ['changpeng zhao', 'justin sun', 'vitalik buterin', 'brian armstrong', 'sam bankman-fried']
    keywords = ['talk', 'interview', 'seminar', 'keynote', 'presentation', 'lecture']
    
    for handle in handles:
        get_and_save_transcripts(handle, k=100, min_duration_minutes=5, keywords=keywords)

# Call the main function
main()
