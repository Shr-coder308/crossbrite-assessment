import json

import redis

from app.core.config import settings


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)


def queue_evaluation(evaluation_id: int, session_id: int):
    job = {
        "evaluation_id": evaluation_id,
        "session_id": session_id,
        "status": "queued",
    }

    redis_client.rpush(
        "evaluation_queue",
        json.dumps(job)
    )

    return job