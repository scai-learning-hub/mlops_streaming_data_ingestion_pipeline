import pandera as pa
from pandera import Column, Check

OrderSchema = pa.DataFrameSchema(
    {
        "order_id": Column(pa.Int64, Check.gt(0), nullable=False, coerce=True),
        "user_id": Column(pa.Int64, nullable=False, coerce=True),
        "amount": Column(float, Check.gt(0), nullable=False, coerce=True),
        "country": Column(str, Check.isin(["IN", "US", "UK", "FR"]), nullable=False, coerce=True),
        "channel": Column(str, Check.isin(["web", "app", "partner"]), nullable=False, coerce=True),
    },
    strict=True,
    coerce=True,
)

    # {"order_id": 11, "user_id": 201, "amount": 150.0, "country": "FR", "channel": "web"},   # ❌
