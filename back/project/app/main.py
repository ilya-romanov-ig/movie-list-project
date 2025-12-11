from fastapi import FastAPI
from app.routers import (
    films,
    actors,
    users,
    auth,
    favorites,
    ratings,
    watched,
    search,
    home,
    genres,
)

app = FastAPI(title="Movies API")

# Подключение роутеров (пока они пустые)
app.include_router(auth.router)
app.include_router(films.router)
app.include_router(actors.router)
app.include_router(users.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
app.include_router(watched.router)
app.include_router(search.router)
app.include_router(home.router)
app.include_router(genres.router)

import os
from app.db import DATABASE_URL

#print("DATABASE_URL =", DATABASE_URL)


import pathlib
#print("WORKDIR:", pathlib.Path().absolute())
#print("FILES:", [p.name for p in pathlib.Path().absolute().iterdir()])





