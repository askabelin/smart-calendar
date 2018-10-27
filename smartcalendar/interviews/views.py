from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, generics, response, permissions

from .models import get_candidates_group, get_interviewers_group
from .serializers import SlotsSerializer


class AvailableSlotsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SlotsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class InterviewSlotsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        candidates_qs = User.objects.filter(groups=get_candidates_group())
        candidate = generics.get_object_or_404(candidates_qs, pk=pk)
        interviewers_qs = User.objects.filter(groups=get_interviewers_group())
        interviewers = dict(request.query_params).get('interviewers')
        if not interviewers:
            return response.Response([])
        interview_slots = candidate.slots.all()
        for interviewer_id in interviewers:
            interviewer = generics.get_object_or_404(interviewers_qs, pk=interviewer_id)
            interview_slots = interview_slots.filter(start__in=interviewer.slots.values('start'))

        serializer = SlotsSerializer(interview_slots, many=True)
        return response.Response(serializer.data)
