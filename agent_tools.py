from agents import function_tool
from typing import TypedDict

class Location(TypedDict):
    lat: float
    long: float
    
    
@function_tool
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    print(f"Fetching weather for {location.get('lat')},{location.get('long')}")
    # In real life, we'd fetch the weather from a weather API
    return "sunny"

@function_tool
async def get_invoice(invoice_id: str) -> str:
    """
    Get the invoice for a given invoice id.
    """
    return "Invoice " + invoice_id + " for $100"

@function_tool
async def refund_invoice(invoice_id: str) -> str:
    """
    Refund the invoice for a given invoice id.
    """
    return "Refunded invoice " + invoice_id + " for $100"