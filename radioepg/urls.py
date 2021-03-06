# Copyright 2021 Radio Moreeni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.urls import path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'bearers', views.BearerViewSet)

urlpatterns = [
    path('radiodns/spi/3.1/SI.xml', views.service_information, name='service_information'),
]
