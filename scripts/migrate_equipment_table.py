from pathlib import Path
import sys

from sqlalchemy import MetaData, Table, inspect, or_, select


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.database import engine


EQUIPMENT_COLUMNS = {
    "laboratory_id": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS laboratory_id INTEGER",
    "category": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS category VARCHAR",
    "asset_tag": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS asset_tag VARCHAR",
    "purchase_date": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS purchase_date DATE",
    "warranty_expiry": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS warranty_expiry DATE",
    "maintenance_interval_months": (
        "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS "
        "maintenance_interval_months INTEGER"
    ),
    "next_maintenance_due": (
        "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS next_maintenance_due DATE"
    ),
    "status": "ALTER TABLE equipment ADD COLUMN IF NOT EXISTS status VARCHAR",
}


def is_blank(column):
    return or_(column.is_(None), column == "")


def main():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if "equipment" not in table_names:
        raise RuntimeError("equipment table does not exist")

    if "laboratories" not in table_names:
        raise RuntimeError("laboratories table does not exist")

    with engine.begin() as connection:
        for ddl in EQUIPMENT_COLUMNS.values():
            connection.exec_driver_sql(ddl)

        metadata = MetaData()
        equipment = Table("equipment", metadata, autoload_with=connection)
        laboratories = Table("laboratories", metadata, autoload_with=connection)

        laboratory_id = connection.scalar(
            select(laboratories.c.id).order_by(laboratories.c.id).limit(1)
        )

        if laboratory_id is None:
            raise RuntimeError(
                "cannot backfill equipment.laboratory_id without a laboratory row"
            )

        connection.execute(
            equipment.update()
            .where(equipment.c.laboratory_id.is_(None))
            .values(laboratory_id=laboratory_id)
        )

        connection.execute(
            equipment.update()
            .where(is_blank(equipment.c.category))
            .values(category="general")
        )

        connection.execute(
            equipment.update()
            .where(is_blank(equipment.c.status))
            .values(status="active")
        )

        rows_missing_asset_tag = connection.execute(
            select(equipment.c.id).where(is_blank(equipment.c.asset_tag))
        ).scalars()

        for equipment_id in rows_missing_asset_tag:
            connection.execute(
                equipment.update()
                .where(equipment.c.id == equipment_id)
                .values(asset_tag=f"LEGACY-{equipment_id}")
            )

        rows_missing_serial_number = connection.execute(
            select(equipment.c.id).where(is_blank(equipment.c.serial_number))
        ).scalars()

        for equipment_id in rows_missing_serial_number:
            connection.execute(
                equipment.update()
                .where(equipment.c.id == equipment_id)
                .values(serial_number=f"LEGACY-SERIAL-{equipment_id}")
            )

        unique_columns = {
            tuple(constraint["column_names"])
            for constraint in inspect(connection).get_unique_constraints("equipment")
        }

        if ("serial_number",) not in unique_columns:
            connection.exec_driver_sql(
                "ALTER TABLE equipment ADD CONSTRAINT "
                "equipment_serial_number_key UNIQUE (serial_number)"
            )

        if ("asset_tag",) not in unique_columns:
            connection.exec_driver_sql(
                "ALTER TABLE equipment ADD CONSTRAINT "
                "equipment_asset_tag_key UNIQUE (asset_tag)"
            )

        foreign_key_columns = {
            tuple(foreign_key["constrained_columns"])
            for foreign_key in inspect(connection).get_foreign_keys("equipment")
        }

        if ("laboratory_id",) not in foreign_key_columns:
            connection.exec_driver_sql(
                "ALTER TABLE equipment ADD CONSTRAINT "
                "equipment_laboratory_id_fkey FOREIGN KEY (laboratory_id) "
                "REFERENCES laboratories (id)"
            )

        connection.exec_driver_sql(
            "ALTER TABLE equipment ALTER COLUMN laboratory_id SET NOT NULL"
        )
        connection.exec_driver_sql(
            "ALTER TABLE equipment ALTER COLUMN category SET NOT NULL"
        )
        connection.exec_driver_sql(
            "ALTER TABLE equipment ALTER COLUMN serial_number SET NOT NULL"
        )
        connection.exec_driver_sql(
            "ALTER TABLE equipment ALTER COLUMN asset_tag SET NOT NULL"
        )

    print("equipment table migrated successfully")


if __name__ == "__main__":
    main()
