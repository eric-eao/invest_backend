from io import BytesIO
from fastapi import Response
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta

def export_table_excel(db: Session, model: DeclarativeMeta, filename: str) -> Response:
    query = db.query(model)
    df = pd.read_sql(query.statement, db.bind)

    # remover timezone de todos campos datetime
    for col in df.select_dtypes(include=["datetime64[ns, UTC]"]).columns:
        df[col] = df[col].dt.tz_localize(None)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Export", index=False)

    headers = {
        "Content-Disposition": f'attachment; filename=\"{filename}.xlsx\"'
    }
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )