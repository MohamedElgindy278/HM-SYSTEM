from typing import Optional

from pyodbc import IntegrityError

from src.config.database import get_pyodbc_connection
from src.core.decorators import handle_db_errors
from src.core.exceptions import Errors
from src.core.query_utils import build_where_clause, paginate
from src.schemas.room_schema import (
    RoomCreateSchema,
    RoomResponseSchema,
    RoomStatusUpdateSchema,
    RoomUpdateSchema,
)
from src.schemas.common_schema import PaginatedResponse


class RoomService:

    @staticmethod
    def _row_to_schema(row) -> RoomResponseSchema:
        return RoomResponseSchema(
            room_id=row.room_id,
            ward_id=row.ward_id,
            room_number=row.room_number,
            room_type=row.room_type,
            status=row.status,
            floor_number=row.floor_number,
            created_at=row.created_at,
        )

    @staticmethod
    @handle_db_errors("Failed to create room")
    def create_room(room_data: RoomCreateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT ward_id FROM [Ward] WHERE ward_id = ?",
                (room_data.ward_id,),
            )
            if not cursor.fetchone():
                raise Errors.ward_not_found()

            try:
                cursor.execute(
                    """
                    INSERT INTO [Room]
                    (ward_id, room_number, room_type, status, floor_number)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        room_data.ward_id,
                        room_data.room_number,
                        room_data.room_type,
                        room_data.status,
                        room_data.floor_number,
                    ),
                )
                conn.commit()

            except IntegrityError as e:
                if "UQ_Room_WardNumber" in str(e):
                    raise Errors.room_exists()
                raise

    @staticmethod
    @handle_db_errors("Failed to update room")
    def update_room(room_id: int, room_data: RoomUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT ward_id, room_number, room_type, floor_number
                FROM [Room]
                WHERE room_id = ?
                """,
                (room_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.room_not_found()

            fields = room_data.model_dump(exclude_unset=True)

            ward_id = fields.get("ward_id", row.ward_id)
            room_number = fields.get("room_number", row.room_number)
            room_type = fields.get("room_type", row.room_type)
            floor_number = fields.get("floor_number", row.floor_number)

            if ward_id != row.ward_id:
                cursor.execute(
                    "SELECT ward_id FROM [Ward] WHERE ward_id = ?",
                    (ward_id,),
                )
                if not cursor.fetchone():
                    raise Errors.ward_not_found()

            try:
                cursor.execute(
                    """
                    UPDATE [Room]
                    SET ward_id = ?, room_number = ?, room_type = ?, floor_number = ?
                    WHERE room_id = ?
                    """,
                    (ward_id, room_number, room_type, floor_number, room_id),
                )
                conn.commit()

            except IntegrityError as e:
                if "UQ_Room_WardNumber" in str(e):
                    raise Errors.room_exists()
                raise

    @staticmethod
    @handle_db_errors("Failed to update room status")
    def update_room_status(room_id: int, status_data: RoomStatusUpdateSchema) -> None:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT room_id FROM [Room] WHERE room_id = ?", (room_id,))
            if not cursor.fetchone():
                raise Errors.room_not_found()

            cursor.execute(
                "UPDATE [Room] SET status = ? WHERE room_id = ?",
                (status_data.status, room_id),
            )
            conn.commit()

    @staticmethod
    @handle_db_errors("Failed to retrieve room")
    def get_room_by_id(room_id: int) -> RoomResponseSchema:

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT room_id, ward_id, room_number, room_type, status,
                       floor_number, created_at
                FROM [Room]
                WHERE room_id = ?
                """,
                (room_id,),
            )
            row = cursor.fetchone()

            if not row:
                raise Errors.room_not_found()

            return RoomService._row_to_schema(row)

    @staticmethod
    @handle_db_errors("Failed to retrieve rooms")
    def get_all_rooms(
        start_num: int = 1,
        page_size: int = 20,
        ward_id: Optional[int] = None,
        room_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> PaginatedResponse[RoomResponseSchema]:

        where_clause, params = build_where_clause(
            [
                ("ward_id = ?", ward_id),
                ("room_type = ?", room_type),
                ("status = ?", status),
            ]
        )

        offset, limit = paginate(start_num, page_size)

        with get_pyodbc_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT COUNT(*) AS total FROM [Room] {where_clause}", params
            )
            total = cursor.fetchone().total

            cursor.execute(
                f"""
                SELECT room_id, ward_id, room_number, room_type, status,
                       floor_number, created_at
                FROM [Room]
                {where_clause}
                ORDER BY room_number
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """,
                params + [offset, limit],
            )
            rows = cursor.fetchall()

            items = [RoomService._row_to_schema(row) for row in rows]

            return PaginatedResponse(items=items, total=total)
