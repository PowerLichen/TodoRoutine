from drf_spectacular.utils import extend_schema, OpenApiExample

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
                "message": {
                    "msg": "You have successfully created the routine.",
                    "status": "ROUTINE_CREATE_OK"
                }
            }
        )
    ]
)
