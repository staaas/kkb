from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeSpan3(processors.Resize):
    width = 160
    height = 160

class Span3(ImageSpec):
    quality = 75  # defaults to 70
    access_as = 'logo_span3'
    pre_cache = True
    processors = [ResizeSpan3]
