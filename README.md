## PyXIE
### About
A lightweight [Tracking Pixel](https://en.wikipedia.org/wiki/Tracking_Pixel?wprov=srpw1_0) service written in Python.

## Installation
### Quickstart using Docker
#### Pull the image from Dockerhub
```bash
user@shell> docker pull devdull/pyxie:latest
latest: Pulling from devdull/pyxie

> snip <

Status: Downloaded newer image for devdull/pyxie:latest
docker.io/devdull/pyxie:latest
```

#### Create a directory to store PyXIE's data
```bash
user@shell> mkdir data
```

#### Create your configuration file
When running PyXIE as a Docker image, it is recommended to set the `DATABASE_FILE` value in `config.yaml` to ensure that data is persisted between container restarts. Below is a minimal example.

`config.yaml`:
```yaml
DATABASE_FILE: /app/data/uadb.json
API_KEYS:
  - your-api-key-here
  - a-different-api-key-here
  - Another API key with spaces and a comma, but this might be hard to use later.
```

#### Run the image, mounting the data path and configuration file:
```bash
user@shell> docker run -d --mount type=bind,src="./config.yaml",dst="/app/config.yaml" --mount type=bind,src="./data",dst="/app/data" -p 5000:5000 devdull/pyxie:latest
```

#### Test the instance
```bash
user@shell> curl -X POST -H 'X-Api-Key: your-api-key-here' -d 'id=foo' 'http://localhost:5000/register'
Success
user@shell> ls -l data/  # Confirm the data file exists in the bound directory
total 8
-rw-r--r--  1 user  staff  2043 Jul  8 11:57 uadb.json
```

#### Stuff the average user can ignore
The service inside the container is run using Gunicorn. To configure the bind IP and port, you can set the environment variables `LISTEN_IP` and `LISTEN_PORT`. These should not be confused for the configuration items used by Flask which can be defined in `config.yaml`.

### Manual install using Flask (or Gunicorn)
#### Install the app requirements
```bash
user@shell> python3 -m venv .venv
user@shell> source .venv/bin/activate
user@shell> pip3 install -r requirements.txt
```

You should now be able to start PyXIE using Flask with the command `python3 pyxie.py` (listens on `127.0.0.1:5000`) or `gunicorn pyxie:pyxie` (listens on to `0.0.0.0:8000`)

## Usage
### Configuration
Below is a minimal configuration file which lists out API keys. These keys should be long and difficult to guess.

`config.yaml`:
```yaml
API_KEYS:
  - your-api-key-here
  - a-different-api-key-here
  - Another API key with spaces and a comma, but this might be hard to use later.
```

Below is a complete list of user configurable settings:
|Configuration item|Default value|Details|
|---|---|---|
|`LISTEN_IP`|`127.0.0.1`|The IP address to listen on when running with Flask (omit for Docker, Gunicorn)|
|`LISTEN_PORT`|`5000`|The port number to listen on when running with Flask (omit for Docker, Gunicorn)|
|`API_KEYS`|`[]` (empty list)|A list of API keys that should be considered valid by PyXIE|
|`LOG_LEVEL`|`WARNING`|The logging level. Valid values are, `CRITICAL`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`|
|`DATABASE_FILE`|`uadb.json`|The file that stores all pixel tracking data|
|`RRD_MAX_SIZE`|`10000`|Planned to be deprecated! The maximum number of records to keep for each `id`|

### Register a new `id`
The purpose of an `id` is to enable the user to differentiate between the various places a tracking pixel has been embedded. For example, you would want a different `id` for tracking if a user saw an email versus tracking embedded into a specific webpage.

Make a `POST` request to the `/register` endpoint which specifies your new `id` as a parameter using an API key specified in your configuration as the value for a `X-Api-Key` header. If successful, you should get a "Success" message and a status code of `201`.

Here is an example that registers an `id` of `testing` for the service when it is running locally:
```bash
user@shell> curl -Ss -X POST -H 'X-Api-Key: your-api-key-here' -d 'id=testing' 'http://127.0.0.1:5000/register'
Success
```

If no `Success` message appears, nothing was registered. Double check your API key, your URL, and your port number.

Using your registered `id` as a `GET` parameter, you should now be able to navigate to the tracking pixel in your browser. For the `id` of `testing` like in the above call, the URL to the tracking pixel would be `http://127.0.0.1:5000/?id=testing`. Any unregistered IDs will result in a "Not Found" message and a `404` status code.

### Embed your tracking pixel
How you embed your pixel will depend on the document format, but here's an example for an HTML page:
```html
<img src="http://127.0.0.1:5000/?id=testing" width="1" height="1" />
```

Because the image is a transparent PNG a single pixel in size, it is unlikely to significantly interfere with the formatting of any website, but placing it at the bottom of a page should minimize any potential formatting issues. Specifying the width and height (like in the example or using CSS) should mitigate the likelihood of a broken image icon on your page should PyXIE go offline, or the `id` to be unregistered.

### View or collect stats
Statistics are only viewable to individuals who have a valid API key, and can be accessed using the `/stats` endpoint. When successful, you should get valid JSON back as well as a status code of `200`.

for example:
```bash
user@shell> curl -Ss -H 'X-Api-Key: your-api-key-here' 'http://127.0.0.1:5000/stats' | jq
{
  "browser_family_counts": {
    "foo": {
      "192.168.1.99": {
        "Firefox": 1,
        "curl": 1
      }
    },
    "testing": {
      "127.0.0.1": {
        "Firefox": 3
      }
    }
  },
  "os_family_counts": {
    "foo": {
      "192.168.1.99": {
        "Mac OS X": 1,
        "Unknown": 1
      }
    },
    "testing": {
      "127.0.0.1": {
        "Mac OS X": 3
      }
    }
  },
  "referrer_counts": {
    "foo": {
      "192.168.1.99": {
        "Unknown": 2
      }
    },
    "testing": {
      "127.0.0.1": {
        "Unknown": 3
      }
    }
  }
}
```

The data is structured in the following format (examples are from the first block in the above):
- Name of the data (e.g. `browser_family_counts`)
  - an `id` you registered (e.g. `foo`)
    - The IP address of the individual who viewed the tracking pixel (e.g. `192.168.1.99`)
      - The value of the viewer data and the number of times that value has been seen (`Firefox` has been seen `1` time and `curl` has been seen `1` time)

To put all of that together: One or more user at the IP address `192.168.1.99` saw a tracking pixel with an `id` of `foo`. Once with a "browser family" of `Firefox`, and another with `curl`.

### Unregister an `id`
Note that unregistering an ID is destructive and all data for that `id` will be lost. If you wish to retain the data, make a copy of your datafile (e.g. `uadb.json`) first. If successful, you should get a "Success" message and a status code of `204`.

```bash
user@shell> curl -Ss -X DELETE -H 'X-Api-Key: your-api-key-here' 'http://127.0.0.1:5000/unregister?id=testing'
Success
```

### Cleanly shutting down PyXIE
If PyXIE is killed while in the middle of persisting data to disk, it will likely result in a corrupted file. To ensure that your data is complete and well formed, use one of your defined API keys ot send a `POST` request to the `/shutdown` endpoint like in the following example. This will tell PyXIE to write all data to disk and exit.

```bash
user@shell>  curl -Ss -X POST -H 'X-Api-Key: your-api-key-here' 'http://127.0.0.1:5000/shutdown'
curl: (52) Empty reply from server
```
