from gcm import *
from Academy.models import Profile

gcm = GCM("AIzaSyC3LGruJQLdsco3ptkbDkgEJzEswwh9sQU")
name = Profile.get_name()
# datetime =

data = {'name': name, 'time':'2014/01/22 21:13'}

reg_id = 'APA91bErf2O-w00MggCY3cRzGaIxYhYc651LDjsrxUxFHh5BMUIv1ZgdiWkJvDBLA1lIWkzwLtgScJuUf2F4cIsSzxMnwUScIszSQo3XnX1pyH2mOMYkeM-VS_P_9CfXaXJD3NyKk-QB9XSsSi13NTjuLIIBcaguNz-PZn58uhOxg8f83odPy6o'

gcm.plaintext_request(registration_id=reg_id, data=data)