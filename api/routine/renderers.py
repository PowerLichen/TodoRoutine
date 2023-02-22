from rest_framework import status
from rest_framework.renderers import JSONRenderer


class RoutineJSONRenderer(JSONRenderer):
    routine_msgs = {
        "create": {
            "msg": "You have successfully created the routine.",
            "status": "ROUTINE_CREATE_OK"
        },
        "partial_update": {
            "msg": "The routine has been modified.",
            "status": "ROUTINE_UPDATE_OK"
        },
        "retrieve": {
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_DETAIL_OK"
        },
        "list": {
            "msg": "Routine lookup was successful.",
            "status": "ROUTINE_LIST_OK"
        },
        "destroy": {
            "msg": "The routine has been deleted.",
            "status": "ROUTINE_DELETE_OK"
        }
    }
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = data
        
        status_code = renderer_context["response"].status_code
        if status.is_success(status_code):
            current_action = renderer_context['view'].action
            custom_data = {
                "data": data,
                "message": self.routine_msgs.get(current_action, None)
            }
        
        return super().render(custom_data, accepted_media_type, renderer_context)
