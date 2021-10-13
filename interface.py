from database import Database
from dotenv import load_dotenv
from MCForecastTools import MCSimulation
import alpaca_trade_api as tradeapi
import pandas as pd
import warnings
import getpass
import os

class UserInterface:
    # Create a private instance of the Database class
    __database = Database()
    
    def __init__(self):
        # Suppress the PerformanceWarning message when running the Monte Carlo simulation (below)
        warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
        
        # Load .env enviroment variables
        load_dotenv()
        
        # Set Alpaca API key and secret
        alpaca_api_key = os.getenv("ALPACA_API_KEY")
        alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.__api = tradeapi.REST( alpaca_api_key, alpaca_secret_key, api_version = "v2")
    
    def login_user(self):
        while True:
            # Present the user with the following input prompts
            username = input(prompt="\nEnter Username:")
            password = getpass.getpass(prompt="Enter Password:")

            # Attempt to login the user given their username and password
            user_profile = self.__database.login(username, password)

            # If the user_profile does not exist then their login has failed...
            if len(user_profile) == 0:
                print("\nUsername or Password entered is incorrect.")
            else:
                print(f"\nWelcome, {username}.  You are now logged in...")
                break
        
        # Create a data structure to store the user's profile data
        user = {}
        user["id"] = user_profile.loc[0, "id"]
        user["username"] = user_profile.loc[0, "username"]
        
        return user
    
    def select_portfolio(self):
        # Initialize the data structure for storing the portfolio
        portfolio = {}
        
        # Present the user with the following input prompts
        portfolio["investment"] = float(input(prompt="\nEnter Initial Investment (e.g. $50,000):").replace(",", "").replace("$", ""))
        portfolio["symbols"] = [symbol for symbol in input(prompt="\nEnter Symbols In Portfolio (e.g. AAPL, MSFT, etc...):").replace(" ", "").split(",")]
        portfolio["weights"] = [float(weight) for weight in input(prompt="\nEnter Weights for the Portfolio Symbols (e.g. 0.2, 0.4, etc...):").replace(" ", "").split(",")]
            
        return portfolio
    
    def get_historical_data(self, portfolio, timeframe="1D", starting="2017-11-01", ending="2021-11-01"):
        # Format the start_date and end_date to the ISO 8601 extended format
        start_date = pd.Timestamp(starting, tz="America/Phoenix").isoformat()
        end_date = pd.Timestamp(ending, tz="America/Phoenix").isoformat()
        
        # Add the SPY symbol as the benchmark index
        portfolio_with_spy = portfolio["symbols"].copy()
        portfolio_with_spy.append("SPY")
        
        # Call the Alpaca Trade API to retrieve historical data
        historical_data = self.__api.get_barset(
            symbols=portfolio_with_spy,
            timeframe=timeframe,
            start=start_date,
            end=end_date,
            limit=1000,
        ).df
        
        # Remove the time component from the datetime value
        historical_data.index = historical_data.index.date
        
        return historical_data
    
    def calculate_beta_values(self, portfolio):
        # Initialize the beta values structure
        beta_values = {}
        
        # Calculate the daily returns for each stock symbol in the DataFrame
        daily_returns = portfolio["historical_data"].pct_change().dropna()
        
        # Calculate the beta value for each symbol in the portfolio
        for symbol in portfolio["symbols"]:
            covariance = daily_returns[symbol]["close"].cov(daily_returns['SPY']["close"])            
            variance = daily_returns["SPY"]["close"].var()
            beta_values[symbol] = round(covariance/variance, 1)

        return beta_values
    
    def display_beta_values(self, beta_values):
        for symbol, beta_value in beta_values.items():
            print(f"beta for {symbol} is: {beta_value}")
    
    def create_simulation(self, portfolio, simulations=1000, years=5):
        # Create a copy of the portfolio (historical data)
        historical_data = portfolio["historical_data"].copy()
        
        # Remove the "SPY" column if present
        if "SPY" in historical_data.columns:
            historical_data.drop(columns=["SPY"], inplace=True)
            
        return MCSimulation(
            portfolio_data = historical_data,
            weights = portfolio["weights"],
            num_simulation = simulations,
            num_trading_days = 252*years
        )
    
    def display_portfolio_forecast(self, portfolio):
        upper_ci_95_pct = portfolio["simulated_returns"][8]
        lower_ci_95_pct = portfolio["simulated_returns"][9]
        investment = portfolio["investment"]                
        
        ci_lower = round(investment * upper_ci_95_pct, 2)
        ci_upper = round(investment * lower_ci_95_pct, 2)

        # Display the portfolio forecast based on the simulation run
        print(f"There is a 95% chance that an initial investment of ${investment:,.2f}\nin the portfolio"
              f" over the next 10 years will end within the following\nrange of"
              f" ${ci_lower:,.2f} and ${ci_upper:,.2f}")