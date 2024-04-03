from abc import ABC

from infra.entities.video_metadata_entity import VideoMetadataEntity



class VideoMetadataRepo(ABC):
    def get_metadata(self, video_id: str) -> dict:
        pass

    def save_metadata(self, metadata: VideoMetadataEntity):
        pass