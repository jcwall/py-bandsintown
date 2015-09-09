"""
    Unofficial Python API Wrapper for BandsInTown API
    https://github.com/papernotes
"""
import requests

class Client(object):
    """
        Class object to use BandsInTown API
    """

    def __init__(self, app_id):
        self.app_id = "app_id=" + app_id
        self.artist_url = "http://api.bandsintown.com/artists/"
        self.search_url = "http://api.bandsintown.com/events/"
        self.venue_url = "http://api.bandsintown.com/venues/"


    def lookup_artist(self, artist_name=None, mbid=None):
        """
            Search for a single artist and artist's information
        """
        if not (artist_name or mbid):
            return "Need 'artist_name' or 'mbid'"
        if mbid:
            mbid = "mbid_" + mbid + "?"

            response = requests.get(self.artist_url + mbid + self.app_id)
            if response.raise_for_status():
                return response.raise_for_status()
            return Artist(response)
        else:
            artist_name += ".json?"

            response = requests.get(self.artist_url + artist_name + self.app_id)
            if response.raise_for_status():
                return response.raise_for_status()
            else:
                return Artist(response)


    def get_artist_events(self, artist_name=None, mbid=None, date=None):
        """
            Search for a single artist's events
        """
        get_string = ""
        if not (artist_name or mbid):
            return "Need 'artist_name' or 'mbid'"
        if mbid:
            get_string += self.artist_url + "mbid_" + mbid + "/events?" + self.app_id
        else:
            get_string += self.artist_url + artist_name + "/events.json?" + self.app_id

        if date:
            get_string += "&date=" + date

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def search_events(self, artists=None, location=None, radius=None,
                      date=None, page=None, per_page=None):
        """
            Search for events based on artist(s) or location
        """
        get_string = "" + self.search_url + "search?"
        if not (artists or location):
            return "Need at least 'artists' or 'location'"
        if len(artists) > 1:
            for item in artists:
                get_string += "artists[]=" + item + "&"
        else:
            get_string += "artists[]=" + artists[0] + "&"

        if location:
            get_string += "&location=" + location
        if radius:
            get_string += "&radius=" + str(radius)
        if date:
            get_string += "&date=" + date
        if page:
            get_string += "&page=" + str(page)
        if per_page:
            get_string += "&per_page=" + str(per_page)

        get_string += "format=json&" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def search_recommended_events(self, artists=None, location=None, radius=None,
                                  date=None, only_recs=None, page=None,
                                  per_page=None):
        """
            Search for recommended events based on artist(s) or location
        """
        get_string = "" + self.search_url + "recommended?"
        if not (artists and location):
            return "Need both 'artists' and 'location'"
        if len(artists) > 1:
            for item in artists:
                get_string += "artists[]=" + item + "&"
        else:
            get_string += "artists[]=" + artists[0]

        if location:
            get_string += "&location=" + location
        if radius:
            get_string += "&radius=" + str(radius)
        if date:
            get_string += "&date=" + date
        if only_recs:
            get_string += "&only_recs" + only_recs
        if page:
            get_string += "&page=" + str(page)
        if per_page:
            get_string += "&per_page=" + str(per_page)
        get_string += "format=json&" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def search_on_sale_soon(self, location=None, radius=None):
        """
            Search for events that are on sale soon
        """
        get_string = self.search_url + "on_sale_soon?"
        if location:
            get_string += "&location=" + location
        if radius:
            get_string += "&radius=" + str(radius)

        get_string += "format=json&" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def search_daily_events(self):
        """
            Search for daily events
        """
        get_string = self.search_url + "daily?" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def get_venue_events(self, venue_id):
        """
            Search for events based on a venue
        """
        get_string = self.venue_url + str(venue_id) + "/events?&format=json&" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)


    def search_venues(self, query, location=None, radius=None,
                      page=None, per_page=None):
        """
            Search for events based on location
        """
        get_string = self.venue_url + "search?query="
        for word in query.split():
            get_string += word + "+"
        get_string = get_string[:-1]
        if location:
            get_string += "&location=" + location
        if radius:
            get_string += "&radius=" + radius
        if page:
            get_string += "&page=" + page
        if per_page:
            get_string += "&per_page" + per_page
        get_string += "&format=json&" + self.app_id

        response = requests.get(get_string)
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response, search_venue=True)


class Artist(object):
    """
        Artist class that contains information about an artist
    """

    def __init__(self, data):
        self.name = data.json()['name']
        self.url = data.json()['url']
        self.mbid = data.json()['mbid']
        self.upcoming_events_count = data.json()['upcoming_events_count']


class Events(object):
    """
        Events class - generator for event information
    """

    def __init__(self, data, search_venue=None):
        self.events = data.json()
        if search_venue:
            self.search_venue = True
        else:
            self.search_venue = None

    def __iter__(self):
        if self.search_venue:
            for item in self.events:
                yield EventInfoVenue(item)
        else:
            for item in self.events:
                yield EventInfo(item)


class EventInfo(object):
    """
        EventInfo class that contains details about an event
        self.artists is an EventInfoArtists object
        self.venue is an EventInfoVenue object
    """

    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']

        if 'datetime' in data:
            self.datetime = data['datetime']
        else:
            self.datetime = None

        if 'ticket_url' in data:
            self.ticket_url = data['ticket_url']
        else:
            self.ticket_url = None

        if 'artists' in data:
            self.artists = EventInfoArtists(data['artists'])
        else:
            self.artists = None

        if 'venue' in data:
            self.venue = EventInfoVenue(data['venue'])
        else:
            self.venue = None

        if 'status' in data:
            self.status = data['status']
        else:
            self.status = None

        if 'ticket_status' in data:
            self.ticket_status = data['ticket_status']
        else:
            self.ticket_status = None

        if 'on_sale_datetime' in data:
            self.on_sale_datetime = data['on_sale_datetime']
        else:
            self.on_sale_datetime = None


class EventInfoArtists(object):
    """
        EventInfoArtists class that contains information for an events artists.
        The values in this object are lists
    """

    def __init__(self, data):
        self.artist_names = []
        self.artist_mbids = []
        self.artist_urls = []

        for artist in data:
            self.artist_names.append(artist['name'])
            self.artist_mbids.append(artist['mbid'])
            self.artist_urls.append(artist['url'])


class EventInfoVenue(object):
    """
        Contains an Event's Venue information
    """

    def __init__(self, data):
        self.city = data['city']
        self.name = data['name']
        self.latitude = data['latitude']
        self.region = data['region']
        self.country = data['country']
        self.url = data['url']
        self.id = data['id']
        self.longitude = data['longitude']
