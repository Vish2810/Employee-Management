from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from loguru import logger
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2.extras
from . import get_db, get_raw_db
from sqlalchemy.orm import Session
from src.db.alchemy_models import employee_table

router = APIRouter()


# class Employee(BaseModel):
#     e_id: int
#     e_name: str
#     designation: str
#     email: str
#     contact_no: str
#

class CreateEmployee(BaseModel):
    e_id: int
    e_name: str
    designation: str
    email: str
    contact_no: str
    o_id: int


class ModifyEmployee(BaseModel):
    e_id: Optional[int]
    e_name: Optional[str]
    designation: Optional[str]
    email: Optional[str]
    contact_no: Optional[str]


@router.get('/Employee/ViewEmployeeByEid/{e_id}', tags=['View Employees'])
def view_employee_by_eid(
        e_id: int,
        db: Session = Depends(get_db),
        rdb=Depends(get_raw_db)
):
    try:
        res = db.query(employee_table).filter_by(e_id=e_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{e_id} is not exist')
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
           select * from employee  where e_id={e_id} ;
           """)
        return cursor.fetchall()
    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.get('/Employee/ViewAll', tags=['View Employees'])
def view_all_employee(
        db: Session = Depends(get_db),
        rdb=Depends(get_raw_db),
):
    try:
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
           select * from employee ; 
           """)
        return cursor.fetchall()

    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.post('/Employee/Create', tags=['Manage Employees'])
def create_new_employee(
        emp: CreateEmployee,
        db: Session = Depends(get_db)
):
    try:
        new_employee = employee_table(
            e_id=emp.e_id,
            e_name=emp.e_name,
            designation=emp.designation,
            email=emp.email,
            contact_no=emp.contact_no
        )
        db.add(new_employee)
        db.commit()
        return {
            "detail": "success",
        }

    except Exception as e:
        logger.error(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.put('/Employee/Modify', tags=['Manage Employees'])
def modify_employee_by_eid(
        e_id: int,
        modify_emp: ModifyEmployee = Body(...),
        db: Session = Depends(get_db)
):
    try:
        res = db.query(employee_table).filter_by(e_id=e_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{e_id} is not exist')
        db.query(employee_table).filter_by(e_id=e_id).update(modify_emp.dict(exclude_unset=True))
        db.commit()
        return {
            "details": "success"
        }
    except HTTPException as e:
        logger.error(f'{e}')
        raise e
    except Exception as e:
        logger.error(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')


@router.delete('/Employee/Delete', tags=['Manage Employees'])
def delete_employee_by_eid(
        e_id: int,
        db: Session = Depends(get_db),
        rdb=Depends(get_raw_db)
):
    try:
        res = db.query(employee_table).filter_by(e_id=e_id).all()
        if len(res) == 0:
            raise HTTPException(status_code=404, detail=f'{e_id} is not exist')
        cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(f"""
           delete from employee_table  where e_id={e_id} ;
           """)
        rdb.commit()

        return {
            "details": "success"
        }

    except HTTPException as e:
        logger.debug(f'{e}')
        raise e
    except Exception as e:
        logger.debug(f'{e}')
        raise HTTPException(status_code=500, detail=f'{e}')
