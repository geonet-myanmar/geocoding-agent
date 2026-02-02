import asyncio
from copilot import CopilotClient, define_tool
from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field

# --- STEP 1: DEFINE THE TOOLS ---

geolocator = Nominatim(user_agent="geoai_agent_interactive")

# 1. Define the Input Schema
class GetCoordinatesInput(BaseModel):
    place_name: str = Field(
        ..., 
        description="The name of the city or place to locate (e.g., 'Bangkok', 'Eiffel Tower')."
    )

# 2. Define the Implementation
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

# 3. Define the Tool
get_coords_tool = define_tool(
    name="get_coordinates",
    description="Get the latitude and longitude of a specific city or place name.",
    handler=get_coordinates_impl
)

# --- STEP 2: INITIALIZE THE INTERACTIVE AGENT ---

async def main():
    client = CopilotClient()
    
    try:
        print("Starting Copilot Client...")
        await client.start()
        
        # Create a persistent session with the tool enabled
        session = await client.create_session({
            "model": "gpt-5-mini",  # Using the powerful model
            "tools": [get_coords_tool],
            "system_message": "You are a GeoAI Assistant. Always use coordinates when discussing locations."
        })

        print("\n🌍 GeoAI Agent initialized (Model: GPT-5 mini).")
        print("   Type 'exit' or 'quit' to stop.")
        print("-" * 50)
        
        # --- INTERACTIVE LOOP ---
        while True:
            try:
                user_input = input("\nGeoNet Myanmar: ")
                
                if user_input.strip().lower() in ["exit", "quit"]:
                    print("Exiting...")
                    break
                
                if not user_input.strip():
                    continue

                # The 'send_and_wait' keeps the context of previous turns in 'session'
                response = await session.send_and_wait({
                    "prompt": user_input
                }, timeout=120)

                print(f"Agent: {response.data.content}")
                
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