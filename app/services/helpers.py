from werkzeug.datastructures import FileStorage


def extract_batch_file_data(file: FileStorage):
    file_content = file.stream.read().decode()
    file_rows = file_content.split("\n")
    header: str = file_rows[0]
    footer: str = file_rows[-1]
    data_rows = list(filter(lambda e: e[0] == "C", file_rows))
    batch_name = header[0:28].strip()
    date = header[29:37]
    header_batch_number = header[37:45]
    header_rows_number = int(header[45:51])
    footer_batch_number = footer[0:8]
    footer_rows_number = int(footer[8:14])

    data_rows_data = []
    for row in data_rows:
        num_in_batch = int(row[1:7].strip())
        card_number = row[7:25].strip()
        data_rows_data.append(
            {"num_in_batch": num_in_batch, "card_number": card_number}
        )

    if (footer_rows_number == header_rows_number == len(data_rows))\
    and (header_batch_number == footer_batch_number):
        return {
            "header": {
                "batch_name": batch_name,
                "batch_number": header_batch_number,
                "batch_date": date

            },
            "content": data_rows_data
        }
    else:
        return None
