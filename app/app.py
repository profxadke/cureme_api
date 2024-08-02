#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from .routers import users, medications, appointments, procedures, reminders, notifications, contacts, allergies, medical_conditions, labs
from .database import engine, init_db
from . import models


# Initialize database.
init_db()


description = """
CureMe Medial App's REST API helps you do awesome stuff. 🚀

## Users

You will be able to:

* **Create users**
* **Read users**
* **Read user**
* **Update user**
* **Delete user**

<h3>
<blockquote><i> And so on.. </i></blockquote>
</h3>
"""

"""
# Medications

You will be able to:

* **Create medications**
* **Read medications**
* **Read medication**
* **Update medication**
* **Delete medication**

# Appointments

You will be able to:

* **Create appointments**
* **Read appointments**
* **Read appointment**
* **Update appointment**
* **Delete appointment**

# Reminders

You will be able to:

* **Create reminders**
* **Read reminders**
* **Read reminder**
* **Update reminder**
* **Delete reminder**

# Notifications

You will be able to:

* **Create notifications**
* **Read notifications**
* **Read notification**
* **Update notification**
* **Delete notification**

# Contacts

You will be able to:

* **Create contacts**
* **Read contacts**
* **Read contact**
* **Update contact**
* **Delete contact**

# Procedures

You will be able to:

* **Create procedures**
* **Read procedures**
* **Read procedure**
* **Update procedure**
* **Delete procedure**

# Allergies

You will be able to:

* **Create allergies**
* **Read allergies**
* **Read allergy**
* **Update allergy**
* **Delete allergy**

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also supposed to be implemented here.",
    },
    {
        "name": "medications",
        "description": "Operations with medications.",
    },
    {
        "name": "appointments",
        "description": "Operations with appointments.",
    },
    {
        "name": "reminders",
        "description": "Operations with reminders.",
    },
    {
        "name": "notifications",
        "description": "Operations with notifications",
    },
    {
        "name": "contacts",
        "description": "Operations with contacts.",
    },
    {
        "name": "procedures",
        "description": "Operations with procedures.",
    },
    {
        "name": "allergies",
        "description": "Operations with allergies.",
    },
    {
        "name": "medical_conditions",
        "description": "Operations with medical_conditions.",
    },
    {
        "name": "labs",
        "description": "Labs operations with users.",
    },
    {
        "name": "others",
        "description": "Manage others. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]; api = FastAPI(
    title="CureMe API",
    description=description,
    summary='CureMe Medical App\'s REST API.',
    version="0.0.1",
    terms_of_service="#",
    contact={
        "name": "profxadke",
        "url": "http://is.gd/nikhila",
        "email": "xadkeg@duck.com",
    },
    license_info={
        "name": "GNU General Public License v3 (GPL-3)",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
    openapi_tags=tags_metadata,
    docs_url=None, redoc_url=None
)


def custom_openapi():
    if api.openapi_schema:
        return api.openapi_schema
    openapi_schema = get_openapi(
        title="CureMe Medial App's REST API",
        version="0.0.1",
        summary="CureMe Medical App's REST API.",
        description=description,
        routes=api.routes,
        terms_of_service="#",
        contact={
            "name": "profxadke",
            "url": "http://is.gd/nikhila",
            "email": "xadkeg@duck.com",
        },
        license_info={
            "name": "GNU General Public License v3 (GPL-3)",
            "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
        }
    ); openapi_schema["info"]["x-logo"] = {
        "url": "http://127.0.0.1:8888/static/cureme.png"
    }; api.openapi_schema = openapi_schema
    openapi_schema['tags'] = tags_metadata
    return api.openapi_schema


api.openapi = custom_openapi


# Include routers
api.include_router(users.router, prefix="/users", tags=["users"])
api.include_router(medications.router, prefix="/medications", tags=["medications"])
api.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api.include_router(reminders.router, prefix="/reminders", tags=["reminders"])
api.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api.include_router(procedures.router, prefix="/procedures", tags=["procedures"])
api.include_router(allergies.router, prefix="/allergies", tags=["allergies"])
api.include_router(medical_conditions.router, prefix="/medical_conditions", tags=["medical_conditions"])
api.include_router(labs.router, prefix="/labs", tags=["labs"])


@api.get("/", include_in_schema=False)
def redirect_docs():
    return RedirectResponse(url="/docs/")


'''
@api.get("/docs", include_in_schema=False)
def redirect_redoc():
    return RedirectResponse(url="/redoc/")
'''


@api.get("/favicon.ico", include_in_schema=False)
def respond_favicon():
    return FileResponse("./app/static/favicon.ico")


@api.get("/favicon.png", include_in_schema=False)
def respond_favicon_png():
    return FileResponse("./app/static/favicon.png")


@api.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title="CureMe API - Docs", swagger_favicon_url="/favicon.ico")


@api.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/openapi.json", title="CureMe API - ReDoc", redoc_favicon_url="/favicon.ico")


@api.get("/ping")
def pong():
    return {"ping": "pong!"}


api.mount("/static", StaticFiles(directory="./app/static"), name="static")


if __name__ == "__main__":
    __import__('uvicorn').run('app:api', host="0.0.0.0", port=8888, reload=True)

