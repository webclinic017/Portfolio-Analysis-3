## Stock Portfolio Forecasting (SPF)

This project enables individual investors with the ability to evaluate their own stock portfolio selections via a self-service tool. This is facilitate by the use of historical stock data, Monte Carlo simulations and other analysis techniques.  
Currently, the tool is implemented via a Jupyter Notebook. Future versions will provide a more full feature application with additional capabilities.

## Software Prerequisites
* Git Bash
* Anaconda/Jupyter Notebook
* Python >= 3.7
    * The following libraries must be installed (or available):
      * ConfigParser
      * sqlalchemy
      * psycopg2
      * hashlib
      * pandas
      * dotenv
      * alpaca_trade_api (you will need a key and secret)
      * getpass
      * scipy
      * ipywidgets
      * holoviews
      * hvplot
      * numpy
      * os
    * Or you can just activate the conda `pyvizenv` environment and then install python-dotenv and alpaca-trade-api
      * type `conda activate pyvizenv`
      * type `pip install python-dotenv`
      * type `pip install alpaca-trade-api`
* PostgreSQL >= 11.13    

### Initial Code Setup
* open a git bash terminal on your local computer
* type `git clone https://github.com/gakees/project_1_stock_portfolio_forecasting.git`
* then type `cd project_1_stock_portfolio_forecasting/Code/`
* create a `.env` file and add the following content:
```
    ALPACA_API_KEY=[your alpaca api key goes here...]
    ALPACA_SECRET_KEY=[your alpaca secret key goes here...]
```    
* create a `database.ini` file with the following content:
```
    [postgresql]
    host=localhost
    port=5432
    user=<your postgresql username>
    password=<your postgresql password>
    database=stock_portfolio_forecasting
```

### Database Setup
* Create a new database within PostgreSQL
    * The name of the database should be `stock_portfolio_forecasting`
* Open pgAdmin and run the following scripts to setup the database
    * [schema.sql](https://github.com/gakees/project_1_stock_portfolio_forecasting/blob/glenn-branch/Code/SQL/schema.sql)
    * [seed.sql](https://github.com/gakees/project_1_stock_portfolio_forecasting/blob/glenn-branch/Code/SQL/seed.sql)


### How to launch the interactive Jupyter Notebook
* from within the cloned git repository
    * type `jupyter lab` (from git bash)
    * then open the `dashboard.ipynb` file within the browser (/Code/Dashboard.ipynb)
* **NOTE: to login you will need the user credentials (which will be provided separately with the homework submission)**
