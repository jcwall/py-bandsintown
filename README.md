# py-bandsintown
Python wrapper for [BandsInTown 1.0 API](https://www.bandsintown.com/api/1.0/overview)
# Installation
```
git clone https://github.com/papernotes/py-bandsintown.git
python setup.py install
```
# Usage
Import and create client  
```
from bandsintown import Client
b = Client(app_id="Your APP_ID")
```  
**Please see [examples.py](https://github.com/papernotes/BandsInTownAPI/blob/master/examples.py) for usage**
# API Reference
## Class ```Client```  
Client to use BandsInTown API  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```app_id```|string         | Yes      | A description of your app |  
####```lookup_artist```  
Lookup an artist by either name or mbid. Note that the mbid (artist id) will take precedence even if artist name is found. if mbid is not found, search will use aritst_name instead.  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```artist_name```|string         | Yes      | The artist name |  
|```mbid```|  string  | No  | The MusicBrainz ID |
####```get_artist_events```  
Search for a single artist's events  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```artist_name```|string         | Yes      | The artist name |
|```mbid```|  string  | No  | The MusicBrainz ID |
|```date```|  string  | No  | The date of the event: "all", "yyyy-mm-dd", or "yyyy-mm-dd,yyyy-mm-dd" (inclusive) format |  
####```search_events```  
Search for events based on artist(s) or location  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```artists```|list         | artists or location needed| A list containing the artist(s) |
|```location```|  string  | artists or location needed  | In the format "City,State" eg. "Las Vegas, NV" |
|```radius```|  int | No  | In terms of miles. Max 150 |
|```date```| string | No | The date of the event: "all", "yyyy-mm-dd", or "yyyy-mm-dd,yyyy-mm-dd" (inclusive) format|
|```page```|  int | No  | The page number |
|```per_page```|int|No|Number of items per page|  
####```search_recommended_events```  
Search for recommended events based on artist(s) or location  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```artists```|list         | Yes | A list containing the artist(s) |
|```location```|  string  | Yes | In the format "City,State" eg. "Las Vegas, NV" |
|```radius```|  int | No  | In terms of miles. Max 150 |
|```date```| string | No | The date of the event: "all", "yyyy-mm-dd", or "yyyy-mm-dd,yyyy-mm-dd" (inclusive) format|
|```page```|  int | No  | The page number |
|```per_page```|int|No|Number of items per page|  
####```search_on_sale_soon```  
Search for events that are on sale in the next week (including today)

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```location```|  string  | No  | In the format "City,State" eg. "Las Vegas, NV" |
|```radius```|  int | No  | In terms of miles. Max 150 |
####```search_daily_events```  
Search for events that have been created, updated, or deleted in the last day  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```none```|  None  | No  | None |  
####```get_venue_events```  
Get events for a single venue based on its id  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```venue_id```|  string  | Yes  | The ID of the venue |  
####```search_venues```  
Search for event venues based on location  

| Parameter  | Type          | Required | Description |
|:----------:|:-------------:|:--------:|:-----------|
|```query```|string|Yes| Search words |
|```location```|  string  | No  | In the format "City,State" eg. "Las Vegas, NV" |
|```radius```|  int | No  | In terms of miles. Max 150 |
|```page```|  int | No  | The page number |
|```per_page```|int|No|Number of items per page|  
  
## Class ```Artist```  
Represents an Artist  

|Property|Description|
|:------|:----------|
|name| The name of the artist |
|url | The BandsInTown url for the artist |
|mbid| The MusicBrainz ID |
|upcoming_events_count| The number of upcoming events |  

## Class ```Events```  
A Generator that yields ```EventInfo``` objects

## Class ```EventInfo```  
Contains details about an event.  
```self.artists``` is a list of Artists
```self.venue``` is an Venue object  

|Property|Description|
|:------|:----------|
|id|BandsInTown event ID|
|url|The BandsInTown url for the event|
|datetime|datetime of the event expressed in ISO 8601 format with no timezone. YYYY-MM-DDThh:mm:ss|
|ticket_url|The BandsInTown url to the framed ticket seller page|
|artists_list| List of artists for the event|
|venue| Venue object that contains information about the venue|
|status| Event status (available only from daily event feed). Not always available|
|ticket_status| Tickets available/unavailable for the event|
|on_sale_datetime|On sale datetime for event tickets expressed in ISO 8601 format with no timezone, or None|  
  

## Class ```Venue```  
Contains information for an Event's Venue  

Property|Description|
|:------|:----------|
|name|Venue name|
|id|Venue id|
|city|Venue city name|
|region|Venue region|
|country|Venue country|
|url|Venue url|
|latitude|Venue latitude|
|longitude|Venue longitude|
