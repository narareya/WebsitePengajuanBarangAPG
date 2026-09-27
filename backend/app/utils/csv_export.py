import csv
import io
from fastapi.responses import Response


def build_csv_response(filename: str, headers: list[str], rows: list[list]) -> Response:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)

    # UTF-8 BOM so Excel on Windows renders non-ASCII characters correctly
    content = "﻿" + buffer.getvalue()

    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
