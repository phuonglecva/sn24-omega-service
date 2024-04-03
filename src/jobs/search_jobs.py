import sys
sys.path.append(".")
from concurrent.futures import ThreadPoolExecutor
import time
from typing import List
import requests

from src.infra.repositories.impl.video_metadata_repo_impl import VideoMetadataRepoImpl
from src.models.video_metadata import VideoMetadata
from src.services.openai_service import OpenAIAugment
from src.services.search_service import SearchService

QUERY_URL = "https://dev-validator.api.omega-labs.ai/api/topics"


class SearchVideosJobs:
    def __init__(self, queries: List[str], search_service: SearchService) -> None:
        self.queries = queries
        self.executor = ThreadPoolExecutor(max_workers=1)
        if len(queries) == 0:
            self.queries = self.load_queries()
            self.executor = ThreadPoolExecutor(
                max_workers=len(self.queries) + 10)
        self.search_service = search_service
        self.video_metadata_repo = VideoMetadataRepoImpl()
        self.openai_service = OpenAIAugment()

    def load_queries(self) -> List[str]:
        # load queries from the API
        response = requests.get(QUERY_URL)
        if response.status_code == 200:
            return response.json()
        return []

    def search_videos_by_query(self, query: str):
        while True:
            print(f"Searching for {query}")
            augmented_query = self.openai_service.augment_query(query)
            print(f"Augmented query: {augmented_query}")
            videos = self.search_service.search(
                augmented_query, max_results=30)
            print(f"Found {len(videos)} videos for {query}")

            video_metadatas = [VideoMetadata.from_yt_result(video, query) for video in videos]
            self.video_metadata_repo.save_all(video_metadatas)
            # publish video ids to queue
            print(f"Sleeping for 5 second`s")
            time.sleep(5)

    def run(self):
        futures = []
        for query in self.queries:
            futures.append(self.executor.submit(
                self.search_videos_by_query, query))

        # wait for all futures to finish
        for future in futures:
            future.result()

if __name__=='__main__':
    search_service = SearchService()
    queries = ["how to make a cake"]
    search_jobs = SearchVideosJobs(queries=queries, search_service=search_service)
    search_jobs.run()