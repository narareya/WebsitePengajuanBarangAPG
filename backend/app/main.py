from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import departement_routes, user_routes, auth_routes, product_routes, request_routes, request_detail_routes, dashboard_routes,activity_log_routes

app = FastAPI(title="BEAmazink API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departement_routes.router)
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(request_routes.router)
app.include_router(request_detail_routes.router)
app.include_router(product_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(activity_log_routes.router)

@app.get("/")
def root():
    return {"message": "API is running"}