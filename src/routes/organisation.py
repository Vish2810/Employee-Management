from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from loguru import logger
from . import get_db, get_raw_db
from src.db.alchemy_models import organisation_table
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extras

router = APIRouter()


class CreateOrganisation(BaseModel):
    o_id: int
    o_name: str
    description: str


class ModifyOrganisation(BaseModel):
    o_id: Optional[int]
    o_name: Optional[str]
    description: Optional[str]


@router.get('/Organisation/ViewOrganisationByOId/{o_id}', tags=['View Organisation'])
def view_organisation_by_oid(
        o_id: int,
        db: Session = Depends(get_db),
        rdb=Depends(get_raw_db)
):
    try:
        res = db.query(organisation_table).filter_by(o_id=o_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{o_id} is not exist')
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
            select * from organisation where o_id ={o_id} ;
            """)
        return cursor.fetchall()
    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.get('/Organisation/ViewAll/', tags=['View Organisation'])
def view_all_organisation(
        db: Session = Depends(get_db),
        rdb=Depends(get_raw_db)
):
    try:
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
        select * from organisation ;
        """)
        return cursor.fetchall()
    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.post('/Organisation/CreateOrganisation', tags=['Manage Organisation'])
def create_organisation(
        org: CreateOrganisation,
        db: Session = Depends(get_db)
):
    try:
        new_organisation = organisation_table(
            o_id=org.o_id,
            o_name=org.o_name,
            description=org.description,
            created_datetime=datetime.now()
        )
        db.add(new_organisation)
        db.commit()
        return {
            "detail": "success",
        }
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.put('/Organisation/Modify', tags=['Manage Organisation'])
def modify_organisation_by_oid(
        o_id: int,
        modify_org: ModifyOrganisation = Body(...),
        db: Session = Depends(get_db)
):
    try:
        res = db.query(organisation_table).filter_by(o_id=o_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{o_id} is not exist')
        db.query(organisation_table).filter_by(o_id=o_id).update(modify_org.dict(exclude_unset=True))
        db.commit()
        return {
            "detail": "Success"
        }
    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')

@router.delete('/Organisation/Delete', tags=['Manage Organisation'])
def delete_organisation_by_oid(
        o_id: int,
        db:Session = Depends(get_db),
        rdb=Depends(get_raw_db)
):
    try:
        res = db.query(organisation_table).filter_by(o_id=o_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{o_id} does not exist')
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
            delete from organisation where o_id = {o_id};
            """)
        rdb.commit()

        return{
            "detail": "Success"
        }
    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')

