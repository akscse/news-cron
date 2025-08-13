import asyncio
import os
import sys
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.news import News
from services.news_service import insert_news_from_api_response
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
NEWS_API_URL = os.getenv("NEWS_API_URL")
TIMEOUT = os.getenv("TIMEOUT")


print("MONGO_URI", MONGO_URI)
print("NEWS_API_URL", NEWS_API_URL)
print("TIMEOUT", TIMEOUT)

# 🚨 Fail early if variables are missing
if not MONGO_URI:
    print("❌ ERROR: MONGO_URI is not set in .env or environment variables.")
    sys.exit(1)

if not NEWS_API_URL:
    print("❌ ERROR: NEWS_API_URL is not set in .env or environment variables.")
    sys.exit(1)


print("Project start")

async def run_job():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["sane-news"]  # Explicit DB name to avoid get_default_database() issues
    await init_beanie(database=db, document_models=[News])

    # Static request body
    request_body = {
        "app_name": "news_app",
        "user_id": "user_1",
        "session_id": "session_001",
        "query": "Generate news using preference"
    }


    # Fetch news with POST
    async with httpx.AsyncClient() as client_http:
        # resp = await client_http.post(
        #     NEWS_API_URL,
        #     json=request_body,
        #     timeout=float(TIMEOUT)
        # )
        # resp.raise_for_status()
        # data = resp.json()

        try:
            resp = await client_http.post(NEWS_API_URL, json=request_body, timeout=float(TIMEOUT))
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            print(f"❌ API returned {e.response.status_code}")
            print("Response body:", e.response.text)
            return

#     data = {
#   "response": [
#     {
#       "preference": "Science",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Sports",
#             "description": "The latest news and updates from the world of sports, including major league results, player transfers, and top stories.",
#             "datetime": 1727881200,
#             "news": [
#               {
#                 "heading": "Eagles' Pro Bowl Guard Landon Dickerson Undergoes Knee Surgery",
#                 "news": "Philadelphia Eagles Pro Bowl guard Landon Dickerson is undergoing a minor procedure for a meniscus injury, adding to a growing list of significant NFL preseason injuries. The team is hopeful he will be ready for the start of the regular season.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "LAFC Signs Son Heung-Min; Darwin Nunez to Leave Liverpool",
#                 "news": "In a major MLS transfer, LAFC has signed South Korean superstar Son Heung-Min from Tottenham Hotspur. In other big soccer news, Liverpool striker Darwin Nunez is reportedly leaving the Premier League to join Saudi club Al-Hilal.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Milwaukee Brewers Extend Winning Streak to 10 Games",
#                 "news": "The Milwaukee Brewers continue their dominant run, extending their winning streak to 10 games. This is the second time this season the club has achieved a 10-game winning streak, solidifying their position as the best team in baseball.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Crystal Palace Wins Community Shield in Penalty Shootout",
#                 "news": "Crystal Palace has won the Community Shield, defeating Premier League champions Liverpool in a dramatic penalty shootout. The victory marks a significant upset to kick off the English football season.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "NBA Announces Marquee Matchups for Christmas Day and Opening Night",
#                 "news": "The NBA has unveiled its schedule for the 2025-26 season's opening night and Christmas Day games. A highly anticipated matchup between the Los Angeles Lakers and the Golden State Warriors will headline the opening night festivities.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Entertainment",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Politics",
#             "description": "The latest news and updates from the world of politics, covering the White House, Congress, the Supreme Court, and international relations.",
#             "datetime": 1727794800,
#             "news": [
#               {
#                 "heading": "Trump Federalizes D.C. Police, Citing 'Crime Emergency'",
#                 "news": "President Trump has invoked the D.C. Home Rule Act to place the Metropolitan Police Department under federal control, deploying the National Guard to address what he termed a 'crime emergency.' The move has been met with strong opposition from local officials who dispute the administration's crime statistics.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "U.S. and China Extend Tariff Truce for 90 Days",
#                 "news": "The United States and China have agreed to extend their trade truce for another 90 days, delaying a potential escalation of tariffs. The move is intended to provide more time for negotiations to resolve ongoing trade disputes between the world's two largest economies.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Trump and Putin to Discuss Ukraine 'Land Swapping' Deal",
#                 "news": "The White House is arranging a summit between President Trump and Russian President Vladimir Putin to negotiate an end to the war in Ukraine. A controversial 'land swapping' proposal is expected to be a central topic, an idea that has already been rejected by Ukrainian President Zelenskyy.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Supreme Court to Rule on Transgender Athlete Participation in Schools",
#                 "news": "The U.S. Supreme Court has agreed to hear a significant case concerning the participation of transgender athletes in school sports. The court will review lower court rulings from Idaho and West Virginia, setting the stage for a landmark decision on a contentious social and legal issue.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Redistricting and Sanctuary City Clashes Escalate in States",
#                 "news": "Intense political battles are flaring up in major states. In Texas, the Attorney General is taking legal action to expel Democratic lawmakers over a redistricting standoff. In California, Governor Gavin Newsom is publicly clashing with the Trump administration over redistricting, while San Francisco is suing the administration over its sanctuary city policies.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Health",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Science",
#             "description": "The latest news and updates in the world of science, from space exploration to the latest in biotechnology and quantum computing.",
#             "datetime": 1727708400,
#             "news": [
#               {
#                 "heading": "Webb Telescope Finds 'Sleeping Beauty' Galaxies; Planet Sighted in Nearest Star System",
#                 "news": "The James Webb Space Telescope continues to provide groundbreaking insights, recently discovering dormant 'sleeping beauty' galaxies in the early universe. In another major discovery, astronomers have found strong evidence of a giant planet orbiting a star in Alpha Centauri, our closest neighboring star system.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "New CRISPR Tools Advance Disease Modeling and Gene-Editing Precision",
#                 "news": "Biotechnology research is accelerating with the development of new CRISPR-based technologies. Yale scientists have created a new tool, CRISPR-Cas12a, that allows for more complex modeling of diseases like cancer. Other advancements are expanding RNA editing capabilities and enabling the precise insertion of large DNA sequences.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "AI Tool Developed to Detect Surgical Infections; Quantum ML Advances",
#                 "news": "Researchers have developed an AI-based tool that can automatically identify surgical incisions and detect early signs of infection, a major step for post-operative care. In a sign of converging technologies, other research has shown that even small-scale quantum computers can be used to enhance machine learning performance.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "2024 Confirmed as Hottest Year on Record Amidst Rise in Extreme Weather",
#                 "news": "Climate data has confirmed that 2024 was the warmest year since global records began in 1850, with the last seven years being the warmest ever. Scientific reports continue to link the rise in global temperatures to an increase in the frequency and intensity of extreme weather events around the world.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "New State of Matter 'Quantum Liquid Crystal' Discovered; Advances in Quantum Virtualization",
#                 "news": "Physicists have discovered a new state of matter known as a 'quantum liquid crystal' at the edge of two exotic materials. In the quantum computing realm, researchers have unveiled 'HyperQ,' a system that allows multiple users to share a single quantum processor, a key step towards practical, cloud-based quantum computing.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Technology",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Entertainment",
#             "description": "The latest news and updates from the world of entertainment, including movies, celebrity news, music, and streaming.",
#             "datetime": 1727535600,
#             "news": [
#               {
#                 "heading": "Cristiano Ronaldo and Georgina Rodriguez Announce Engagement",
#                 "news": "Soccer superstar Cristiano Ronaldo and his longtime partner Georgina Rodriguez have announced their engagement. Rodriguez was seen with a massive diamond ring, confirming the news that has excited fans worldwide.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Kelly Clarkson Pays Emotional Tribute to Late Ex-Husband Brandon Blackstock",
#                 "news": "Following the recent death of her ex-husband Brandon Blackstock at age 48, Kelly Clarkson paid a tearful tribute to him during a performance, changing the lyrics to a song. The singer is said to be 'devastated' by the loss.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Horror Film 'Weapons' Scores Big at Box Office with $42.5M Debut",
#                 "news": "The new original horror film 'Weapons' has topped the weekend box office with a strong $42.5 million. The film also earned a rare 'A–' CinemaScore from audiences, indicating positive word-of-mouth and a successful opening.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "'Tulsa King' Season 3 Premiere Date Announced; Samuel L. Jackson to Star in Spin-Off",
#                 "news": "Paramount+ has announced that Season 3 of the hit series 'Tulsa King,' starring Sylvester Stallone, will premiere on September 21st. It was also revealed that Samuel L. Jackson is joining the cast and will lead a new spin-off series, 'NOLA King.'",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Franchise Updates: 'Shrek 5' Delayed, New 'Rambo' Actor Cast for Prequel",
#                 "news": "There are major updates for several beloved film franchises. The release of 'Shrek 5' has been officially pushed back to the summer of 2027. In other news, a new actor has been cast to replace Sylvester Stallone in an upcoming 'Rambo' prequel.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Breaking News",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Health",
#             "description": "The latest news and updates from the world of health, including disease outbreaks, medical research, wellness trends, and healthcare policy.",
#             "datetime": 1727622000,
#             "news": [
#               {
#                 "heading": "Global Dengue Cases at Record High; Measles Outbreak in Texas",
#                 "news": "The global incidence of Dengue fever in 2024 is the highest on record for a calendar year, prompting a Level 1 travel notice from the CDC. In the U.S., a measles outbreak continues in the South Plains region of Texas, and several Salmonella outbreaks linked to food products are also ongoing.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Gene Therapy Restores Hearing in Deaf Child; CAR T-Cell Shows Promise for Brain Cancer",
#                 "news": "In a groundbreaking medical achievement, gene therapy has allowed a deaf child to hear for the first time. In cancer research, CAR T-cell therapy is showing significant promise in treating aggressive brain tumors in both children and adults, offering new hope for patients with difficult-to-treat cancers.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Wellness Shifts to Nature; CDC Launches Youth Mental Health Campaign",
#                 "news": "A prominent wellness trend for 2025 is a return to nature-infused pursuits like 'wild swimming' for its stress-reducing benefits. In response to a growing youth mental health crisis, the CDC has launched a new national campaign called 'Free Mind' to provide resources and information on substance use and mental well-being for teens.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Medicare Drug Cost Negotiations and ACA Coverage Dominate Health Policy",
#                 "news": "The Inflation Reduction Act (IRA) continues to be a central focus of healthcare policy, with ongoing negotiations to lower prescription drug costs for Medicare beneficiaries. The ACA also remains a key topic, credited with helping millions gain health insurance and reducing disparities in access to care.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "FDA Fast-Tracks Brain Tumor Drug; Quicker Cancer Treatment Injection Under Review",
#                 "news": "The FDA has granted accelerated approval to Modeyso (dordaviprone), a new drug for a rare and aggressive type of brain tumor. The agency is also reviewing a subcutaneous, under-the-skin version of the widely used cancer immunotherapy drug Keytruda, which could offer a more convenient treatment option for patients.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Market & Finance",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Technology",
#             "description": "The latest news and updates from the world of technology, including AI, consumer electronics, cybersecurity, and future tech.",
#             "datetime": 1727535600,
#             "news": [
#               {
#                 "heading": "AI Advances: Unrestricted Image Generator Launches, Met by New Deepfake Detector",
#                 "news": "Elon Musk's xAI has launched Grok-Imagine, an AI tool that generates images and videos without explicit safety restrictions, sparking ethical debates. In response to the rise of synthetic media, a new universal AI detector has been developed that can identify deepfake videos with 98% accuracy.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "New High-End Displays from Samsung and LG; Gaming Handhelds Emerge",
#                 "news": "Samsung has launched its new Micro RGB display, offering exceptional color accuracy with micro-scale LEDs. LG has also unveiled its G5 OLED TV, which is 40% brighter than previous models. In the gaming market, new PC gaming handhelds from Lenovo and Acer are entering the scene.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Big Tech News: Nvidia Becomes Most Valuable Company, Microsoft Pauses Hiring",
#                 "news": "Nvidia's market capitalization has reached $3.45 trillion, surpassing Microsoft to become the world's most valuable company. In other Big Tech news, Microsoft is pausing hiring in its U.S. consulting business as part of cost-cutting measures, and Apple is increasing its U.S. investment commitment to $600 billion.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Cybersecurity Alert: Yale Health Suffers Massive Data Breach, Ransomware Surges",
#                 "news": "The Yale New Haven Health System has been impacted by a major data breach affecting 5.5 million individuals, with personal and medical information compromised. This comes as cybersecurity reports indicate an 81% year-over-year increase in sophisticated ransomware attacks.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "The Future is Converged: AI and Quantum Computing Integration Deepens",
#                 "news": "The synergy between advanced technologies is growing stronger, particularly between AI and quantum computing. Quantum algorithms are being developed to accelerate machine learning models, while AI is being used to tackle key challenges in quantum development, such as error correction. The development of quantum-resistant blockchains is also a critical area of focus.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Education",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Breaking News",
#             "description": "The latest and most significant breaking news stories from around the world.",
#             "datetime": 1727535600,
#             "news": [
#               {
#                 "heading": "Trump Federalizes D.C. Police, Citing 'Public Safety Emergency'",
#                 "news": "President Trump has ordered a federal takeover of the Washington, D.C. police force and has deployed the National Guard, declaring a public safety emergency to crack down on crime. The move, which places the city's law enforcement under direct federal control, has been met with strong opposition from local officials.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Three People Killed in Shooting at Austin, Texas Target",
#                 "news": "A shooting in the parking lot of a Target store in Austin, Texas, has left three people dead. A suspect has been taken into custody. The incident is the latest in a series of violent events that have raised public safety concerns.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Fatal Explosion Rocks U.S. Steel Plant in Pennsylvania",
#                 "news": "At least two people have been killed and ten others injured following a major explosion at a U.S. Steel plant near Pittsburgh, Pennsylvania. Emergency crews responded to the scene at the Clairton Coke Works facility. The cause of the explosion is under investigation.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Journalists Killed by Israeli Strike in Gaza, Sparking Global Outrage",
#                 "news": "An Israeli airstrike in Gaza has killed a team of Al Jazeera journalists, an event that has drawn widespread international condemnation. The United Nations and media groups have called for a thorough investigation, while Israel has claimed that one of the journalists was a terrorist.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "U.S. and China Extend Trade Truce by 90 Days",
#                 "news": "The United States and China have extended their current trade truce for another 90 days, delaying a potential showdown over tariffs between the world's two largest economies. The move is seen as an opportunity for more ambitious talks to resolve ongoing trade disputes.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Travel",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Market & Finance",
#             "description": "The latest news and updates from the world of markets and finance, including stock market trends, cryptocurrency, economic indicators, and global trade.",
#             "datetime": 1727602800,
#             "news": [
#               {
#                 "heading": "Stock Markets Mixed as Investors Await Inflation Data",
#                 "news": "U.S. stock markets are showing mixed results, with the Dow Jones posting a slight gain while the Nasdaq has edged lower. Investors appear to be in a holding pattern, anticipating the release of key inflation data which is expected to influence the Federal Reserve's next moves on interest rates.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Cryptocurrency Market Sees Slight Pullback After Record High",
#                 "news": "Following a surge that pushed the total crypto market capitalization to a record high, the market has experienced a slight correction. The global crypto market cap has decreased by about 1.88% in the last 24 hours, with Bitcoin trading just under $119,000.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "U.S. Economy Shows Strength with 3% GDP Growth in Q2",
#                 "news": "The latest government reports indicate a solid performance for the U.S. economy. Real Gross Domestic Product (GDP) increased at an annual rate of 3.0% in the second quarter of 2025. Additionally, the U.S. international trade deficit decreased in June, providing another positive economic signal.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "John Deere Announces $20B U.S. Investment; Hims & Hers Reports Strong Growth",
#                 "news": "In major corporate news, John Deere has announced a $20 billion investment in the United States over the next 10 years. In earnings news, telehealth company Hims & Hers reported strong second-quarter results, including significant subscriber growth and a substantial increase in revenue.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "New U.S. Tariffs Take Effect, Creating Global Trade Uncertainty",
#                 "news": "A new round of U.S. tariffs on goods from various countries is now in effect, creating uncertainty in the global trade landscape. The World Trade Organization (WTO) has revised its 2025 trade growth forecast upward due to a pre-tariff surge in U.S. imports, but warns that the new tariffs are likely to dampen trade in the long term.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Sports",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Education",
#             "description": "The latest news and updates from the world of education, covering policy, technology, higher education, K-12 issues, and global trends.",
#             "datetime": 1727689200,
#             "news": [
#               {
#                 "heading": "Google's $1B Investment Fuels AI Integration in U.S. Colleges",
#                 "news": "Google is investing $1 billion to provide U.S. colleges and universities with artificial intelligence education and job training tools. This comes as AI is rapidly being integrated into classrooms for tasks like lesson planning and personalized feedback, though many teachers report a lack of formal training on the new technology.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "U.S. Universities Face Federal Scrutiny and Antitrust Lawsuit",
#                 "news": "America's higher education institutions are under increasing pressure. The Trump administration is scrutinizing college admissions data for racial bias and has frozen research grants at some universities. Simultaneously, 32 elite universities are facing an antitrust lawsuit over their early decision admissions programs.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "K-12 Schools Grapple with Teacher Shortages and Mental Health Crisis",
#                 "news": "The K-12 education system continues to face a dual crisis of severe teacher shortages and growing student mental health issues. In response to the latter, Illinois has become the first state to require universal mental health screenings for students in grades 3-12.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Education Reform Focuses on Local Control and Foundational Skills",
#                 "news": "In the U.S., the Secretary of Education is on a 50-state tour to promote local innovation in schools. In India, the implementation of the National Education Policy (NEP) 2020 continues to advance, with a strong focus on improving foundational literacy and numeracy for young students.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "International Student Enrollment Hits Record High, But New U.S. Numbers Dip",
#                 "news": "The total number of international students studying in the U.S. has reached an all-time high of over 1.1 million. However, the number of *new* international students has decreased by 5%, with visa challenges, rising costs, and increased competition from other countries cited as reasons for the decline.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     },
#     {
#       "preference": "Politics",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Travel",
#             "description": "The latest news and updates from the world of travel, including industry news, trending destinations, deals, and safety information.",
#             "datetime": 1727794800,
#             "news": [
#               {
#                 "heading": "Air Canada in Talks to Avert Strike; Airlines Announce Route Expansions",
#                 "news": "Air Canada is in negotiations to prevent a potential strike by its 10,000 flight attendants, which could begin as early as August 16th. In other airline news, American Airlines and Lufthansa have announced major expansions of their international routes for 2025 and 2026.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Italy, Japan, and South Africa Top 2025's Trending Destinations",
#                 "news": "For travelers planning ahead, Italy and Japan remain top trending destinations. South Africa is also gaining popularity, offering a unique combination of safari adventures and vibrant city life. For a different kind of experience, Osaka, Japan has been named the number one trending destination for 2025.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Travel Trend Shifts from 'Sustainable' to 'Regenerative'",
#                 "news": "A significant evolution in eco-conscious travel is underway, with the focus shifting from 'sustainable' to 'regenerative' travel. This new approach encourages travelers to actively improve the destinations they visit through activities like habitat restoration and supporting community-led tourism projects.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "Flexibility and Advance Booking Key to Unlocking Travel Deals",
#                 "news": "Travel experts continue to advise that the best way to save money on travel is to be flexible with your dates and to book in advance. Flying on Tuesdays and Wednesdays is often cheaper than on weekends. Additionally, using travel credit cards for points and perks can lead to significant savings.",
#                 "image": "",
#                 "src": []
#               },
#               {
#                 "heading": "U.S. Issues Travel Advisories for Brazil and UAE; 'Do Not Travel' List Updated",
#                 "news": "The U.S. State Department has issued updated travel advisories, urging increased caution for travelers heading to Brazil due to rising crime rates, and to the United Arab Emirates due to potential terrorism threats. The 'Do Not Travel' list continues to include countries like Russia, Ukraine, and Syria.",
#                 "image": "",
#                 "src": []
#               }
#             ]
#           }
#         ]
#       }
#     }
#   ]
# }

    # Insert into MongoDB
    print("Start inserting")
    await insert_news_from_api_response(data)
    print("✅ News inserted successfully")


if __name__ == "__main__":
    asyncio.run(run_job())
