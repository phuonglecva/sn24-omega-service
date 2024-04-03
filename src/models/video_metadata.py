from typing import Optional
from pydantic import BaseModel

from src.infra.entities.video_metadata_entity import VideoMetadataEntity


class YoutubeResult(BaseModel):
    video_id: str
    title: str
    description: Optional[str]
    length: int
    views: int
    
class VideoMetadata(BaseModel):
    # generate same column as entity
    video_id: str
    description: str
    query: str
    views: int
    start_time: int
    end_time: int
    video_emb: str
    audio_emb: str
    description_emb: str
    score: int
    
    @staticmethod
    def from_yt_result(yt_result: YoutubeResult, query: str):
        # self.query = query
        # self.video_id = yt_result.video_id
        # self.description = yt_result.description
        # self.views = yt_result.views
        # self.start_time = 0
        # self.end_time = yt_result.length
        # self.video_emb = ""
        # self.audio_emb = ""
        # self.description_emb = ""
        # self.score = 0
        return VideoMetadataEntity(
            video_id=yt_result.video_id,
            title=yt_result.title,
            description=yt_result.description,
            views=yt_result.views,
            start_time=0,
            end_time=yt_result.length,
            query=query,
            score=0
        )