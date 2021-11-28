import pytest
from pydantic import ValidationError
from typing import List


def check_required_fields(required_fields: List[str], valid_data, dto):
    for field in required_fields:
        with pytest.raises(ValidationError):
            data = {key: item for key,
                    item in valid_data.items() if key != field}
            dto(**data)


def check_optional_fields(optional_fields: List[str], valid_data, dto):
    for field in optional_fields:
        data = {key: value for key, value in valid_data.items()
                if key != field}
        assert dto(**data)
