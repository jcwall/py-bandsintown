"""
    A series of examples for using the bandsintown api wrapper
"""
from bandsintown import Client

# create the client
b = Client(app_id="Your APP_ID")


# lookup an artist by name
artist = b.lookup_artist(artist_name="Skrillex")
print artist.url

    # http://www.bandsintown.com/Skrillex


# lookup artist by mbid
artist = b.lookup_artist(mbid="65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
print artist.name 

    # Metallica


# lookup single artist's events by name
events = b.get_artist_events(artist_name="Skrillex")
for event in events:
    print event.venue.name.encode('utf-8')

    # Dog Blood @ Lollapalooza Berlin
    # Bestival
    # RTU Ultra
    # Ultra Music Festival


# lookup single artist's events by mbid
events = b.get_artist_events(mbid="65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
for event in events:
    print event.venue.name.encode('utf-8')

    # Centre Videotron
    # Parque dos atletas


# lookup single artist's events with date range
events = b.get_artist_events(artist_name="Skrillex", date="2012-09-01,2012-12-01")
for event in events:
    print event.venue.name.encode('utf-8')

    # Benjamin Franklin Parkway
    # Electric Zoo
    # Bumbershoot Festival


# search for events based on artists, location, and radius
events = b.search_events(artists=["Skrillex", "Diplo"], location="Las Vegas,NV", radius=5)
for event in events:
    print event.venue.name.encode('utf-8')

    # XS
    # XS


# search for recommended events based on artists and location
events = b.search_recommended_events(artists=["Skrillex", "Diplo"], location="Las Vegas, NV")
for event in events:
    print event.venue.name.encode('utf-8')

    # Encore Beach Club @ Night
    # Surrender Nightclub
    # 400 N. 7th Street


# search for events that are on sale soon
events = b.search_on_sale_soon()
for event in events:
    print event.venue.name.encode('utf-8')

    # River Run ATV Park
    # Toad's Place of New Haven
    # Avalanche Vs Ducks


# search for events that are on sale soon based on location
events = b.search_on_sale_soon(location="Boston,MA")
for event in events:
    print event.venue.name.encode('utf-8')

    # Somerville Theatre
    # House of Blues
    # Glabicky Field


# search for daily events
events = b.search_daily_events()
for event in events:
    print event.venue.name.encode('utf-8')

    # Shooting Bull
    # Secret Show @ Bandung
    # Azul Beach


# search for events based on venue id
events = b.get_venue_events(venue_id=1700)
for event in events:
    print event.on_sale_datetime

    # 2015-05-08T12:00:00
    # 2015-05-29T12:00:00
    # 2015-08-07T12:00:00


# search for events based on location
events = b.search_venues(query="House of Blues")
for event in events:
    print event.region

    # TX
    # CA
    # LA
