
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection
import jwt

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


@app.get("/films")
async def getFilm(page:int=1, per_page:int=20, genre_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        if genre_id == None:
            cursor.execute(f"""
                SELECT COUNT(*) FROM Film
            """)
        else:
            cursor.execute(f"""
                SELECT COUNT(*) FROM Film WHERE Genre_ID = {genre_id}
            """)
        total = cursor.fetchone()[0]


        if genre_id == None :
            cursor.execute(f"""
            SELECT * FROM Film ORDER BY DateSortie DESC
            LIMIT {per_page} OFFSET {per_page * (page-1) }
            """)
        else:
            cursor.execute(f"""
            SELECT * FROM Film WHERE Genre_ID = {genre_id} ORDER BY DateSortie DESC
            LIMIT {per_page} OFFSET {per_page * (page-1) }
            """)
        res = cursor.fetchall()
        print(res)
        return {"data" : res, "total" : total, "page" : page , "per_page" : per_page }

@app.get("/films/{film_id}")
async def getFilmbyID(film_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM Film WHERE Id = {film_id}
            """)
        res = cursor.fetchone()

        if res == None :
            raise HTTPException(status_code=404, detail=f"Film not found")
        print(res)
        return res

@app.get("/genres")
async def getGenre():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT DISTINCT Genre_Id, Type FROM Film JOIN Genre ON Film.Genre_Id = Genre.Id
            """)
        res = cursor.fetchall()
        print(res)
        return res


class User(BaseModel):
    id: int | None = None
    email: str | None = None
    pseudo: str | None = None
    motdepasse: str | None = None


@app.post("/auth/register")
async def createUser(user : User):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO Utilisateur (AdresseMail, Pseudo, MotDePasse)  
            VALUES('{user.email}','{user.pseudo}','{user.motdepasse}') RETURNING *
            """)
        res = cursor.fetchone()
        print(res)
        return res



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)