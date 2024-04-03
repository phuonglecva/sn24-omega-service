import sys
sys.path.append(".")

from concurrent.futures import ThreadPoolExecutor
import time
from src.infra.repositories.impl.video_metadata_repo_impl import VideoMetadataRepoImpl
from src.models.video_metadata import VideoMetadata
from src.services.imagebind_wrapper import ImageBind
from src.services.proxy_service import ProxyService
from src.utils.video_utils import clip_video, download_video, get_description, get_relevant_timestamps
import json


class DownloadJobs:
    def __init__(self):
        self.video_metadata_repo = VideoMetadataRepoImpl()
        self.proxy_services = ProxyService()
        self.imagebind = ImageBind()
        self.executor = ThreadPoolExecutor(max_workers=1)
        
    def get_videos_to_download(self):
        return self.video_metadata_repo.find_not_embeddings_videos()
    
    def run(self):
        while True:
            videos = self.get_videos_to_download()
            print(f"Found {len(videos)} videos to download")
            futures = []
            for video in videos:
                futures.append(self.executor.submit(self.download, video))
            
            for future in futures:
                future.result()
            print("Finished downloading videos")
            time.sleep(30)            
    
    def download(self, video: VideoMetadata):
        print(f"Downloading video {video.video_id}")
        download_path = download_video(
            video.video_id, start=video.start_time, end=video.end_time,
            proxy=self.proxy_services.get_random_proxy()
        )
        print(f"Downloaded video {video.video_id}")
        if download_path:
            start, end = get_relevant_timestamps(video, video, download_path)
            description = get_description(video, download_path)
            clip_path = clip_video(download_path.name, start, end)
            embeddings = self.imagebind.embed([description], [clip_path])
            
            video.video_emb = json.dumps(embeddings.video[0].tolist())
            video.audio_emb = json.dumps(embeddings.audio[0].tolist())
            video.description_emb = json.dumps(embeddings.description[0].tolist())
            
            self.video_metadata_repo.update(video)
            print(f"Downloaded video {video.video_id} and updated embeddings")
            download_path.close()
            clip_path.close()
            return True
        return False
    
if __name__ == "__main__":
    jobs = DownloadJobs()
    jobs.run()