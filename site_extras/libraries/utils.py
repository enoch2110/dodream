# -*- coding: utf-8 -*-
import os
import random
import string
import uuid
from django.db.models.loading import get_model
from django.utils.deconstruct import deconstructible


@deconstructible
class FilenameChanger(object):

    def __init__(self, base_path):
        self.base_path = base_path

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = "%s.%s" % (uuid.uuid4(), ext)

        return os.path.join(self.base_path, filename)

    def __eq__(self, other):
        return self.base_path


def generate_random(type='char', length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))