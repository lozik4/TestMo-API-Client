from datetime import date, datetime
from typing import Literal, Union

DateIso = Union[date, datetime, str]
Order = Literal["asc", "desc"]
BoolFilter = Literal[0, 1, None]
