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
        self.app_id = app_id
        self.artist_url = "http://api.bandsintown.com/artists/"
        self.search_url = "http://api.bandsintown.com/events/"
        self.venue_url = "http://api.bandsintown.com/venues/"

    def lookup_artist(self, artist_name=None, mbid=None):
        """
            Search for a single artist and artist's information
        """
        if not (artist_name or mbid):
            raise ValueError("Need 'artist_name' or 'mbid'")
        if mbid:
            mbid = "mbid_" + mbid + "?"
            response = requests.get(self.artist_url + mbid, params={"app_id": self.app_id})
        else:
            artist_name += ".json?"
            response = requests.get(self.artist_url + artist_name, params={"app_id": self.app_id})

        if response.raise_for_status():
            return response.raise_for_status()

        else:
            json = response.json()
            return Artist(json.get("name"), json.get("url"),
                          json.get("mbid"), json.get("upcoming_events_count"))

    def get_artist_events(self, artist_name=None, mbid=None, date=None):
        """
            Search for a single artist's events
        """
        get_string = ""
        if not (artist_name or mbid):
            raise ValueError("Need 'artist_name' or 'mbid'")
        if mbid:
            get_string += self.artist_url + "mbid_" + mbid + "/events?"
        else:
            get_string += self.artist_url + artist_name + "/events.json?"

        response = requests.get(get_string, params={"date=": date, "app_id": self.app_id})

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
            raise ValueError("Need at least 'artists' or 'location'")

        if len(artists) > 1:
            for item in artists:
                get_string += "artists[]=" + item + "&"
            get_string = get_string[:-1]
        else:
            get_string += "artists[]=" + artists[0] + "&"

        response = requests.get(get_string, params={"location": location, "radius": radius,
                                                    "date": date, "page": page, "per_page": per_page,
                                                    "format": "json", "app_id": self.app_id})
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
            raise ValueError("Need both 'artists' and 'location'")
        if len(artists) > 1:
            for item in artists:
                get_string += "artists[]=" + item + "&"
        else:
            get_string += "artists[]=" + artists[0]

        response = requests.get(get_string, params={"location": location, "radius": radius,
                                                    "date": date, "only_recs": only_recs,
                                                    "page": page, "per_page": per_page,
                                                    "format": "json", "app_id": self.app_id})
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)

    def search_on_sale_soon(self, location=None, radius=None):
        """
            Search for events that are on sale soon
        """
        get_string = self.search_url + "on_sale_soon?"

        response = requests.get(get_string, params={"location": location, "radius": radius,
                                                    "format": "json", "app_id": self.app_id})
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)

    def search_daily_events(self):
        """
            Search for daily events
        """
        get_string = self.search_url + "daily?"

        response = requests.get(get_string, params={"app_id": self.app_id})
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response)

    def get_venue_events(self, venue_id):
        """
            Search for events based on a venue
        """
        get_string = self.venue_url + str(venue_id) + "/events?"

        response = requests.get(get_string, params={"format": "json", "app_id": self.app_id})
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

        response = requests.get(get_string, params={"location": location, "radius": radius,
                                                    "page": page, "per_page": per_page,
                                                    "format": "json", "app_id": self.app_id})
        if response.raise_for_status():
            return response.raise_for_status()
        else:
            return Events(response, search_venue=True)


class Artist(object):
    """
        Artist class that contains information about an artist
    """

    def __init__(self, name, url, mbid, upcoming_events_count):
        self.name = name
        self.url = url
        self.mbid = mbid
        self.upcoming_events_count = upcoming_events_count


class Events(object):
    """
        Events class - generator for event information
    """

    def __init__(self, data, search_venue=None):
        self.events = data.json()
        self.search_venue = True if search_venue else False

    def __iter__(self):
        if self.search_venue:
            for item in self.events:
                yield Venue(item.get("city"), item.get("name"), item.get("latitude"),
                            item.get("region"), item.get("country"), item.get("url"),
                            item.get("id"), item.get("longitude"))
        else:
            for item in self.events:
                yield EventInfo(item.get("id"), item.get("url"), item.get("datetime"),
                                item.get("ticket_url"), item.get("artists"),
                                item.get("venue"), item.get("status"),
                                item.get("ticket_status"), item.get("on_sale_datetime"))


class EventInfo(object):
    """
        EventInfo class that contains details about an event
        self.artists is a list of artists
        self.venue is an Venue object
    """

    def __init__(self, event_id, url, datetime, ticket_url, artists, venue, status,
                 ticket_status, on_sale_datetime):
        self.id = event_id
        self.url = url
        self.datetime = datetime
        self.ticket_url = ticket_url
        self.artists_list = [Artist(artist.get("name"), artist.get("url"), artist.get("mbid"), artist.get("upcoming_events_count")) for artist in artists]
        self.venue = Venue(venue.get("city"), venue.get("name"), venue.get("latitude"),
                           venue.get("region"), venue.get("country"), venue.get("url"),
                           venue.get("event_id"), venue.get("longitude"))
        self.status = status
        self.ticket_status = ticket_status
        self.on_sale_datetime = on_sale_datetime


class Venue(object):
    """
        Contains an Event's Venue information
        'data' is a dict of values
    """

    def __init__(self, city, name, latitude, region, country, url, event_id, longitude):
        self.city = city
        self.name = name
        self.latitude = latitude
        self.region = region
        self.country = country
        self.url = url
        self.id = event_id
        self.longitude = longitude

