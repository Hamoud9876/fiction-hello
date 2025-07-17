from fastapi import FastAPI
from fastapi.responses import JSONResponse
from core.src.main import main

app = FastAPI()


@app.get("/healthcheck")
def get_healthcheck():
    return {"status": "The server is running"}


@app.get("/create_records")
def get_create_records(num_records: int | None = 1):
    if num_records == 0:
        return JSONResponse(content={"status": "Failed"}, status_code=400)

    main(num_records)
    return {"status": "Ok", "records_created": num_records}
