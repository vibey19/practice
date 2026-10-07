import sys
import requests


# Check command-line argument
if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")

# Convert argument to a float
try:
    bitcoin_amount = float(sys.argv[1])
except ValueError:
    sys.exit("Command-line argument is not a number")

# Get Bitcoin price from CoinCap API
try:
    response = requests.get(
        "https://rest.coincap.io/v3/assets/bitcoin?apiKey=4465ee4b3a7660e26e576de63700933375a573c18e371a0b0c0087b4ddccf304"
    )
    response.raise_for_status()
    data = response.json()
except requests.RequestException:
    sys.exit("Could not retrieve Bitcoin price")

# Extract Bitcoin price
bitcoin_price = float(data["data"]["priceUsd"])

# Calculate total cost
total = bitcoin_amount * bitcoin_price

# Print with comma separators and 4 decimal places
print(f"${total:,.4f}")