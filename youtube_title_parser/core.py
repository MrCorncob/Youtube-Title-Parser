import re


class YoutubeTitleParser(object):
    song_name = None
    artist_name = None

    def __init__(self, title=None):
        self.song_name = ''
        self.artist_name = ''
        from .helpers import separators
        self.separators = separators
        if title:
            self.split_artist_title(title)

    def parse_song(self, title=None):
        parts = title.split('-', 1)
        if len(parts) > 1:
            self.artist_name = parts[0]
            self.song_name = parts[1]
        else:
            self.song_name = parts[0]
            self.artist_name = ''

    @staticmethod
    def _clean_fluff(string):
        result = re.sub(r'/\s*\[[^\]]+\]$/', '', string=string)  # [whatever] at the end
        result = re.sub(r'/^\s*\[[^\]]+\]\s*/', '', string=result)  # [whatever] at the start
        result = re.sub(r'/\s*\[\s*(M/?V)\s*\]/', '', string=result)  # [MV] or [M/V]
        result = re.sub(r'/\s*\(\s*(M/?V)\s*\)/', '', string=result)  # (MV) or (M/V)
        result = re.sub(r'/[\s\-–_]+(M/?V)\s*/', '', string=result)  # MV or M/V at the end
        result = re.sub(r'/(M/?V)[\s\-–_]+/', '', string=result)  # MV or M/V at the start
        result = re.sub(r'/\s*\([^\)]*\bver(\.|sion)?\s*\)$/i', '', string=result)  # (whatever version)
        result = re.sub(r'/\s*[a-z]*\s*\bver(\.|sion)?$/i', '', string=result)  # ver. and 1 word before (no parens)
        result = re.sub(r'/\s*(of+icial\s*)?(music\s*)?video/i', '', string=result)  # (official)? (music)? video
        result = re.sub(r'/\s*(ALBUM TRACK\s*)?(album track\s*)/i', '', string=result)  # (ALBUM TRACK)
        result = re.sub(r'/\s*\(\s*of+icial\s*\)/i', '', string=result)  # (official)
        result = re.sub(r'/\s*\(\s*[0-9]{4}\s*\)/i', '', string=result)  # (1999)
        result = re.sub(r'/\s+\(\s*(HD|HQ)\s*\)$/', '', string=result)  # HD (HQ)
        result = re.sub(r'/[\s\-–_]+(HD|HQ)\s*$/', '', string=result)  # HD (HQ)

        return result

    @staticmethod
    def _clean_title(title):
        result = re.sub('/\s*\*+\s?\S+\s?\*+$/', '', title)
        result = re.sub('/\s*video\s*clip/i', '', result)  # **NEW**
        result = re.sub('/\s*video\s*clip/i', '', result)  # video clip
        result = re.sub('/\s+\(?live\)?$/i', '', result)  # live
        result = re.sub('/\(\s*\)/', '', result)  # Leftovers after e.g. (official video)
        result = re.sub('/^(|.*\s)"(.*)"(\s.*|)$/', '$2', result)  # Artist - The new "Track title" featuring someone
        result = re.sub('/^(|.*\s)\'(.*)\'(\s.*|)$/', '$2', result)  # 'Track title'
        result = re.sub('/^[/\s,:;~\-–_\s"]+/', '', result)  # trim starting white chars and dash
        result = re.sub('/[/\s,:;~\-–_\s"]+$/', '', result)  # trim trailing white chars and dash
        return result

    @staticmethod
    def _clean_artist(artist):
        result = re.sub('/\s*[0-1][0-9][0-1][0-9][0-3][0-9]\s*/', '', artist)  # date formats ex. 130624
        result = re.sub('/^[/\s,:;~\-–_\s"]+/', '', result)  # trim starting white chars and dash
        result = re.sub('/[/\s,:;~\-–_\s"]+$/', '', result)  # trim starting white chars and dash

        return result

    def split_artist_title(self, title):
        parts = None
        for separator in self.separators:
            if separator in title:
                parts = title.split('{}'.format(separator), 1)
                break

        if parts:
            self.song_name = self._clean_title(parts[1])
            self.artist_name = self._clean_artist(parts[0])
        else:
            self.song_name = title
            self.artist_name = ''
