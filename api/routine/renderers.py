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
    }
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        current_action = renderer_context['view'].action
        response_data = {
            "data": data,
            "message": self.routine_msgs.get(current_action, None)
        }
        return super().render(response_data, accepted_media_type, renderer_context)