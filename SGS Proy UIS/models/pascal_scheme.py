import marshmallow
import marshmallow_dataclass
class PascalScheme(marshmallow.Schema):
    """A Schema that marshals data with uppercased keys."""

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = (field_obj.data_key or field_name).title()


