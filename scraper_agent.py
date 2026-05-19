import os
import sys
from dotenv import load_dotenv
from crewai import Agent,Task,Crew,Process
# from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool,SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI


# Load the .env file and parse its contents into the system's environment
load_dotenv()

#access the api key
gemini_api=os.getenv("GEMINI_API_KEY")

# 1. Define Agents (Role, Goal, Backstory)
selenium_tool = SeleniumScrapingTool(
    website_url='https://konga.com',
    css_element='mnr-c.pla-unit',
    wait_time=2
)
#serup my llm
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # or gemini-1.5-pro
    verbose=True,
    temperature=0.5,
    google_api_key=gemini_api
)



# Define the website url
website_url='https://www.google.com'
# Define the product to search for
product=sys.argv[1]

# Define the scraping agent
scraper_agent = Agent(
    role='Expert Web Data Scraper',
    goal=f'Accurately extract and format prices and product names from {website_url} about {product}',
    backstory=(
        "You are a master of web structures and data extraction. "
        "Your expertise lies in navigating complex websites to find "
        "hidden gems of information while ensuring the data is clean, "
        "structured, and ready for analysis.,Save the info in csv form"
    ),
    tools=[selenium_tool],
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)


# Create a task for the researcher
scrape_task = Task(
    description="Extract the main content from the homepage of example.com. Use the CSS selector 'main' to target the main content area.",
    expected_output="The main content from example.com's homepage.",
    agent=scraper_agent,
)

# Create and run the crew
crew = Crew(
    agents=[scraper_agent],
    tasks=[scrape_task],
    verbose=True,
    process=Process.sequential,
)
result = crew.kickoff()
print(result)
# with open ("cost.csv","r") as cost:
#     cost=csv.writer