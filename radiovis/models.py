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

from django.db import models
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor


class Image(models.Model):
    image = fields.ImageField(upload_to='images/', dependencies=[
        FileDependency(attname='image600', processor=ImageProcessor(
            format='PNG', scale={'width': 600, 'height': 600, 'preserve': False})),
        FileDependency(attname='image320', processor=ImageProcessor(
            format='PNG', scale={'width': 320, 'height': 240, 'preserve': False})),
        FileDependency(attname='image128', processor=ImageProcessor(
            format='PNG', scale={'width': 128, 'height': 128, 'preserve': False})),
        FileDependency(attname='image112', processor=ImageProcessor(
            format='PNG', scale={'width': 112, 'height': 32, 'preserve': False})),
        FileDependency(attname='image32', processor=ImageProcessor(
            format='PNG', scale={'width': 32, 'height': 32, 'preserve': False})),
    ])
    image600 = models.ImageField(upload_to='autoscaled/')
    image320 = models.ImageField(upload_to='autoscaled/')
    image128 = models.ImageField(upload_to='autoscaled/')
    image112 = models.ImageField(upload_to='autoscaled/')
    image32 = models.ImageField(upload_to='autoscaled/')

    def __str__(self):
        return f'{self.image}'


class ImageSlide(models.Model):
    trigger_time = models.DateTimeField(null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    link = models.CharField(max_length=512, blank=True)
    sent = models.DateTimeField(null=True, editable=False)


class TextSlide(models.Model):
    message = models.CharField(max_length=128, default='')
    sent = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return f'"{self.message}", {self.sent}'
