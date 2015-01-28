from django.views.generic import ListView
from attendance.models import Attendance


class AttendanceList(ListView):
    model = Attendance
    template_name = "academy/attendance-list.html"
    context_object_name = "attendances"

    def get_queryset(self):
        queryset = super(AttendanceList, self).get_queryset(self, datetime)
        import datetime
        if self.request.GET.get('date'):
            date_begin = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[0], "%Y-%m-%d")
            date_end = datetime.datetime.strptime(self.request.GET.get('date').split(" - ")[1], "%Y-%m-%d")
            daterange = [date_begin, date_end]
            queryset = queryset.filter(datetime__range=daterange)
        if self.request.GET.get("q"):
            queryset = queryset.filter(profile__student__name__contains=self.request.GET.get("q"))
        if self.request.GET.get("order"):
            queryset = queryset.order_by(self.request.GET.get("order"))
        return queryset