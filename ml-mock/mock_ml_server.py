from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock ML Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/recommendations")
async def get_recommendations():
    # Возвращаем фиксированные рекомендации для тестов
    return {"recommendations": [1, 2, 3, 4, 5]}

@app.get("/recommendations/{user_id}")
async def get_user_recommendations(user_id: int, count: int = 10):
    # Возвращаем фиксированные рекомендации для тестов
    recommendations = list(range(1, count + 1))
    return {"user_id": user_id, "recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)