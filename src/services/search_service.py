from typing import Optional

from pydantic import BaseModel
from yt_dlp import YoutubeDL

from src.models.video_metadata import YoutubeResult



FIVE_MINUTES=300

class SearchService:
    def __init__(self):
        pass
            
    def skip_live(self, info_dict):
        """
        function to skip downloading if it's a live video (yt_dlp doesn't respect the 20 minute 
        download limit for live videos), and we don't want to hang on an hour long stream
        """
        if info_dict.get("is_live"):
            return "Skipping live video"
        return None
    
    def search(self, query, max_results=10) -> list[YoutubeResult]:
        videos = []
        ydl_opts = {
            "format": "worst",
            "dumpjson": True,
            "extract_flat": True,
            "quiet": True,
            "simulate": True,
            "match_filter": self.skip_live,
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                search_query = f"ytsearch{max_results}:{query}"
                result = ydl.extract_info(search_query, download=False)
                if "entries" in result and result["entries"]:
                    videos = [
                        YoutubeResult(
                            video_id=entry["id"],
                            title=entry["title"],
                            description=entry.get("description"),
                            length=(int(entry.get("duration")) if entry.get("duration") else FIVE_MINUTES),
                            views=(entry.get("view_count") if entry.get("view_count") else 0),
                        ) for entry in result["entries"]
                    ]
            except Exception as e:
                
                return []
        return videos