from site_extras.models.sitemodels import Popup
import datetime


def popups(request):
    today = datetime.date.today()
    if request.session.get('popup-%s' % today):
        popups = Popup.objects.none()
    else:
        popups = Popup.objects.filter(date_begin__lte=today, date_end__gte=today, is_active=True)
    return {'popups': popups}
