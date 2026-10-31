from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core import Inventory

"""Local operator interface. Not exposed as an MCP tool."""


app = FastAPI(title="Inventory operator console")


@lru_cache
def service():
    return Inventory()


class Approval(BaseModel):
    fingerprint: str


@app.get("/api/inventory")
def inventory(q: str = ""):
    return service().search(q)


@app.post("/api/orders/{oid}/approve")
def approve(oid: str, body: Approval):
    try:
        return service().approve(oid, body.fingerprint)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e
