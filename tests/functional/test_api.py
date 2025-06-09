from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)

# Test Endpoint 1
url1 = "http://127.0.0.1:8000/"

def test_default_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing
    WHEN the '/' endpoint is requested (GET)
    THEN check for 200 status return code and that "health_check` message was received as "ok"
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "OK"}

def test_info_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing
    WHEN the '/info' endpoint is requested (GET)
    THEN check for 200 status return code and that
        {"name": "XGBoost Forecasting", "description": "An `eXtreme Gradient Boosting (XGBoost)` regression prediction model to forecast MegaWatt usage for Dominion Energy taking advantage of the high accuracy and performance of XGBoost models."}
        was received
    """
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {"name": "XGBoost Forecasting", "description": "An `eXtreme Gradient Boosting (XGBoost)` regression prediction model to forecast MegaWatt usage for Dominion Energy taking advantage of the high accuracy and performance of XGBoost models."}

def test_plot_forecast_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing
    WHEN the '/plot-forecast' endpoint is requested (GET)
    THEN check for 200 status return code and that 
        an image was produced by checking the response type
    """
    response = client.get("/plot-forecast")
    assert response.status_code == 200
    assert  response.headers["Content-Type"] == "image/png"

def test_data_used_for_forecasting_html_endpoint() -> None:
    """ 
    GIVEN a FASTAPI application configured for testing and
    WHEN the 'data_used_for_forecasting_html' endpoint is requested (GET)
    THEN check for 200 status return code and that HTML was returned
        and verifies that HTML template code is in the response
    """
    response = client.get("/data_used_for_forecasting_html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>DataFrame Display</title>" in response.text #check's that reponse uses my template