from fastapi import FastAPI
from .import models
from .database import engine

from .routers import product, seller

app = FastAPI(
    title="Product APIs",
    description="Get details of products on our website",
    terms_of_service= "https://example.com",
    contact={
        "Developer Name": "Rajat",
        "website": "https://example.com",
        "email": "demo@gmail.com"
    },
    license_info={
        "name": "GPLv3",
        "url": "https://example.com"
    },
    # docs_url="/documentation", redoc_url=None

)

app.include_router(product.router)
app.include_router(seller.router)


models.Base.metadata.create_all(engine)


