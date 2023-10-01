import pandas as pd

def calculate_weekly_revenue(sales_data):
    # Creating a DataFrame from sales_data
    df = pd.DataFrame([(sale.SaleDate, sale.Quantity, sale.Price) for sale in sales_data], 
                      columns=['SaleDate', 'Quantity', 'Price'])

    # Parsing SaleDate column to datetime and setting it as index
    df['SaleDate'] = pd.to_datetime(df['SaleDate'])
    df.set_index('SaleDate', inplace=True)

    # Calculating weekly revenue by multiplying Quantity and Price, then summing by week (W-Mon)
    weekly_revenue = df['Quantity'] * df['Price']
    weekly_revenue = weekly_revenue.resample('D').interpolate()[::7].sum().reset_index()

    # Converting DataFrame to a list of dictionaries for the response format
    weekly_revenue_list = weekly_revenue.rename(columns={'SaleDate': 'week_start_date', 0: 'revenue'}).to_dict(orient='records')

    return weekly_revenue_list


def calculate_daily_revenue(sales_data):
    # Creating a DataFrame from sales_data
    df = pd.DataFrame([(sale.SaleDate, sale.Quantity, sale.Price) for sale in sales_data], columns=['SaleDate', 'Quantity', 'Price'])

    # Parsing SaleDate column to datetime and setting it as index
    df['SaleDate'] = pd.to_datetime(df['SaleDate'])
    df.set_index('SaleDate', inplace=True)

    # Calculating daily revenue by multiplying Quantity and Price, then summing by day
    daily_revenue = df['Quantity'] * df['Price']
    daily_revenue = daily_revenue.resample('D').sum().reset_index()

    # Converting DataFrame to a list of dictionaries for the response format
    daily_revenue_list = daily_revenue.rename(columns={'SaleDate': 'date', 0: 'revenue'}).to_dict(orient='records')

    return daily_revenue_list

def calculate_monthly_revenue(sales_data):
    # Creating a DataFrame from sales_data
    df = pd.DataFrame([(sale.SaleDate, sale.Quantity, sale.Price) for sale in sales_data], 
                      columns=['SaleDate', 'Quantity', 'Price'])

    # Parsing SaleDate column to datetime and setting it as index
    df['SaleDate'] = pd.to_datetime(df['SaleDate']).dt.date
    df.set_index('SaleDate', inplace=True)

    # Calculating monthly revenue by multiplying Quantity and Price, then summing by month
    monthly_revenue = df['Quantity'] * df['Price']
    monthly_revenue = monthly_revenue.resample('M').sum().reset_index()

    # Converting DataFrame to a list of dictionaries for the response format
    monthly_revenue_list = monthly_revenue.rename(columns={'SaleDate': 'month_start_date', 0: 'revenue'}).to_dict(orient='records')

    return monthly_revenue_list
def calculate_annual_revenue(sales_data):
    # Creating a DataFrame from sales_data
    df = pd.DataFrame([(sale.SaleDate, sale.Quantity, sale.Price) for sale in sales_data], 
                      columns=['SaleDate', 'Quantity', 'Price'])

    # Parsing SaleDate column to datetime and setting it as index
    df['SaleDate'] = pd.to_datetime(df['SaleDate'])
    df.set_index('SaleDate', inplace=True)

    # Calculating yearly revenue by multiplying Quantity and Price, then summing by year
    yearly_revenue = df['Quantity'] * df['Price']
    yearly_revenue = yearly_revenue.resample('Y').sum().reset_index()

    # Converting DataFrame to a list of dictionaries for the response format
    yearly_revenue_list = yearly_revenue.rename(columns={'SaleDate': 'year_start_date', 0: 'revenue'}).to_dict(orient='records')

    return yearly_revenue_list


def calculate_revenue(sales_data, frequency):
    # Creating a DataFrame from sales_data
    df = pd.DataFrame([(sale.SaleDate, sale.Quantity, sale.Price) for sale in sales_data], 
                      columns=['SaleDate', 'Quantity', 'Price'])

    # Parsing SaleDate column to datetime and setting it as index
    df['SaleDate'] = pd.to_datetime(df['SaleDate']).dt.date
    df.set_index('SaleDate', inplace=True)

    # Calculating revenue based on frequency (daily, weekly, monthly, yearly)
    if frequency == 'daily':
        revenue = df['Quantity'] * df['Price']
        revenue = revenue.resample('D').sum().reset_index()
    elif frequency == 'weekly':
        revenue = df['Quantity'] * df['Price']
        revenue = revenue.resample('W-Mon').sum().reset_index()
    elif frequency == 'monthly':
        revenue = df['Quantity'] * df['Price']
        revenue = revenue.resample('M').sum().reset_index()
    elif frequency == 'yearly':
        revenue = df['Quantity'] * df['Price']
        revenue = revenue.resample('Y').sum().reset_index()
    else:
        raise ValueError("Invalid frequency. Supported frequencies: daily, weekly, monthly, yearly.")

    # Converting DataFrame to a list of dictionaries for the response format
    revenue_list = revenue.rename(columns={'SaleDate': f'{frequency}_start_date', 0: 'revenue'}).to_dict(orient='records')

    return revenue_list