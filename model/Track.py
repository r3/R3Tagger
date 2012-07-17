"""r3tagger.model.Track

Provides models:
    Track
    Represents a music file on disc at a given path
"""

import os

import acoustid

from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3


class Track(object):
    """Path to a file and metadata that represents a track"""

    _supported_fields = ('artist', 'album', 'title',
                         'tracknumber', 'date', 'genre')

    _supported_filetypes = {'flac': FLAC, 'ogg': OggVorbis, 'mp3': EasyID3}

    def __init__(self, path, fields=None):
        """Instantiate Track object

        Requires a filepath for a song file to represent and accepts an
        optional fields parameter for specifying that song's fields. If
        such a dictionary is passed, it will be used exclusively to fill
        the field tag data of the Track instance.

        If no additional fields are specified, the Track instance's fields
        will be populated by metadata from the audio file.

        Compatible files: flac (*.flac), ogg vorbis (*.ogg)
        """

        self.path = path
        self._song_file = None
        self._connect_to_file()

        # Fill in tags if given a dict
        if fields is not None:
            for field in self.supported_fields():
                self._song_file[field] = fields.get(field, None)

    def __call__(self):
        """Shortcut to _update_file: Saves updated metadata to file."""
        self._update_file()

    def __setattr__(self, attr, val):
        if attr in self.supported_fields():
            self._song_file[attr] = val
        else:
            self.__dict__[attr] = val

    def __getattr__(self, attr):
        if attr in self.supported_fields():
            return self._song_file.get(attr, '')[0]
        else:
            result = self.__dict__.get(attr)
            if result is not None:
                return result
            else:
                raise AttributeError

    def __str__(self):
        return str(self.title)

    def _connect_to_file(self):
        """Opens a file and determines type. File will be opened
        (if compatible) with codec and metadata will be read in.
        """
        def determine_type(path):
            """Determine codec to use in opening file depending on extension"""
            extension = os.path.splitext(path)[-1][1:]
            result = self.supported_filetypes().get(extension)
            if result is None:
                error = "Extension '{}' is not supported"
                raise NotImplementedError(error.format(extension))
            else:
                return result

        song_type = determine_type(self.path)
        self._song_file = song_type(self.path)

    def _update_file(self):
        """Saves updated metadata to file."""
        self._song_file.save()

    @property
    def length(self):
        """Track length in seconds"""
        return self._song_file.info.length

    @property
    def bitrate(self):
        """Bitrate of song (eg. 160000)"""
        return self._song_file.info.bitrate

    @property
    def fingerprint(self):
        """Returns the Acoustid fingerprint"""
        _, fingerprint = acoustid.fingerprint_file(self.path)
        return fingerprint

    @classmethod
    def supported_fields(cls):
        return cls._supported_fields

    @classmethod
    def supported_filetypes(cls):
        return cls._supported_filetypes
