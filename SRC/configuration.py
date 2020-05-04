import os
from dotenv import load_dotenv

load_dotenv()



PORT=os.getenv("PORT")
DBURL=os.getenv("DBURL")

# Connect to the database
#DBURL = os.getenv("DBURL") 
#if not DBURL:
#    raise ValueError("You should specify DBURL environment variable")