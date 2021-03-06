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

from datetime import datetime, timezone, timedelta

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import ProtectedError

from .models import ImageSlide, TextSlide


@receiver(pre_delete, sender=TextSlide)
@receiver(pre_delete, sender=ImageSlide)
def prevent_slide_deletion(sender, instance, using, **_):
    del sender, using
    date_send = instance.sent
    if date_send:
        date_now = datetime.now(timezone.utc)

        if (date_now - date_send) < timedelta(days=21):
            raise ProtectedError('Slides must be stored for 21 days due to legal requirements', instance)
