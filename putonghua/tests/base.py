import os.path
from django.conf import settings

TEST_RESOURCES = os.path.abspath(os.path.join(settings.BASE_DIR, 'putonghua/tests/resources'))

def test_resource_file(filename):
    return os.path.join(TEST_RESOURCES, filename)

