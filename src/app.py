import io
from pathlib import Path

from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import matplotlib

# displaying the image in the user's browser on client side with matplotlib.use
# Use the "Agg" backend for non-GUI environments
# AGG used in the example above is a backend that renders graphs as PNGs.
# matplotlib.use() must be used before importing pyplot so placing it here
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xgboost as xgb

# displaying the image in the user's browser on client side with matplotlib.use
# Use the "Agg" backend for non-GUI environments
# AGG used in the example above is a backend that renders graphs as PNGs.
matplotlib.use("Agg")

# Get Base path
BASE_DIR = Path(__file__).resolve().parent.parent
template_path=str(Path(BASE_DIR, "templates"))

# Get Path to the /eda folder - contains theXGBoost model and future data set to show forecasting
eda_directory_path = Path(__file__).resolve().parent /"eda"
model_path = f"{eda_directory_path.joinpath("model.json")}"
future_values_path = f"{eda_directory_path.joinpath("future_values.csv")}"

#Get the feature data for input into ML model
future_values_df = pd.read_csv(future_values_path)

#Convert first column to get datetime
old_name = future_values_df.columns[0]
future_values_df = future_values_df.rename(columns={old_name:"Datetime"})
future_values_df = future_values_df.set_index("Datetime")
future_values_df.index = pd.to_datetime(future_values_df.index) #convert index from string to datatime type

def create_plot_image(future_values_df: pd.DataFrame, model_path: str) -> io.BytesIO:
    """
    Method to generate a plot of future forecast data

    Args:
        future_values_df (pd.DataFrame): Pandas dataframe of feature values and variables used as input to ML model

        model_path (str): File path to a derived XGBoost model.

    Returns:
        (io.BytesIO): Matplotlib image out of the forecasted MegaWatt usage based on future_values_df inputs.
    """
    # Get XGBoost model and future_values for prediction
    FEATURES = ["dayofyear", "hour", "dayofweek", "quarter", "month", "year",
                    "lag1", "lag2", "lag3"]
    color_palette = sns.color_palette("tab10") #seaborn color palette

    reg = xgb.XGBRegressor()
    reg.load_model(model_path)
    future_values_df["pred"] = reg.predict(future_values_df[FEATURES])

    future_values_df["pred"].plot(figsize=(10, 5),
                                color=color_palette[1],
                                ms=1, lw=1,
                                title="XGBoost Future Prediction for Dominon Energy MegaWatt (MW) Hourly Usage (2018-08-03 - 2019-08-01)")
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    plt.close()
    return img_buf

# Create FastAPI object API - for rendering the results of requests to the AI/ML model
app = FastAPI()
templates = Jinja2Templates(directory=template_path) # Create a 'templates' directory

# API operations - GET requests for various endpoints
@app.get("/")
def health_check() -> dict[str, str]:
    """ 
    FASTAPI route that returns simple dictionary/JSON message to show site

    Returns:
        (dict[str, str]): Dict with simple message for entry API show "ok" message
    """
    return {"health_check": "OK"}

@app.get("/info")
def info() -> dict[str, str]:
    """
    FASTAPI route that returns simple dictionary/JSON message to show site

    Returns:
        (dict[str, str]): Dict with text describing he purpose of the Fast API web application
    """
    return {"name": "XGBoost Forecasting", "description": "An `eXtreme Gradient Boosting (XGBoost)` regression prediction model to forecast MegaWatt usage for Dominion Energy taking advantage of the high accuracy and performance of XGBoost models."}

# async def allows you to write efficient, responsive programs, 
# especially for I/O-bound tasks, by enabling the program to perform 
# other work while waiting for slow operations to finish.
@app.get("/plot-forecast")
async def get_plot(background_tasks: BackgroundTasks) -> Response:
    """
    Method to Plot Matplotlib image of XGBoost forecast model from this FAST API route

    Args:
        background_tasks (BackgroundTasks): Runs task to close image buffer after sending image

    Returns:
        (Response): Returns an image that is rendered in the this FAST API route
    """
    img_buf = create_plot_image(future_values_df, model_path)
    background_tasks.add_task(img_buf.close) # Ensure the buffer is closed after sending

    # Set the Content-Disposition header, so that the image can be viewed in the browser
    headers = {"Content-Disposition": 'inline; filename="plot.png"'}
    return Response(img_buf.getvalue(), media_type="image/png", headers=headers)

@app.get("/data_used_for_forecasting_html", response_class=HTMLResponse)
async def get_dataframe_as_html(request: Request) -> str:
    """
    Method to post Forecast input feature dataframe in HTML format from this FAST API route.

    Args:
        request (Request): HTML request

    Returns:
        (Jinja2Templates.TemplateResponse): Dataframe rendered in HTML format of dataframe_template.html
    """
    return templates.TemplateResponse("dataframe_template.html", {"request": request, "dataframe_html": future_values_df.to_html()})
