from .auth import router as auth_router
from .patients import router as patients_router
from .health_data import router as health_data_router
from .alerts import router as alerts_router
from .recommendations import router as recommendations_router
from .doctors import router as doctors_router
from .chat import router as chat_router

all_routers = [
    auth_router,
    patients_router,
    health_data_router,
    alerts_router,
    recommendations_router,
    doctors_router,
    chat_router
]

__all__ = ["all_routers"]
