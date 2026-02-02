"""
Extended GeoAI Agent with Multiple Tools
Demonstrates how to add distance calculation and reverse geocoding
"""

import asyncio
from copilot import CopilotClient, define_tool
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from pydantic import BaseModel, Field

# --- INITIALIZE GEOCODER ---
geolocator = Nominatim(user_agent="geoai_agent_extended")

# --- TOOL 1: GET COORDINATES ---
class GetCoordinatesInput(BaseModel):
    place_name: str = Field(
        ...,
        description="The name of the city or place to locate (e.g., 'Bangkok', 'Eiffel Tower')."
    )

async def get_coordinates_impl(args: GetCoordinatesInput) -> str:
    print(f"\n   [Tool] Fetching coordinates for: {args.place_name}...")
    try:
        location = geolocator.geocode(args.place_name)
        if location:
            return f"{args.place_name} is located at Lat: {location.latitude}, Lon: {location.longitude}"
        else:
            return f"Could not find coordinates for {args.place_name}."
    except Exception as e:
        return f"Error finding location: {str(e)}"

get_coords_tool = define_tool(
    name="get_coordinates",
    description="Get the latitude and longitude of a specific city or place name.",
    handler=get_coordinates_impl
)

# --- TOOL 2: CALCULATE DISTANCE ---
class CalculateDistanceInput(BaseModel):
    location1: str = Field(description="First location name (e.g., 'Paris')")
    location2: str = Field(description="Second location name (e.g., 'London')")

async def calculate_distance_impl(args: CalculateDistanceInput) -> str:
    print(f"\n   [Tool] Calculating distance between {args.location1} and {args.location2}...")
    try:
        loc1 = geolocator.geocode(args.location1)
        loc2 = geolocator.geocode(args.location2)

        if not loc1:
            return f"Could not find location: {args.location1}"
        if not loc2:
            return f"Could not find location: {args.location2}"

        coords1 = (loc1.latitude, loc1.longitude)
        coords2 = (loc2.latitude, loc2.longitude)

        distance_km = geodesic(coords1, coords2).kilometers
        distance_mi = geodesic(coords1, coords2).miles

        return f"Distance between {args.location1} and {args.location2}: {distance_km:.2f} km ({distance_mi:.2f} miles)"
    except Exception as e:
        return f"Error calculating distance: {str(e)}"

distance_tool = define_tool(
    name="calculate_distance",
    description="Calculate the distance between two locations in kilometers and miles.",
    handler=calculate_distance_impl
)

# --- TOOL 3: REVERSE GEOCODE ---
class ReverseGeocodeInput(BaseModel):
    latitude: float = Field(description="Latitude coordinate (e.g., 13.7563)")
    longitude: float = Field(description="Longitude coordinate (e.g., 100.5018)")

async def reverse_geocode_impl(args: ReverseGeocodeInput) -> str:
    print(f"\n   [Tool] Finding location for coordinates: {args.latitude}, {args.longitude}...")
    try:
        location = geolocator.reverse(f"{args.latitude}, {args.longitude}")
        if location:
            return f"Coordinates {args.latitude}, {args.longitude} correspond to: {location.address}"
        else:
            return f"No location found for coordinates {args.latitude}, {args.longitude}."
    except Exception as e:
        return f"Error in reverse geocoding: {str(e)}"

reverse_tool = define_tool(
    name="reverse_geocode",
    description="Get the location name and address from latitude and longitude coordinates.",
    handler=reverse_geocode_impl
)

# --- MAIN AGENT ---
async def main():
    client = CopilotClient()

    try:
        print("Starting Extended Copilot Client...")
        await client.start()

        # Create session with all three tools
        session = await client.create_session({
            "model": "gpt-5-mini",
            "tools": [get_coords_tool, distance_tool, reverse_tool],
            "system_message": """You are an advanced GeoAI Assistant with multiple capabilities:
            1. Find coordinates for any location using get_coordinates
            2. Calculate distances between locations using calculate_distance
            3. Find location names from coordinates using reverse_geocode

            Always use the appropriate tool for each request and provide detailed, helpful responses."""
        })

        print("\n🌍 Extended GeoAI Agent initialized (Model: GPT-5 mini).")
        print("   Available tools: Geocoding, Distance Calculation, Reverse Geocoding")
        print("   Type 'exit' or 'quit' to stop.")
        print("-" * 60)

        # Interactive loop
        while True:
            try:
                user_input = input("\nGeoNet Pro: ")

                if user_input.strip().lower() in ["exit", "quit"]:
                    print("Exiting...")
                    break

                if not user_input.strip():
                    continue

                response = await session.send_and_wait({
                    "prompt": user_input
                }, timeout=120)

                print(f"\nAgent: {response.data.content}")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    finally:
        print("Stopping client...")
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
