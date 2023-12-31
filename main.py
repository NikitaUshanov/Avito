import asyncio
import os

from dotenv import load_dotenv

from src.avito import AvitoSearch

project_folder = os.path.expanduser(os.getcwd())
load_dotenv(os.path.join(project_folder, ".env"))

AS = AvitoSearch()
asyncio.run(AS.init_browser())
