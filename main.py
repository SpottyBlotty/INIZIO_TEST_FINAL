import os
import httpx
import csv
import io
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "62f922ff06787a89106a50ae9c3f5b5a93c7234b")

@app.get("/api/search")
async def search_google(q: str = Query(...)):
    serper_url = "https://google.serper.dev/search"
    request_headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(serper_url, headers=request_headers, json={"q": q, "num": 10})
            response.raise_for_status()
            search_data = response.json()
            
        formatted_results = []
        for index, item in enumerate(search_data.get("organic", []), start=1):
            formatted_results.append({
                "position": index,
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
            
        return {"query": q, "results": formatted_results}
        
    except Exception as error_message:
        raise HTTPException(status_code=500, detail=str(error_message))

@app.post("/api/export/csv")
async def generate_csv(data: dict):
    memory_file = io.StringIO()
    memory_file.write('\ufeff') 
    
    csv_writer = csv.writer(memory_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    
    csv_writer.writerow(["Position", "Title", "URL", "Snippet"])
    
    search_results = data.get("results", [])
    for row in search_results:
        csv_writer.writerow([
            row.get("position", ""),
            row.get("title", ""),
            row.get("link", ""),
            row.get("snippet", "")
        ])
    
    final_csv_content = memory_file.getvalue()
    
    return Response(
        content=final_csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"}
    )

app.mount("/", StaticFiles(directory="public", html=True), name="static")