"""An export API with caller choices that may or may not belong in its contract."""


def export_report(report, destination, *, delimiter=",", include_header=True,
                  date_format="iso", null_text="", quote_all=False):
    rows = report.rows
    if include_header:
        rows = [report.columns, *rows]
    return destination.write_rows(
        rows,
        delimiter=delimiter,
        date_format=date_format,
        null_text=null_text,
        quote_all=quote_all,
    )
