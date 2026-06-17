from fastapi import APIRouter, Query, HTTPException, status
from services.trend_service import generate_trend_forecast
from models.schemas import TrendResponse

router = APIRouter(prefix="/api", tags=["TrendRadar"])

@router.get("/trends", response_model=TrendResponse)
def get_trends(
    niche: str = Query(None, description="E.g., fitness, food, gaming, lifestyle"),
    platform: str = Query(None, description="E.g., instagram, tiktok, youtube")
):
    try:
        forecast_result = generate_trend_forecast(niche, platform)
        return forecast_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Trend forecasting failed: {str(e)}"
        )
