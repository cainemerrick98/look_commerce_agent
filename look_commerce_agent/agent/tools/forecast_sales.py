import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_sales(data: pd.DataFrame, periods: int = 3) -> pd.DataFrame:
    """
    Forecasts future sales by applying a linear trend to historical monthly data.
    
    Args:
        data (pd.DataFrame): A DataFrame with two columns: 'month' (datetime or string) 
                             and 'revenue' (numeric).
        periods (int): Number of months to forecast into the future.
                             
    Returns:
        pd.DataFrame: A DataFrame containing the historical data plus the forecasted months.
    """
    # 1. Ensure date format
    data['month'] = pd.to_datetime(data['month'])
    data = data.sort_values('month')

    # 2. Convert dates to numeric 'ordinal' values for the model
    # (Linear models can't read dates directly, so we use numbers)
    X = np.array(data['month'].map(pd.Timestamp.toordinal)).reshape(-1, 1)
    y = data['revenue'].values

    # 3. Fit the model
    model = LinearRegression()
    model.fit(X, y)

    # 4. Create future dates
    last_date = data['month'].max()
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1), 
        periods=periods, 
        freq='MS'
    )

    # 5. Predict
    future_X = np.array(future_dates.map(pd.Timestamp.toordinal)).reshape(-1, 1)
    future_preds = model.predict(future_X)

    # 6. Combine results
    forecast_df = pd.DataFrame({
        'month': future_dates,
        'revenue': future_preds,
        'is_forecast': True
    })
    
    data['is_forecast'] = False
    return pd.concat([data, forecast_df], ignore_index=True)