import pytest
from toolz import dissoc
from pydantic import ValidationError
from typing import Any, Dict, List


def check_required_fields(required_fields: List[str], valid_data, dto):
    for field in required_fields:
        with pytest.raises(ValidationError):
            data = {key: item for key,
                    item in valid_data.items() if key != field}
            dto(**data)


def check_optional_fields(optional_fields: List[str], valid_data, dto):
    for field in optional_fields:
        data = dissoc(valid_data, field)
        assert dto(**data)


def check_require_at_least_one_field(dto, data: Dict[str, Any]):
    with pytest.raises(ValueError):
        dto(**data)
