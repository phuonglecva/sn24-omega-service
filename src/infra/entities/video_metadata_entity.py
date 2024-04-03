import datetime
from sqlalchemy import Column, Integer, DateTime, String
from infra.entities.base import Base

class VideoMetadataEntity(Base):
    __tablename__ = "video_metadata"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    
    video_id = Column(Integer, index=True, unique=True)
    description = Column(String)
    title = Column(String)
    views = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    video_emb = Column(String, default="[]")
    audio_emb = Column(String, default="[]")
    description_emb = Column(String, default="[]")
    query = Column(String)  
    score = Column(Integer)
    
def convert_video_to_dict(video: VideoMetadataEntity):
    import json
    return {
        "id": video.id,
        "created_at": video.created_at,
        "updated_at": video.updated_at,
        "video_id": video.video_id,
        "description": video.description,
        "views": video.views,
        "start_time": video.start_time,
        "end_time": video.end_time,
        "video_emb": json.loads(video.video_emb),
        "audio_emb": json.loads(video.audio_emb),
        "description_emb": json.loads(video.description_emb),
        "query": video.query,
        "score": video.score
    }