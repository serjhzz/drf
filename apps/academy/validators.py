import re

from rest_framework.exceptions import ValidationError

class OnlyYouTubeUrlAllow:
    message = ''

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        description = dict(value).get(self.field)

        if description is None:
            raise ValidationError('description must be filled')

        link_pattern = r'https?://\S+|www\.\S+'
        youtube_url_pattern = r'(?:https?://)?(?:www\.)?youtube\.com'

        all_links = re.findall(link_pattern, description)
        for link in all_links:
            if not bool(re.match(youtube_url_pattern, link)):
                raise ValidationError(f'You can add only YouTube links not this {link}')