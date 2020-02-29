from album import as_album, set_album
from artist import as_artist, set_artist
from log import PlexLog
from movie import as_movie, set_movie
from show import as_episode, as_show, set_episode, set_show, set_episode_cover
from utils import convert_date, create_id, request_json, update_season_summary
from urlparse import urljoin

version = "1.0.2"


# noinspection PyClassHasNoInit,PyShadowingNames
class AvalonRestTvAgent(Agent.TV_Shows):
    name = "Avalon Rest TV Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("=================== Search Start ===================")

        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "show")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        show = request_json(requestUrl, as_show(media))
        if show is None:
            return

        title = show.get("title")
        if title is None:
            PlexLog.error("Missing or invalid title: %s" % str(show))
            return

        aired = convert_date(show.get("aired"))
        year = aired.year if aired is not None else 0

        # Plex throws exception that have "/" in ID
        mid = create_id(title, year)
        result = MetadataSearchResult(id=mid,
                                      name=title,
                                      year=year,
                                      lang=lang,
                                      score=100)
        results.Append(result)
        PlexLog.debug("===================  Search end  ===================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("=================== Update Start ===================")

        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "show")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        show = request_json(requestUrl, as_show(media))
        if show is None:
            return
        set_show(metadata, media, show)

        season_summary = show.get("season_summary", {})
        for season in media.seasons:
            season_id = media.seasons[season].id
            summary = season_summary.get(season)
            if summary is not None:
                update_season_summary(season_id, summary)
            for episode in media.seasons[season].episodes:
                episode_metadata = metadata.seasons[season].episodes[episode]
                model = request_json(urljoin(server, "episode"),
                                     as_episode(media, season, episode))
                set_episode(episode_metadata, model)
                set_episode_cover(episode_metadata, media, season, episode)
        PlexLog.debug("===================  Update end  ===================")


# noinspection PyClassHasNoInit,PyShadowingNames
class AvalonRestMovieAgent(Agent.Movies):
    name = "Avalon Rest Movie Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("=================== Search Start ===================")

        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "movie")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        movie = request_json(requestUrl, as_movie(media))
        if movie is None:
            return

        title = movie.get("title")
        if title is None:
            PlexLog.error("Missing or invalid title: %s" % str(movie))
            return

        aired = convert_date(movie.get("aired"))
        year = aired.year if aired is not None else 0

        # Plex throws exception that have "/" in ID
        mid = create_id(title, year)
        result = MetadataSearchResult(id=mid,
                                      name=title,
                                      year=year,
                                      lang=lang,
                                      score=100)
        results.Append(result)
        PlexLog.debug("===================  Search end  ===================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("=================== Update Start ===================")

        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "movie")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        movie = request_json(requestUrl, as_movie(media))
        if movie is None:
            return
        set_movie(metadata, movie)

        PlexLog.debug("===================  Update end  ===================")


# noinspection PyClassHasNoInit,PyShadowingNames
class AvalonRestArtistAgent(Agent.Artist):
    name = "Avalon Rest Artist Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("=================== Search Start ===================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "artist")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        artist = request_json(requestUrl, as_artist(media))
        if artist is None:
            return

        result = MetadataSearchResult(id=media.id,
                                      name=media.title,
                                      lang=lang,
                                      year=None,
                                      score=100)

        results.Append(result)

        PlexLog.debug("===================  Search end  ===================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("=================== Update Start ===================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "artist")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        artist = request_json(requestUrl, as_artist(media))
        if artist is None:
            return

        set_artist(metadata, media, artist)

        PlexLog.debug("===================  Update end  ===================")


# noinspection PyClassHasNoInit,PyShadowingNames
class AvalonRestAlbumAgent(Agent.Album):
    name = "Avalon Rest Album Agent"
    ver = version
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = ["com.plexapp.agents.localmedia"]

    def search(self, results, media, lang, manual):
        PlexLog.debug("=================== Search Start ===================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "album")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        album = request_json(requestUrl, as_album(media))
        if album is None:
            return

        result = MetadataSearchResult(id=media.id,
                                      name=media.title,
                                      lang=lang,
                                      year=None,
                                      score=100)

        results.Append(result)

        PlexLog.debug("===================  Search end  ===================")

    def update(self, metadata, media, lang, force):
        PlexLog.debug("=================== Update Start ===================")
        PlexLog.debug("%s (%s)" % (self.name, self.ver))
        PlexLog.debug("Plex version: %s" % Platform.ServerVersion)

        server = Prefs["Server"]
        authKey = Prefs["AuthKey"]
        if not server:
            PlexLog.error("Missing server!")
            return

        requestUrl = urljoin(server, "album")
        if authKey:
            requestUrl = requestUrl + "?AuthKey=" + authKey

        PlexLog.debug("Requesting URL: %s" % requestUrl)

        album = request_json(requestUrl, as_album(media))
        if album is None:
            return

        set_album(metadata, media, album)

        PlexLog.debug("===================  Update end  ===================")
