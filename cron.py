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
        resp = await client_http.post(
            NEWS_API_URL,
            json=request_body,
            timeout=float(TIMEOUT)
        )
        resp.raise_for_status()
        data = resp.json()

#     data = {
#   "response": [
#     {
#       "preference": "Science",
#       "agent_response": {
#         "news_fetched": [
#           {
#             "name": "Science",
#             "description": "A broad field encompassing the systematic study of the structure and behavior of the physical and natural world through observation and experiment.",
#             "datetime": 1723563316.292399,
#             "news": [
#               {
#                 "heading": "Europe's Ariane 6 Rocket Successfully Launches Weather Satellite",
#                 "news": "Europe's new Ariane 6 rocket completed its third launch, successfully deploying a weather satellite into orbit. This mission is a significant step for the European Space Agency (ESA) as it works to re-establish its independent access to space.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "OpenAI Launches GPT-5, Touting It as 'Smartest, Fastest, Most Useful Model Yet'",
#                 "news": "OpenAI has officially launched GPT-5, the latest iteration of its flagship AI model. The company claims GPT-5 is significantly better at complex reasoning, creative writing, and coding. It is being rolled out to ChatGPT users and will be available to enterprise and education users soon.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Biotechnology Sector Sees Advances in mRNA and Gene Therapies Amid Funding Debates",
#                 "news": "The biotechnology industry is buzzing with discussions around the future of mRNA technology and the development of redosable gene therapies. These advancements come at a time of debate over federal funding for biotech startups and the impact of new drug pricing legislation.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "2024 Confirmed as Warmest Year on Record, Highlighting Urgent Climate Concerns",
#                 "news": "Multiple international studies have confirmed that 2024 was the warmest year since global record-keeping began in 1850. The global average surface temperature was 1.29°C above the 20th-century average, pushing the planet closer to the critical 1.5°C warming threshold.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Quantum Computing Breakthrough Allows Multiple Users to Share a Single Processor",
#                 "news": "Researchers at Columbia Engineering have developed 'HyperQ,' a system that enables multiple users to share a single quantum processor simultaneously. This breakthrough in cloud-style virtualization for quantum computing is expected to increase resource utilization and reduce costs, accelerating research and development in the field.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Entertainment",
#             "description": "The world of entertainment, including movies, music, television, and celebrity news, providing a glimpse into the latest cultural trends and events.",
#             "datetime": 1723563581.085834,
#             "news": [
#               {
#                 "heading": "'Weapons' Dominates the Box Office with $42.5 Million Opening Weekend",
#                 "news": "The new horror thriller 'Weapons' has taken the top spot at the box office, earning an impressive $42.5 million in its debut weekend. It was a strong opening for the film, outperforming other new releases like 'Freakier Friday' and 'Nobody 2'.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Taylor Swift Announces New Album, 'The Life of a Showgirl'",
#                 "news": "Taylor Swift has sent shockwaves through the music world with the announcement of her 12th studio album, titled 'The Life of a Showgirl.' The surprise announcement has fans buzzing with excitement and speculation about the new record.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "New Albums from The Black Keys, Maroon 5, and More Drop This Week",
#                 "news": "Music fans have a lot to look forward to this week with a fresh slate of album releases. Notable new albums include 'No Rain, No Flowers' from The Black Keys, 'Love Is Like' from Maroon 5, and 'Tunnel Vision' from Beach Bunny.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "'Alien: Earth' Premieres on FX/Hulu, Expanding the Iconic Sci-Fi Universe",
#                 "news": "The highly anticipated prequel series 'Alien: Earth' has premiered on FX and is available for streaming on Hulu. The show, set shortly before the events of the original 1979 film, explores a Xenomorph encounter on Earth and has been met with early positive reviews.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Shah Rukh Khan, Rani Mukerji, and '12th Fail' Win Big at 71st National Film Awards",
#                 "news": "The 71st National Film Awards in New Delhi honored the best of Indian cinema, with major wins for Shah Rukh Khan and Rani Mukerji. The film '12th Fail' took home the award for Best Feature Film, while Karan Johar's 'Rocky Aur Rani Kii Prem Kahaani' was recognized as the Best Popular Film Providing Wholesome Entertainment.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Health",
#             "description": "The latest news and updates in the world of health, covering medical breakthroughs, public health alerts, wellness trends, and healthcare policy.",
#             "datetime": 1723563964.91238,
#             "news": [
#               {
#                 "heading": "FDA Authorizes First At-Home Test for Both COVID-19 and Flu",
#                 "news": "The U.S. Food and Drug Administration has authorized the first over-the-counter rapid test that can simultaneously detect COVID-19 and influenza. This new test will allow individuals to use a single nasal swab to determine if they have either of the common respiratory viruses, providing more convenient at-home diagnosis.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Legionnaires' Disease Outbreak in NYC's Central Harlem Leads to 73 Infections, 3 Deaths",
#                 "news": "An outbreak of Legionnaires' disease in Central Harlem, New York City, has resulted in 73 reported infections and 3 fatalities. Health officials have identified and treated 11 cooling towers that tested positive for the Legionella bacteria, and investigations are ongoing.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "High Consumption of Ultra-Processed Foods Linked to Reduced Lifespan, Study Finds",
#                 "news": "A new study reveals a strong correlation between a diet high in ultra-processed foods—such as sodas, packaged snacks, and frozen meals—and a shorter lifespan. Health experts are urging for greater public awareness of these risks, as consumption of these foods is also linked to a variety of chronic health problems.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "New Research Discovers a Two-Way Link Between Gut Bacteria and Insomnia",
#                 "news": "Recent scientific findings have established a connection between specific types of gut bacteria and the risk of developing insomnia. This research opens up new possibilities for treating sleep disorders by focusing on improving gut health and the microbiome.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "House Passes 'One Big Beautiful Bill Act' with Major Cuts to Healthcare Programs",
#                 "news": "The U.S. House of Representatives has passed the 'One Big Beautiful Bill Act,' a budget bill that includes nearly $1 trillion in cuts to federal healthcare programs like Medicaid, Medicare, and the Affordable Care Act. The bill's passage has sparked significant debate over the future of healthcare access and funding in the country.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Technology",
#             "description": "The latest news and updates from the fast-paced world of technology, covering artificial intelligence, consumer electronics, big tech, cybersecurity, and future innovations.",
#             "datetime": 1723564267.423985,
#             "news": [
#               {
#                 "heading": "AI-Powered Robot in China Learns to Play Badminton with Humans",
#                 "news": "A new four-legged AI robot developed in China is making headlines for its ability to play badminton with human opponents. The robot uses a combination of advanced vision, sensors, and machine learning to react to the shuttlecock in real-time, showcasing a significant leap in AI-powered robotics.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Apple TV 2025 Rumored to Get a Major Performance Boost with A17 Pro or A18 Chip",
#                 "news": "Tech enthusiasts are buzzing with rumors about the upcoming Apple TV 2025, which is expected to feature a powerful A17 Pro or A18 chip. This upgrade would significantly enhance its performance, particularly for gaming, and could also include features like Wi-Fi 6E and a more sustainable design.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Big Tech Continues Mass Layoffs in 2025, with Over 130,000 Jobs Cut",
#                 "news": "The technology industry has seen a continuation of mass layoffs in 2025, with major companies like Microsoft, Google, and Amazon cutting over 130,000 jobs so far. Some experts point to the rise of AI and automation as a contributing factor, as companies look to optimize their operations.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "New 'Charon' Ransomware Targets Public Sector and Aviation in the Middle East",
#                 "news": "A sophisticated new ransomware family, dubbed 'Charon,' is actively targeting the public sector and aviation industry in the Middle East. Cybersecurity researchers have noted that the ransomware employs advanced tactics similar to those used by state-sponsored hacking groups, raising serious security concerns.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "AI Institute Launched to Accelerate Mathematical Discovery",
#                 "news": "Carnegie Mellon University is launching a new AI institute, funded by the National Science Foundation, with the goal of accelerating mathematical discovery. The institute will focus on developing AI tools that can assist mathematicians in conjecturing, proving, and visualizing complex theorems, potentially revolutionizing the field.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Breaking News",
#             "description": "The latest and most significant breaking news stories from around the world, covering politics, business, international events, and natural disasters.",
#             "datetime": 1723564757.98394,
#             "news": [
#               {
#                 "heading": "White House Defends Federal Takeover of D.C. Police as National Guard Arrives",
#                 "news": "The White House is defending its decision to federalize the Washington, D.C. police force. The move comes as National Guard troops have been deployed to the city, leading to uncertainty about the command structure of the local police.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Federal Court System Hacked, Exploiting Known Security Flaws",
#                 "news": "A significant hack has compromised the federal court's filing system, exploiting security vulnerabilities that have reportedly been known since 2020. The breach raises serious concerns about the security of sensitive legal documents and the integrity of the judicial system's digital infrastructure.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "US Treasury Secretary Calls for Half-Point Interest Rate Cut",
#                 "news": "In a significant economic development, the US Treasury Secretary is urging the Federal Reserve to implement a half-point interest rate cut at its next meeting. This call comes amid reports of steady US inflation and is likely to have a major impact on financial markets.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Mexico Extradites 26 High-Ranking Cartel Members to the US",
#                 "news": "In a major blow to organized crime, Mexico has sent 26 high-ranking cartel figures to the United States. This move is part of a significant deal between the two countries and represents a major step in the ongoing fight against drug trafficking and cartel violence.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Disaster Declared in 191 Texas Counties Due to Wildfire Threat",
#                 "news": "A state of disaster has been declared in 191 counties across Texas as the state faces a growing threat from wildfires. The declaration will free up resources to help combat the fires and support affected communities as dry and windy conditions continue to create a high-risk environment.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Market & Finance",
#             "description": "The latest news and analysis from the world of finance, including stock market performance, economic indicators, corporate M&A, and cryptocurrency trends.",
#             "datetime": 1723565158.583348,
#             "news": [
#               {
#                 "heading": "S&P 500 and Nasdaq Hit Record Highs on Hopes of Interest Rate Cut",
#                 "news": "The S&P 500 and Nasdaq Composite closed at record highs, fueled by growing investor optimism that the Federal Reserve will soon cut interest rates. The positive market sentiment comes after recent inflation data met expectations, reinforcing the case for a less aggressive monetary policy.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "US Inflation Holds Steady at 2.7%, Fueling Interest Rate Cut Speculation",
#                 "news": "The annual inflation rate in the US remained at 2.7% in July, matching the previous month's figure. This steady inflation data has intensified expectations that the Federal Reserve will move to cut interest rates at its upcoming September meeting to support economic growth.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Skydance Media Completes $8.4 Billion Merger with Paramount Global",
#                 "news": "RedBird Capital-backed Skydance Media has finalized its merger with Paramount Global in a landmark $8.4 billion deal. This major consolidation in the media and entertainment industry is expected to have significant ripple effects on the competitive landscape.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "US Senate Passes Landmark Stablecoin Bill, a Milestone for the Crypto Industry",
#                 "news": "The United States Senate has passed a new bill aimed at regulating stablecoins, marking a major legislative milestone for the cryptocurrency industry. The bill is expected to provide a clearer regulatory framework for stablecoin issuers and could pave the way for wider adoption of digital assets.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Trump Extends US-China Trade Ceasefire for Another 90 Days",
#                 "news": "President Trump has extended the trade truce with China for an additional 90 days, providing temporary relief from escalating trade tensions. The move is intended to allow more time for negotiations between the two economic giants and to avoid the imposition of new tariffs.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Education",
#             "description": "The latest news and developments in the field of education, covering policy, higher education, K-12 schools, educational technology, and student issues.",
#             "datetime": 1723565431.18933,
#             "news": [
#               {
#                 "heading": "Lawsuit Filed Against Federal Administration for Withholding $6 Billion in Education Funding",
#                 "news": "A coalition of education advocates, including the New York State United Teachers (NYSUT), has filed a lawsuit against the federal administration for withholding nearly $6 billion in education funding. The lawsuit aims to release funds designated for low-income students, English language learners, and other critical programs for the 2025-2026 school year.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Google Commits $1 Billion to AI Education and Job Training for US Colleges",
#                 "news": "Google has announced a $1 billion commitment to provide U.S. colleges and universities with artificial intelligence education and job training tools. This initiative aims to equip students with the skills needed for the future workforce and to foster innovation in AI research and development.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "K-12 Schools Grapple with Worsening Teacher Shortages",
#                 "news": "School districts across the country are facing critical teacher shortages, prompting a re-evaluation of state credentialing rules and recruitment strategies. The ongoing struggle to find and retain qualified educators is impacting classroom sizes, course offerings, and overall student learning.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "American Federation of Teachers Partners with Tech Giants to Boost AI Literacy",
#                 "news": "The American Federation of Teachers has announced a partnership with leading AI companies, including Microsoft, OpenAI, and Anthropic, to bring AI literacy to educators. This collaboration will provide teachers with the training and resources they need to effectively integrate AI into their classrooms and prepare students for a tech-driven future.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Student Reading and Math Scores Hit Lowest Levels in Decades",
#                 "news": "A new report reveals that student reading and math scores have fallen to their lowest levels in decades, highlighting a growing crisis in American education. The decline in academic performance is accompanied by a rise in chronic absenteeism, raising serious concerns about student engagement and well-being.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Travel",
#             "description": "The latest news, deals, and inspiration for your next journey, covering everything from airline updates and trending destinations to expert travel tips.",
#             "datetime": 1723565654.404874,
#             "news": [
#               {
#                 "heading": "British Airways Offers Deals on Flights to New York, Boston, and More",
#                 "news": "British Airways has released a new set of travel deals, with flights from London to New York starting at £357. The airline is also offering discounts on flights to other popular destinations like Boston, San Francisco, and Las Vegas, as well as savings on hotel stays at Universal Orlando Resort.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Allegiant Air Announces Five New Nonstop Routes Across Eight Cities",
#                 "news": "Allegiant Air has announced an expansion of its network with five new nonstop routes connecting eight cities. The new routes, which include service to Huntsville, Alabama, and Fort Lauderdale, Florida, are set to launch between late 2025 and early 2026.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Italy, Sri Lanka, and Greece Top the List of Trending Travel Destinations for 2025",
#                 "news": "Travel experts have identified Italy, Sri Lanka, and Greece as some of the most popular and trending destinations for 2025. These countries offer a diverse range of experiences, from the historic cities of Italy and the vibrant culture of Sri Lanka to the beautiful islands of Greece.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Experts Advise International Travelers to Enroll in STEP for Safety Alerts",
#                 "news": "Travel safety experts are advising international travelers to enroll in the Smart Traveler Enrollment Program (STEP). This free service from the U.S. Department of State provides travelers with email alerts on security issues, natural disasters, and other emergencies at their destination.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "U.S. Travel Association Launches New Coalition to Support Mega Sporting Events",
#                 "news": "The U.S. Travel Association has announced the launch of the America's Sports and Travel Mega Event Coalition (ASTMEC). The new coalition is designed to help the United States successfully host major global sporting events, which are a significant driver of tourism and economic growth.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Sports",
#             "description": "The latest news, scores, and highlights from the world of sports, covering everything from football and basketball to combat sports and more.",
#             "datetime": 1723565882.35338,
#             "news": [
#               {
#                 "heading": "Aaron Rodgers Criticizes New NFL Helmet, Calling It a 'Spaceship'",
#                 "news": "Pittsburgh Steelers quarterback Aaron Rodgers has voiced his displeasure with the NFL's new mandated helmet, humorously comparing its appearance to a 'damn spaceship.' The comment has sparked a conversation among players and fans about the design and aesthetics of the new safety equipment.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Darwin Nunez Leaves Liverpool for Al-Hilal in Major Transfer",
#                 "news": "In a significant move in the football transfer market, Darwin Nunez has completed a move from Liverpool to Saudi Arabian club Al-Hilal. The high-profile transfer is one of the biggest of the summer and marks a major shift in the global football landscape.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Vikings WR Rondale Moore Suffers Season-Ending Knee Injury",
#                 "news": "The Minnesota Vikings have suffered a major blow to their offense as wide receiver Rondale Moore sustained a season-ending knee injury during the preseason opener. Moore's absence will be a significant challenge for the Vikings as they head into the regular season.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Lakers and Kings Reportedly in Talks for Malik Monk Trade",
#                 "news": "The Los Angeles Lakers and Sacramento Kings are reportedly in discussions about a potential trade that would send guard Malik Monk to the Lakers. The rumored trade has generated significant buzz during the NBA off-season as teams look to finalize their rosters for the upcoming season.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "UFC Inks Massive $7.7 Billion Broadcast Deal with Paramount",
#                 "news": "The UFC has signed a new, record-breaking broadcast deal with Paramount worth a reported $7.7 billion. The landmark agreement is set to reshape the media rights landscape for combat sports and has sparked a debate about its potential impact on fighter pay and the overall fan experience.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
#             "name": "Politics",
#             "description": "The latest news and analysis from the world of politics, covering the White House, international relations, elections, and major policy debates.",
#             "datetime": 1723566089.541303,
#             "news": [
#               {
#                 "heading": "National Guard Deploys in Washington D.C. After Federal Takeover of Police",
#                 "news": "The D.C. National Guard has begun deploying on the streets of the nation's capital following a federal takeover of the city's police force. The move has sparked controversy and uncertainty, with the White House defending the action as necessary to address what it calls 'crime, bloodshed, bedlam and squalor.'",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "White House Open to Facilitating Peace Talks Between Ukraine and Russia",
#                 "news": "The White House has indicated that it is open to the possibility of bringing Ukraine and Russia together for peace talks. This development comes ahead of a planned meeting between President Trump and Russian President Vladimir Putin, which the White House has described as a 'listening exercise.'",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "Trump-Backed Byron Donalds Campaigns for Florida Governor in 2026",
#                 "news": "In an early move for the 2026 election cycle, Trump-backed Byron Donalds has officially begun his campaign to become the next governor of Florida. The race is expected to be closely watched as a key indicator of the political landscape in the crucial swing state.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "'One Big Beautiful Bill Act' and Minimum Wage Debates Dominate Legislative News",
#                 "news": "The 'One Big Beautiful Bill Act' has become one of the most-viewed pieces of legislation in Congress, highlighting a busy period of legislative activity. Lawmakers are also engaged in heated debates over other key issues, including the federal minimum wage, voter rights, and military aid to Ukraine.",
#                 "image": "",
#                 "src": [
                  
#                 ]
#               },
#               {
#                 "heading": "New Bribery Scandal Rocks European Parliament, Involving Huawei",
#                 "news": "The European Parliament is facing a new corruption scandal, with allegations that up to 15 former and current MEPs received gifts from Chinese tech giant Huawei in exchange for favorable political positions. The allegations have drawn comparisons to the 2022 'Qatargate' scandal and have sparked a major investigation.",
#                 "image": "",
#                 "src": [
                  
#                 ]
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
