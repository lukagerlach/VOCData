from fastapi import FastAPI

from backend.app.api.contacts import contact_router
from backend.app.api.datasets import dataset_router
from backend.app.api.publications import publication_router
from backend.app.api.sites import site_router
from backend.app.api.voc_subclasses import voc_subclass_router
from backend.app.api.vocs import voc_router
from backend.database import init_db

# include api routers
app = FastAPI()
app.include_router(dataset_router)
app.include_router(site_router)
app.include_router(voc_router)
app.include_router(voc_subclass_router)
app.include_router(contact_router)
app.include_router(publication_router)

# initialize database connection
init_db()
