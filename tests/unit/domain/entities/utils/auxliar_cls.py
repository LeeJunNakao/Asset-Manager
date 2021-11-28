from typing_extensions import Required

from tests.unit.domain.entities.utils.auxiliar_fns import check_required_fields, check_optional_fields


class DefaultEntityTests:
    required_fields = []
    optional_fields = []
    dto = None

    def test_required_fields(self, valid_data):
        check_required_fields(self.required_fields,
                              valid_data, self.dto)

    def test_optional_fields(self, valid_data):
        check_optional_fields(self.optional_fields, valid_data, self.dto)

    def test_valid_fields(self, valid_data):
        assert self.dto(**valid_data)
