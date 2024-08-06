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
    """
    Create a new dataset.

    This endpoint allows the creation of a new dataset in the database.

    :param dataset: The dataset information to be added.
    :type dataset: Dataset
    :param db: The database session.
    :type db: Session
    :return: The created dataset.
    :rtype: Dataset
    """

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


@dataset_router.get("/")
async def get_datasets(db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve all datasets.

    This endpoint retrieves all datasets stored in the database.

    :param db: The database session.
    :type db: Session
    :return: A list of all datasets.
    :rtype: list[Dataset]
    """

    return db.query(Dataset).all()


@dataset_router.get("/by-site/{site_id}")
async def get_datasets_by_site_id(
    site_id: int, db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve datasets by site ID.

    This endpoint retrieves datasets associated with a specific site.

    :param site_id: The ID of the site.
    :type site_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of datasets associated with the specified site.
    :rtype: list[Dataset]
    """

    statement = select(Dataset).where(Dataset.site_id == site_id)
    return db.exec(statement).all()


@dataset_router.get("/by-country/{country-name}")
async def get_datasets_by_country(
    country: str, db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve datasets by country.

    This endpoint retrieves datasets associated with a specific country.

    :param country: The name of the country.
    :type country: str
    :param db: The database session.
    :type db: Session
    :return: A list of datasets associated with the specified country.
    :rtype: list[Dataset]
    """

    statement = select(Dataset).where(Dataset.site.country == country)
    return db.exec(statement).all()


@dataset_router.get("/by-subclass/{subclass_name}")
async def get_datasets_by_subclass_name(
    subclass_name: str, db: Annotated[Session, Depends(get_db)]
):
    """
    Retrieve datasets by VOC subclass name.

    This endpoint retrieves datasets associated with a specific VOC subclass.
    This checks multiple cases:

        - is VOC subclass directly associated with dataset?
        - is VOC subclass indirectly associated with dataset, \
        i.e. is an ancestor of directly linked VOC Subclass
        - is VOC subclass associated with specific VOC, \
        that is directly associated with this dataset?
        - is VOC subclass indirectly associated with specific VOC, \
        that is directly associated with this dataset, i.e.\
        is VOC Subclass ancestor of directly linked VOCs Subclass

    :param subclass_name: The name of the VOC subclass.
    :type subclass_name: str
    :param db: The database session.
    :type db: Session
    :return: A list of datasets associated with the specified VOC subclass.
    :rtype: list[Dataset]
    :raise HTTPException: no datasets found for subclass

    """

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
    """
    Retrieve datasets within a specified area.

    This endpoint retrieves datasets that are \
    located within a specified bounding box.

    :param min_lon: Minimum longitude of the bounding box.
    :type min_lon: float
    :param min_lat: Minimum latitude of the bounding box.
    :type min_lat: float
    :param max_lon: Maximum longitude of the bounding box.
    :type max_lon: float
    :param max_lat: Maximum latitude of the bounding box.
    :type max_lat: float
    :param db: The database session.
    :type db: Session
    :return: A list of datasets within the specified bounding box.
    :rtype: list[Dataset]
    :raise HTTPException: no datasets found in that area
    """

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
