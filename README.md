# Mappy - Google Maps Navigation for Alfred

This Alfred Workflow makes it easy to quickly access the Google Maps Navigation.
It either works with a simple address search or by combining `from` & `to` based on your pre-defined home or work address.

https://github.com/adrianbartnik/AlfredGoogleMapsNavigationWorkflow/assets/3998715/abfaa653-c147-43f7-b9e0-720867aa3288

## Usage

You can use the `mappy` keyword to invoke this workflow from Alfred.
It provides two main features: quick access based on your current location or based on pre-configured home/work addresses.
In addition, a default transportation mode can be set or set per search.

### Default Address Search based on your current location

```shell
mappy <your address query>
```

This opens the default Google Navigation with the address query as destination and your location as origin.

### Navigation to / from your home / work address

```shell
mappy [to|from] [home|work] <your address query>
```

This opens the default Google Navigation with the home/work address and the address query as origin/destination respectively.
The home and work address need to be configured, see below.

### Transportation mode

You can configure a default transportation mode (car, walking, bike, public transport) for each search.
In addition, you can also configure the transportation per search by appending it to the commands above, e.g.:

```shell
mappy <your address query> car
mappy to home <your address query> walking
```

A description of the different transportation modes can be found in the [Google Documentation](https://developers.google.com/maps/documentation/urls/get-started).
The latest list of valid transportation modes can be looked up in [lines 24 of the `google-maps.py` file](google-maps.py).

| Transportation Mode | Description                            | Alternative Keys                  |
| ------------------- | -------------------------------------- | --------------------------------- |
| driving             | Car transportation                     | `["car", "drive", "driving"]`     |
| bicycling           | Bike travel                            | `["bike", "cycle", "bicycling"]`  |
| transit             | Public Transport                       | `["public", "transit", "train"]`  |
| walking             | Walking                                | `["walk", "walking"]`             |
| default             | Automatically choosing the best option | `["default", "best", "adaptive"]` |


## Configuration

During installation and in the workflow configuration, you have the possibility to set:

* Your home address
* Your work address
* Your default mode of transportation
* The default Google domain

## Development

This project is built with Python 3.9 and Poetry.
To get started, run `poetry install`.

### Linting

We use `flake8` and `black` to lint our code.
Run the following to lint the code:

```shell
poetry run pflake8 .
poetry run black .
```
