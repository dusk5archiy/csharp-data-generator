import json


def pascal_case_to_snake_case(name):
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def gen_code(filename):
    code_1 = []
    code_2 = set()
    code_3 = []
    with open(filename, "r") as f:
        tables = json.load(f)

    for table in tables:
        table_name = table["table_name"]
        tbl_name = table_name
        if table_name == "__EFMigrationsHistory":
            continue

        code_1.append(f'public const string {tbl_name} = "{table_name}";')
        columns = table["columns"]
        for column in columns:
            column_name = column["column_name"]
            code_2.add(f'public const string {column_name} = "{column_name}";')
            code_3.append(
                f'public const string {tbl_name}__{column_name} = "[{table_name}].[{column_name}]";'
            )

    code = (
        "static class Tbl {\n"
        + "\n".join(code_1)
        + "\n}\n"
        # + "static class Fld {\n"
        # + "\n".join(code_2)
        # + "\n}\n"
        + "static class Field {\n"
        + "\n".join(code_3)
        + "\n}\n"
    )
    return code


if __name__ == "__main__":
    code = gen_code("schema.json")
    with open("Output/Field.cs", "w") as f:
        f.write(code)

    print("Code generated successfully!")
