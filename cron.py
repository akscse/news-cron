#!/usr/bin/env python3
import asyncio
import os
import sys
import httpx
import logging
import json
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from dotenv import load_dotenv
from models.news import News
from services.news_service import insert_news_from_api_response

# Load .env variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
NEWS_API_URL = os.getenv("NEWS_API_URL")
APP_NAME = os.getenv("APP_NAME", "news_app")
USER_ID = os.getenv("USER_ID", "user_1")
QUERY = os.getenv("QUERY", "Generate news using preference")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
DB_NAME = os.getenv("DB_NAME", "sane-news")

# Fail early if important variables are missing
missing_vars = []
if not MONGO_URI:
    missing_vars.append("MONGO_URI")
if not NEWS_API_URL:
    missing_vars.append("NEWS_API_URL")
if missing_vars:
    logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)


# Define AgentCallLog model
class AgentCallLog(Document):
    session_id: str
    start_timestamp: datetime
    end_timestamp: datetime
    status: str
    total_time_taken: float
    response_size: int
    error_message: str | None = None

    class Settings:
        name = "agent_call_log"


async def run_job():
    # Connect to MongoDB
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    await init_beanie(database=db, document_models=[News, AgentCallLog])

    # Generate new session_id using UTC-aware timestamp
    session_id = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    start_time = datetime.now(timezone.utc)

    logger.info(f"Starting API call, session_id={session_id}")

    # Prepare request body
    request_body = {
        "app_name": APP_NAME,
        "model_name": MODEL_NAME,
        "user_id": USER_ID,
        "session_id": session_id,
        "query": QUERY,
    }

    # Variables for logging
    status = "fail"
    response_size = 0
    error_message = None

    try:
        # Call the API (no timeout)
        async with httpx.AsyncClient(timeout=None) as client_http:
            logger.info(f"Calling API: {NEWS_API_URL}")
            resp = await client_http.post(NEWS_API_URL, json=request_body)

            # Raise for status to catch HTTP errors
            resp.raise_for_status()
            data = resp.json()

            # Calculate response size in bytes
            response_size = len(json.dumps(data).encode("utf-8"))

            # Process and insert data
            if not data:
                logger.warning("No 'news' field found in the API response.")
            else:
                logger.info("Inserting news into MongoDB...")
                await insert_news_from_api_response(data)
                logger.info("✅ News inserted successfully.")
                status = "pass"

    except httpx.HTTPStatusError as e:
        error_message = f"HTTP {e.response.status_code}: {e.response.text}"
        logger.error(f"❌ Server returned {e.response.status_code}: {e.response.text}")

    except Exception as e:
        error_message = str(e)
        logger.exception(f"❌ Error in cron job: {e}")

    finally:
        end_time = datetime.now(timezone.utc)
        total_time_taken = (end_time - start_time).total_seconds()

        # Log the call details in MongoDB
        await AgentCallLog(
            session_id=session_id,
            start_timestamp=start_time,
            end_timestamp=end_time,
            status=status,
            total_time_taken=total_time_taken,
            response_size=response_size,
            error_message=error_message
        ).insert()

        logger.info(
            f"📄 Logged API call: session_id={session_id}, status={status}, "
            f"duration={total_time_taken:.2f}s, size={response_size} bytes"
        )

        # Explicitly close Mongo connection
        mongo_client.close()


if __name__ == "__main__":
    asyncio.run(run_job())