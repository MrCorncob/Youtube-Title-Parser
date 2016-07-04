from unittest import TestCase
from youtube_title_parser.core import YoutubeTitleParser


class TestYoutubeTitleParser(TestCase):
    def test_init_parse_song(self):
        parser = YoutubeTitleParser()
        self.assertIsNotNone(parser, 'Parser is None')

    def test_parse_song(self):
        parser = YoutubeTitleParser('Kygo - Raging ft. Kodaline')
        self.assertEqual('Kygo', parser.artist_name)
        self.assertEqual('Raging ft. Kodaline', parser.song_name)

    def test_parse_song_no_artist(self):
        parser = YoutubeTitleParser('Raging ft. Kodaline')
        self.assertEqual(parser.artist_name, '')
        self.assertEqual(parser.song_name, 'Raging ft. Kodaline')

