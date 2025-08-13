from datetime import datetime
from models.news import News
async def insert_news_from_api_response(api_data: dict):
    """
    Insert news from API response into MongoDB.
    API format (simplified):

    {
        "response": [
            {
                "preference": "Science",
                "agent_response": {
                    "news_fetched": [
                        {
                            "name": "Science",
                            "description": "...",
                            "datetime": 1753517001.45211,
                            "news": [
                                {
                                    "heading": "...",
                                    "news": "...",
                                    "image": "...",
                                    "src": [...]
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    """

    for preference_block in api_data.get("response", []):
        preference = preference_block.get("preference")
        agent_response = preference_block.get("agent_response", {})
        news_fetched_list = agent_response.get("news_fetched", [])

        # print("News_fetched list", news_fetched_list)

        for fetched in news_fetched_list:
            category = fetched.get("name")
            timestamp = fetched.get("datetime")
            news_datetime = datetime.utcfromtimestamp(timestamp)

            for item in fetched.get("news", []):
                heading = item.get("heading")
                description = item.get("news")
                image = item.get("image", "")
                src = item.get("src", [])


                news_data = News(
                    category=category,
                            preference=preference,
                            heading=heading,
                            description=description,
                            news_datetime=news_datetime,
                            image=image,
                            src=src

                )

                await news_data.insert()
