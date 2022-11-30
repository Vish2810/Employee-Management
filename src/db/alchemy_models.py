from loguru import logger
from .alchemy import Base

try:
    employee_table = Base.classes.employee
    organisation_table = Base.classes.organisation

except Exception as err:
    logger.error("error while creating models - {}".format(err))
