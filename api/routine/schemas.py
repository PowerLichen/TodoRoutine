from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiResponse

from api.routine.renderers import RoutineJSONRenderer
from api.routine.serializers import RoutineDestroySerializer

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

SCHEMA_ROUTINE_RETRIEVE = extend_schema(
    summary="Routine 단건 조회",
    examples=[
        OpenApiExample(
            name="example response",
            response_only=True,
            description="루틴 단건 조회 성공",
            value={
                "data": {
                    "goal" : "Solve 2 pages of math problems every day",
                    "id" : 1,
                    "result" : "NOT",
                    "title" : "solve math problems",
                    "days": ["MON", "WED", "FRI"]
                },
                "message": RoutineJSONRenderer.routine_msgs["retrieve"]
            }
        )
    ]
)

SCHEMA_ROUTINE_LIST = extend_schema(
    summary="Routine 목록 조회",
    examples=[
        OpenApiExample(
            name="example request",
            request_only=True,
            value={
                "today" : "2022-02-14"
            }
        ),
        OpenApiExample(
            name="example response",
            response_only=True,
            description="루틴 목록 조회 성공",
            value={
                "data":  [{
                    "goal" : "Solve 2 pages of math problems every day",
                    "id" : 1,
                    "result" : "NOT",
                    "title" : "solve math problems"
                    },
                    {
                    "goal" : "Solve 2 pages of english problems every day",
                    "id" : 1,
                    "result" : "DONE",
                    "title": "solve english problems"
                }],
                "message": RoutineJSONRenderer.routine_msgs["list"]
            }
        )
    ]
)

SCHEMA_ROUTINE_DESTROY = extend_schema(
    summary="Routine 삭제",
    responses={200: OpenApiResponse(response=RoutineDestroySerializer)},
    examples=[
        OpenApiExample(
            name="example response",
            response_only=True,
            description="루틴 삭제 성공",
            value={
                "data": {
                    "routine_id": 1
                },
                "message": RoutineJSONRenderer.routine_msgs["destroy"]
            }
        )
    ]
)