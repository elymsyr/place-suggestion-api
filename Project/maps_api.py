import googlemaps
from KEYS import MAPS_API_KEY

# Initialize the client
gmaps = googlemaps.Client(key=MAPS_API_KEY)

# Function to search for places with location restriction
def search_place_with_location(place_name, location):
    """Search for a place with a location restriction."""
    results = gmaps.places(query=place_name, location=location)
    return results

# Function to search for places without a location restriction
def search_place_without_location(place_name):
    """Search for a place without a location restriction."""
    results = gmaps.places(query=place_name)
    return results

# Function to find a place by phone number
def search_place_by_phone_number(phone_number):
    """Search for a place by phone number."""
    results = gmaps.find_place(input=phone_number, input_type="phonenumber")
    return results

# # Example 1: Search with a specific address
# results_with_address = search_place_with_location("10 High Street", "Escher, UK")
# print(results_with_address)

# Example 2: Search for a chain restaurant in a city
results_chain_restaurant = search_place_with_location("Burger King", "Sarıçam, Adana, Turkey")
print(results_chain_restaurant)

# # Example 3: Search for a unique restaurant by name in a specific city
# results_unique_restaurant = search_place_with_location("UniqueRestaurantName", "New York, NY, USA")
# print(results_unique_restaurant)

# # Example 4: Search for pizza restaurants in New York
# results_pizza = search_place_without_location("pizza restaurants in New York")
# print(results_pizza)

# # Example 5: Search by phone number
# results_by_phone = search_place_by_phone_number("+1 514-670-8700")
# print(results_by_phone)
