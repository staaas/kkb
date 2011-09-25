from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeSpan3(processors.Resize):
    width = 160
    height = 160

class ResizeSpan4(processors.Resize):
    width = 220
    height = 220

class ResizeSpan5(processors.Resize):
    width = 280
    height = 280

class Span3(ImageSpec):
    quality = 75  # defaults to 70
    access_as = 'poster_span3'
    pre_cache = True
    processors = [ResizeSpan3]

class Span4(ImageSpec):
    quality = 75  # defaults to 70
    access_as = 'poster_span4'
    pre_cache = True
    processors = [ResizeSpan4]

class Span5(ImageSpec):
    quality = 75  # defaults to 70
    access_as = 'poster_span5'
    pre_cache = True
    processors = [ResizeSpan5]
