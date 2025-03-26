import os
import sys
import time
import asyncio
import nest_asyncio
from typing import List

import gspread
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller

load_dotenv()
nest_asyncio.apply()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

class GSheets:
    def __init__(self, worksheet_name):
        self.gc = gspread.service_account(filename='service-account-keys.json')
        self.spreadsheet = self.gc.open_by_key(os.getenv("GSHEETS"))
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))
        self.rows = self.worksheet.get_all_values()
        self.cols_names = self.worksheet.get_all_values()[:1][0]
        self.formulas = {
            "Company Name": {"query": "This URL is for which Company? Return just the Company Name.", "agent": self.cohesive_gpt},
            "Internet KB": {"query": "Tell what does this company do in one line?", "agent": self.cohesive_scraper},
            "Number of Employees": {"query": "Find the number of employees in this Company", "agent": self.cohesive_scraper},
        }
        self.company_name=""

    def cohesive_gpt(self, query):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[query]
        )
        return response.text

    async def cohesive_scraper(self, task):
        agent = Agent(task=task, llm=self.model)
        history = await agent.run()
        result = history.final_result()
        return result

    async def async_wrapper(self, agent, prompt):
        return await agent(prompt)

    def update_sheet(self):
        rows = self.worksheet.get_all_values()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            website_url = row[0]
            for i in range(1, len(row)):
                col_name = self.cols_names[i]
                formula = self.formulas.get(col_name)
                if not formula:
                    continue
                prompt = formula.get("query")
                if i == 1:
                    prompt += f" {website_url}"
                else:
                    prompt += f" {self.company_name}"
                print(f"Prompt: {prompt}")
                agent = formula.get("agent")
                if asyncio.iscoroutinefunction(agent):
                    response_text = loop.run_until_complete(self.async_wrapper(agent, prompt))
                else:
                    response_text = agent(prompt)
                    if self.company_name == "":
                        self.company_name = response_text
                self.worksheet.update_cell(idx + 1, i + 1, response_text)

        loop.close()

if __name__ == "__main__":
    gs = GSheets("Sheet1")
    gs.update_sheet()
