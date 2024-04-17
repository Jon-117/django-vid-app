from django.test import TestCase
from django.urls import reverse

from .models import Video


# Create your tests here.

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'VidCollector app')

class TestAddVideos(TestCase):

    def test_add_video(self):
        valid_video = {
            'name': 'yoga',
            'url': 'https://www.youtube.com/watch?v=4vTJHUDB5ak',
            'notes': 'yoga for neck and shoulders'
        }

        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        # Correct template used?
        self.assertTemplateUsed('video_collection/video_list.html')

        # Video list has new vid?
        self.assertContains(response, 'yoga')
        self.assertContains(response, 'yoga for neck and shoulders')

        #  @claraj - I can't search for the link using assertContains because I've used
        #  <a> to make it prettier with "Link" for all links. Any suggestions?

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()
        self.assertEqual('yoga', video.name)
        self.assertEqual('https://www.youtube.com/watch?v=4vTJHUDB5ak', video.url)
        self.assertEqual('yoga for neck and shoulders', video.notes)
        self.assertEqual('4vTJHUDB5ak', video.video_id)

    def test_video_invalid_url_not_added(self):
        invalid_video_urls = [
            'https://www.randomsite.com/explore',
            'https://www.vidworld.com/show?query=nothing',
            'https://www.mysterydomain.com/unknown?params=404',
            'https://www.fictionalhost.com/vid?p=',
            'https://www.fantasyhub.com',
            'https://www.academiafantastica.edu',
            'https://www.minneapolis.edu/?v=xyztalk'
        ]

        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes'
            }
            url = reverse('add_video')
            response = self.client.post(reverse('add_video'), new_video, follow=True)

            self.assertTemplateUsed('video_collection/add.html')

            self.assertEqual(200, response.status_code)

            # if response.context:
            #     for message in response.context['messages']:
            #         print(message)

            messages = response.context['messages']
            #  same messages that appear when erroring in the add.html
            message_texts = [message.message for message in messages]
            print('message_texts start print')
            for message_text in message_texts:

                print(message_text)
            print('message_texts end print')

            # self.assertIn('Invalid YouTube URL', message_texts)
            self.assertIn('Invalid, check your input!', message_texts)

            video_count = Video.objects.count()
            self.assertEqual(video_count, 0)

class TestVideoList(TestCase):
    pass


class TestVideoSearch(TestCase):
    pass


class TestVideoModel(TestCase):
    pass