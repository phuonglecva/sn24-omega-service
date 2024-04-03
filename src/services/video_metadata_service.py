from src.infra.repositories.impl.video_metadata_repo_impl import VideoMetadataRepoImpl


class VideoMetadataSevice:
    def __init__(self, video_metadata_repo: VideoMetadataRepoImpl) -> None:
        self.video_metadata_repo = video_metadata_repo
    
    def get_video_by_query(self, query: str):
        videos = self.video_metadata_repo.search_by_query_and_sort_by_views(query)
        return videos
    