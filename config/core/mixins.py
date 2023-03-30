from django.http import JsonResponse

class Loginrequired():
    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(request,*args,**kwargs)
        else:
            return JsonResponse({"error":"login require"})
        