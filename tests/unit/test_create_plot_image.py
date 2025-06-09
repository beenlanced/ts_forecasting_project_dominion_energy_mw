import io
from pathlib import Path

import pandas as pd
import pytest
from src.app import create_plot_image


# Get Path to the /src/eda folder - contains theXGBoost model and future data set to show forecasting
eda_directory_path = Path(__file__).resolve().parent.parent.parent /"src/eda"
model_path = f"{eda_directory_path.joinpath("model.json")}"
future_values_path = f"{eda_directory_path.joinpath("future_values.csv")}"

#Get the feature data for input into ML model
future_values_df = pd.read_csv(future_values_path)

#Convert first column to get datetime
old_name = future_values_df.columns[0]
future_values_df = future_values_df.rename(columns={old_name:"Datetime"})
future_values_df = future_values_df.set_index("Datetime")
future_values_df.index = pd.to_datetime(future_values_df.index)

# Define the test data with pytext fixtures
test_data = [
    (future_values_df, model_path),
]

@pytest.mark.parametrize("future_values_df, model_path", test_data)
def test_create_plot_image(
    future_values_df: pd.DataFrame, 
    model_path: str
) -> None :
    """
    GIVEN a Pandas dataframe of feature values and variables used as input to an ML model and the ML model
    WHEN the dataframe's feature values are used as input to the ML model
    THEN ML model will produce forecast data which get's rendered as a Matplotlib plot
    """
    result = create_plot_image(future_values_df, model_path)
    assert isinstance(result, io.BytesIO)