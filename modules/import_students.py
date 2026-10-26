import sqlite3
import pandas as pd
import os

DB_PATH = "database/college_bus.db"


def import_students_from_excel(file_path):

    connection = None

    try:

        # Check Excel file
        if not os.path.exists(file_path):
            return False, "Excel file not found!"

        # Read Excel
        df = pd.read_excel(file_path)

        # Required columns
        required_columns = [
            "college_id",
            "name",
            "roll_number",
            "bus_id",
            "parent_name",
            "parent_phone"
        ]

        # Check missing columns
        missing_columns = []

        for column in required_columns:
            if column not in df.columns:
                missing_columns.append(column)

        if missing_columns:
            return False, (
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        # Connect SQLite
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        imported = 0
        skipped = 0
        errors = []

        # Process each Excel row
        for index, row in df.iterrows():

            excel_row = index + 2

            try:

                college_id = int(row["college_id"])
                name = str(row["name"]).strip()
                roll_number = str(row["roll_number"]).strip()

                bus_id = int(row["bus_id"])

                parent_name = str(
                    row["parent_name"]
                ).strip()

                parent_phone = str(
                    row["parent_phone"]
                ).strip()

                # Check empty values
                if not name:
                    errors.append(
                        f"Row {excel_row}: Name is empty"
                    )
                    continue

                if not roll_number:
                    errors.append(
                        f"Row {excel_row}: Roll number is empty"
                    )
                    continue

                # Check duplicate student
                cursor.execute("""
                    SELECT student_id
                    FROM students
                    WHERE college_id = ?
                    OR roll_number = ?
                """, (
                    college_id,
                    roll_number
                ))

                existing_student = cursor.fetchone()

                if existing_student:
                    skipped += 1
                    continue

                # Check bus exists
                cursor.execute("""
                    SELECT bus_id
                    FROM buses
                    WHERE bus_id = ?
                """, (bus_id,))

                bus_exists = cursor.fetchone()

                if not bus_exists:
                    errors.append(
                        f"Row {excel_row}: "
                        f"Bus ID {bus_id} not found"
                    )
                    continue

                # Insert student
                cursor.execute("""
                    INSERT INTO students
                    (
                        college_id,
                        name,
                        roll_number,
                        bus_id,
                        parent_name,
                        parent_phone
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    college_id,
                    name,
                    roll_number,
                    bus_id,
                    parent_name,
                    parent_phone
                ))

                imported += 1

            except ValueError:

                errors.append(
                    f"Row {excel_row}: "
                    "Invalid number format"
                )

            except sqlite3.IntegrityError as error:

                errors.append(
                    f"Row {excel_row}: {error}"
                )

        # Save changes
        connection.commit()
        connection.close()

        # Result message
        message = (
            f"{imported} students imported successfully. "
            f"{skipped} students skipped."
        )

        if errors:
            message += (
                f" {len(errors)} rows had errors."
            )

        return True, message

    except Exception as error:

        if connection:
            connection.rollback()
            connection.close()

        return False, f"Import error: {error}"


# Direct testing
if __name__ == "__main__":

    excel_file = "data/college_students_100.xlsx"

    success, message = import_students_from_excel(
        excel_file
    )

    if success:

        print("\n===================================")
        print("       EXCEL IMPORT SUCCESS")
        print("===================================")
        print(message)

    else:

        print("\n===================================")
        print("       EXCEL IMPORT FAILED")
        print("===================================")
        print(message)