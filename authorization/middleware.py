# from django.utils import timezone
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from authorization.models import User, Session
#
# class check_session():
#
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         if(request.path != reverse('authorization:login') and
#  request.path != reverse('authorization:registration')):
#             try:
#                 sessid = request.COOKIES.get('sessid')
#                 session = Session.objects.get(
#                     key = sessid,
#                     expires__gt = timezone.now()
#                 )
#                 request.session = session
#                 request.user = session.user
#
#             except Session.DoesNotExist:
#                 request.session = None
#                 request.user = None
#                 return HttpResponseRedirect(reverse('authorization:login'))
#
#
#         response = self.get_response(request)
#
#         return response
