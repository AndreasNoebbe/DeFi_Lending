import requests
import time
from plyer import notification

# Define the market and reserve public keys
market_pubkey = "7u3HeHxYDLhnCoErrtycNokbQYbWGzLs6JSDqGAv5PfF"  # Replace with the actual market pubkey
reserve_pubkey = "Bpc4kAh29J3YDQUMJJdGdr1zBAhTQjC48R1B8YTWudsi"  # Replace with the actual reserve pubkey

# Kamino API URL to check the reserve status
api_url = f"https://api.kamino.finance/kamino-market/{market_pubkey}/reserves/{reserve_pubkey}/metrics/history?env=mainnet-beta&start=2023-01-01&end=2023-01-02&frequency=hour"

def check_pool_status():
    try:
        response = requests.get(api_url)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()

        # Check the latest reserve status (You can adjust this depending on the exact format of your data)
        if data and "history" in data[0]:
            latest_data = data[0]["history"][-1]  # Get the latest data
            reserve_status = latest_data["metrics"]

            total_liquidity = float(reserve_status["totalLiquidityWads"])
            deposit_limit = float(reserve_status["reserveDepositLimit"])

            print(f"Total Liquidity: {total_liquidity}")
            print(f"Deposit Limit: {deposit_limit}")

            if total_liquidity < deposit_limit:
                print("Pool has room for deposit!")
                send_notification()
            else:
                print("Pool is full, no room for deposit.")
        else:
            print("Error: Unable to fetch pool data or empty response.")
    except Exception as e:
        print(f"Error fetching pool status: {e}")

def send_notification():
    notification.notify(
        title="FDUSD Pool Update",
        message="There is room in the FDUSD pool for your deposit.",
        timeout=10  # Notification will stay for 10 seconds
    )

if __name__ == "__main__":
    # Check pool status every 10 minutes (600 seconds)
    while True:
        check_pool_status()
        time.sleep(600)  # Sleep for 10 minutes before checking again
