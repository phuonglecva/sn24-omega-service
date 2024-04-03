import sys
sys.path.append(".")
from src.infra.entities.video_metadata_entity import convert_video_to_dict
from src.services.video_metadata_service import VideoMetadataSevice
from src.services.search_service import SearchService
from src.jobs.search_jobs import SearchVideosJobs
from src.jobs.download_jobs import DownloadJobs
from src.infra.repositories.impl.video_metadata_repo_impl import VideoMetadataRepoImpl
import threading
from infra.entities.base import Base
from infra.engine import create_sqlalchemy_engine
from fastapi import FastAPI


# download_jobs = DownloadJobs()
# download_thread = threading.Thread(target=download_jobs.run)

# search_service = SearchService()
# search_jobs = SearchVideosJobs(queries=[], search_service=search_service)
# search_thread = threading.Thread(target=search_jobs.run)

video_metadata_repo = VideoMetadataRepoImpl()
video_metadata_service = VideoMetadataSevice(
    video_metadata_repo=video_metadata_repo)

sqlite_engine = create_sqlalchemy_engine("sqlite:///db.sqlite")

# check if the table exists, if not create it
Base.metadata.create_all(bind=sqlite_engine)
# Base.metadata.create_all(bind=sqlite_engine)

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     download_thread.start()
#     search_thread.start()
#     print("Started download and search threads")

# @app.on_event("shutdown")
# async def shutdown_event():
#     download_thread.join()
#     search_thread.join()
#     print("Stopped download and search threads")

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/search")
def search(query: str):
    if not query:
        return {
            "msg": "Query is required",
            "data": []  
        }
    videos = video_metadata_service.get_video_by_query(query)
    return {
        "msg": "Success",
        "data": [convert_video_to_dict(video[0]) for video in videos]
    
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
