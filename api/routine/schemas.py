from drf_spectacular.utils import extend_schema, OpenApiExample

from api.routine.renderers import RoutineJSONRenderer

SCHEMA_ROUTINE_CREATE = extend_schema(
    summary="Routine 생성",
    examples=[
        OpenApiExample(
            name="example request",
            request_only=True,
            value={
                "title" : "problem solving",
                "category" : "HOMEWORK'",
                "goal": "Increase your problem-solving skills",
                "is_alarm": True,
                "days": ["MON", "WED", "FRI"]
            }
        ),
        OpenApiExample(
            name="example response",
            response_only=True,
            description="루틴 생성 성공",
            value={
                "data": {
                    "routine_id": 1
                },
                "message": RoutineJSONRenderer.routine_msgs["create"]
            }
        )
    ]
)

SCHEMA_ROUTINE_UPDATE = extend_schema(
    summary="Routine 수정",
    examples=[
        OpenApiExample(
            name="example request",
            request_only=True,
            value={
                "title" : "problem solving 2",
                "is_alarm": False,
                "days": ["TUE", "FRI"]
            }
        ),
        OpenApiExample(
            name="example response",
            response_only=True,
            description="루틴 수정 성공",
            value={
                "data": {
                    "routine_id": 1
                },
                "message": RoutineJSONRenderer.routine_msgs["partial_update"]
            }
        )
    ]
)
