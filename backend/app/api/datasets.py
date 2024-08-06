from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, col, func, select  # noqa: F401

from backend.app.models.dataset import Dataset
from backend.app.models.site import Site
from backend.app.models.voc_subclass import VocSubclass
from backend.app.utils.query_utils import (
    get_all_voc_subclass_ancestor_ids_by_voc_subclass_id,
)
from backend.database import get_db

dataset_router = APIRouter(prefix="/datasets", tags=["Datasets"])


@dataset_router.post("/")
async def create_dataset(
    dataset: Dataset, db: Annotated[Session, Depends(get_db)]
):
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


@dataset_router.get("/")
async def get_datasets(db: Annotated[Session, Depends(get_db)]):
    return db.query(Dataset).all()


@dataset_router.get("/by-site/{site_id}")
async def get_datasets_by_site_id(
    site_id: int, db: Annotated[Session, Depends(get_db)]
):
    statement = select(Dataset).where(Dataset.site_id == site_id)
    return db.exec(statement).all()


@dataset_router.get("/by-country/{country-name}")
async def get_datasets_by_country(
    country: str, db: Annotated[Session, Depends(get_db)]
):
    statement = select(Dataset).where(Dataset.site.country == country)
    return db.exec(statement).all()


@dataset_router.get("/by-subclass/{subclass_name}")
async def get_datasets_by_subclass_name(
    subclass_name: str, db: Annotated[Session, Depends(get_db)]
):

    # get subclass_id by name
    given_subclass_id = (
        db.exec(select(VocSubclass).where(VocSubclass.name == subclass_name))
        .one()
        .id
    )

    # init array for relevant datasets
    relevant_datasets = []

    # get all datasets from db
    datasets = db.exec(select(Dataset))

    # TODO: There might be a more elegant solution for this function
    #  by utilizing more sql functionality
    for dataset in datasets:
        contained_voc_subclasses = []
        subclasses = dataset.voc_subclasses
        for subclass in subclasses:
            # for every dataset, collect the ancestors
            #   for each associated voc_subclass
            ancestor_ids = get_all_voc_subclass_ancestor_ids_by_voc_subclass_id(
                subclass.id, db
            )
            for ancestor_id in ancestor_ids:
                contained_voc_subclasses.append(ancestor_id)

        for voc in dataset.vocs:
            # do the same for all the VOCs and their voc_subclasses
            if voc.voc_subclass:
                ancestor_ids = (
                    get_all_voc_subclass_ancestor_ids_by_voc_subclass_id(
                        voc.voc_subclass.id, db
                    )
                )
                for ancestor_id in ancestor_ids:
                    contained_voc_subclasses.append(ancestor_id)

        contained_voc_subclasses = list(set(contained_voc_subclasses))
        # if any of the linked voc_subclasses or ancestors
        #   are equal to the given_subclass_id
        #   (i.e. the voc_subclass we are looking for),
        #   add the dataset to the relevant datasets
        if given_subclass_id in contained_voc_subclasses:
            relevant_datasets.append(dataset)

    if not relevant_datasets:
        raise HTTPException(
            status_code=404,
            detail="No datasets found that refer to your"
            " specified VOC subgroup",
        )

    return relevant_datasets


@dataset_router.get(
    "/datasets/by-area/{min_lon}/{min_lat}/{max_lon}/{max_lat}/"
)
async def get_datasets_within_area(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    db: Annotated[Session, Depends(get_db)],
):
    # Define the bounding box
    bbox = (
        f"POLYGON(({min_lon} {min_lat}, {min_lon} {max_lat}, {max_lon}"
        f" {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}))"
    )

    # Query to get datasets within the specified bounding box
    statement = select(Dataset).where(
        Dataset.site.func.ST_Within(
            Site.geo_location, func.ST_GeomFromText(bbox, 4326)
        )
    )

    results = db.exec(statement).all()

    if not results:
        raise HTTPException(
            status_code=404, detail="No datasets found in the specified area"
        )

    return results
