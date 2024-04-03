import sys
sys.path.append("src")

from infra.entities.video_metadata_entity import VideoMetadataEntity
from infra.engine import create_sqlalchemy_engine
from repositories.video_metadata_repo import VideoMetadataRepo
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from infra.entities.base import Base

class VideoMetadataRepoImpl(VideoMetadataRepo):
    def __init__(self) -> None:
        self.engine = create_sqlalchemy_engine()
        # Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def find_not_embeddings_videos(self) -> list[VideoMetadataEntity]:
        video_metadatas = []
        select_stmt = select(VideoMetadataEntity).where(VideoMetadataEntity.video_emb == "[]")
        results = self.session.execute(select_stmt).fetchall()
        for result in results:
            video_metadatas.append(result)
        return video_metadatas
    
    def get_metadata(self, video_id: str) -> dict:
        select_stmt = select(VideoMetadataEntity).where(VideoMetadataEntity.video_id == video_id)
        return self.session.execute(select_stmt).fetchone()

    def save_metadata(self, metadata: VideoMetadataEntity):
        self.session.add(metadata)
        self.session.commit()
        print(f"Saving metadata for video {metadata.video_id}")
    
    def update_metadata(self, metadata: VideoMetadataEntity):
        self.session.merge(metadata)
        self.session.commit()
        print(f"Updating metadata for video {metadata.video_id}")

    def save_all(self, metadatas: list[VideoMetadataEntity]):
        #  loop through the list of metadata and save each one if success or update if already exists or skip if error
        for metadata in metadatas:
            try:
                self.save_metadata(metadata)
            except Exception as e:
                print(f"Error saving metadata for video {metadata.video_id}: {e}")
                continue
    
    def search_by_query_and_sort_by_views(self, query: str) -> list[VideoMetadataEntity]:
        video_metadatas = []
        select_stmt = select(VideoMetadataEntity).where(VideoMetadataEntity.description.contains(query)).order_by(VideoMetadataEntity.views.desc())
        results = self.session.execute(select_stmt).fetchall()
        for result in results:
            video_metadatas.append(result)
        return video_metadatas
    
if __name__ == "__main__":
    repo = VideoMetadataRepoImpl()
    metadata = VideoMetadataEntity(
        video_id=1,
        description="Test video",
        views=100,
        start_time=0,
        end_time=100,
        query="test",
        score=100
    )
    repo.save_metadata(metadata)
    