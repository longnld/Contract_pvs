import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.models_utils import random_string_generator
from user.models import Customer



# create secret key
@api_view(["POST"])
def create_secret_key(request):
    if request.method == "POST":
        secret_key = False
        while not secret_key:
            create_key = random_string_generator(size=50)
            secret_key = Customer.objects.filter(key=create_key).count() == 0 and create_key
        request.user.customer.key = secret_key
        request.user.customer.save()
        key_view = f'''
            <th scope="row">Key</th>
            <td>{secret_key}</td>
            <td class="text-center" id="edit_key_button"><button class="btn btn-sm btn-outline-warning"><i class="fas fa-edit"></i></button></td>
        '''
    
        return Response({"code":"00","key_view":key_view})