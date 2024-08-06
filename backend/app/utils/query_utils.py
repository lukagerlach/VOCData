from sqlalchemy.orm import aliased
from sqlmodel import SQLModel, select

from backend.app.models.voc_subclass import VocSubclass


def get_all_voc_subclass_ancestor_ids_by_voc_subclass_id(
    voc_subclass_id, session
) -> list[int]:
    """
    Retrieve all ancestor IDs for a given VocSubclass ID using a recursive CTE.

    :param voc_subclass_id: The ID of the VocSubclass
        for which to find ancestors.
    :type voc_subclass_id: int
    :param session: SQLAlchemy session used to execute the query.
    :type session: sqlalchemy.orm.session.Session

    :return: A list of ancestor IDs of the specified VocSubclass, including all
             direct and indirect parents.
    :rtype: list[int]
    """
    return __get_all_ancestors__(
        VocSubclass, "parent_voc_category_id", voc_subclass_id, session
    )


def __get_all_ancestors__(
    object_class: SQLModel, parent_id_field_name: str, object_id, session
) -> list[int]:
    """
    Find all ancestor IDs for a given object using a recursive CTE.

    :param session: SQLAlchemy session
    :type session: sqlalchemy.orm.session.Session
    :param object_class: The SQLAlchemy model class to query
    :type object_class: SQLModel
    :param parent_id_field_name: The name of the field
        that references the parent ID
    :type parent_id_field_name: str
    :param object_id: ID of the starting object to find the ancestors for
    :type object_id: int
    :return: List of ancestor IDs
    :rtype: list[int]
    """

    # TODO: this function should be more robust and implement some
    #  error handling, e.g. not matching parent_id_field_name fields...
    #  I'm not sure if this level of abstraction is even beneficial, maybe just
    #  create new concrete functions if more tables get hierarchical.

    # Create the base CTE to start with the provided object ID
    base_cte = (
        select(object_class)
        .where(object_class.id == object_id)
        .cte(name="base_cte", recursive=True)
    )

    # Aliases for the base_cte to reference later
    cte_alias = aliased(base_cte, name="cte_alias")

    # Define the recursive part of the CTE, creating a list of all parents
    recursive_cte = base_cte.union_all(
        select(object_class)
        # TODO: rn this only works if the object_class field to join by
        #  is called id. This could be designed more abstract
        .join(cte_alias, cte_alias.c[parent_id_field_name] == object_class.id)
    )

    # Execute the query and retrieve all ancestor IDs
    ancestor_ids = session.execute(select(recursive_cte.c.id)).scalars().all()

    return ancestor_ids
