from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection

app = FastAPI()


@app.get("/ping")
def ping():
    return {"message": "pong"}

class Film(BaseModel):
    id: int | None = None
    nom: str
    note: float | None = None
    dateSortie: int
    image: str | None = None
    video: str | None = None
    genreId: int | None = None

@app.post("/film")
async def createFilm(film : Film):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO Film (Nom,Note,DateSortie,Image,Video)  
            VALUES('{film.nom}',{film.note},{film.dateSortie},'{film.image}','{film.video}') RETURNING *
            """)
        res = cursor.fetchone()
        print(res)
        return res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/film")
async def getFilm(page=1, per_page=20, genre_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if genre_id == None :
            cursor.execute(f"""
            SELECT * FROM Film LIMIT {per_page} OFFSET {per_page * page }
            ORDER BY "Release_Date" DESC
            """)
        else:
            cursor.execute(f"""
            SELECT * FROM Film WHERE "Genre" = {genre_id} LIMIT {per_page} OFFSET {per_page * page }
            ORDER BY "Release_Date" DESC
            """)
        res = cursor.fetchone()
        print(res)
        return res

@app.get("/film/{film_id}")
async def getFilmbyID(film_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM Film WHERE "Title" = {film_id}
            """)
        res = cursor.fetchone()
        print(res)
        return res


class User(BaseModel):
    id: int | None = None
    email: str | None = None
    pseudo: str | None = None
    password: str | None = None