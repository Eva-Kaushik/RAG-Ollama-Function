from typing import List
import yfinance as yf
from pydantic import BaseModel, Field
from instructor import Instructor, Mode

# Define the company name
company = "NVidia"

# Define the data model for stock information
class StockInfo(BaseModel):
    company: str = Field(..., description="Name of the company")
    ticker: str = Field(..., description="Ticker symbol of the company")

# Instantiate the Instructor client
client = Instructor(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    mode=Mode.JSON
)

# Create a message to retrieve stock information
message = [
    {
        "role": "user",
        "content": f"Return the company name and the ticker symbol of {company}."
    }
]

# Request completion from OpenAI's model
resp = client.chat.completions.create(
    model="llama2",
    messages=message,
    response_model=StockInfo,
    max_retries=10
)

# Print the response JSON
print(resp.model_dump_json(indent=2))

# Retrieve stock information using yfinance
stock = yf.Ticker(resp.ticker)
hist = stock.history(period="1d")
stock_price = hist['Close'].iloc[-1]

# Print the stock price
print(f"The stock price of {resp.company} is {stock_price} USD.")
