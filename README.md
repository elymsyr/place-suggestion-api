# Place Suggestion API

This project aims to develop a RESTful API that uses Gemini AI to suggest places based on user prompts. The API will return detailed place information, including names, locations, and multimedia content, and will be deployed in a Docker environment on AWS.

## Features

- **AI-Powered Recommendations:** Suggest places based on user input.
- **Docker Deployment:** Containerized for easy deployment.
- **Detailed Place Information:** Includes scraped names, prices, starts, place features, locations, and multimedia etc.

## Planned Features

- **Google Maps API Implementation**: Google Maps API will be optional for fast and more accurate results.
- **Cloud Deployment:** Planned deployment on services such as AWS. (This feature has been postponed to a later date due to financial reasons.)

## Usage

**Pull and run from Docker Hub:**

```
    docker pull elymsyr/place-suggestion-api-demo
    docker run -d -p 8000:8000 elymsyr/place-suggestion-api-demo
```
Open `http://0.0.0.0:8000/scrap/?query=I%20need%20some%20quiet%20places%20to%20spend%20time%20in%20Amsterdam&gemini_api_key={YOUR_API_KEY}&language=en&max_worker={MAX_WORKER_NUMBER}` to test container. Estimated response time is ~15 seconds.

## API Reference

#### Get suggestion data

See, [API](API).

```
  GET /scrape
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string` | **Required** Query seach |
| `gemini_api_key` | `string` | **Required** GEMINI API key [Get your key here](https://aistudio.google.com/app/apikey)|
| `maps_api_key` | `string` | Enter to use Google Maps API. (Planned Feature)|
| `language` | `string` | **Defalut = str: 'en'** |
| `max_worker` | `string` | **Defalut = int: 1** |

## Usage/Examples

**Results with the Query `I need some quiet places in Amsterdam to spend time` :**

```
Hortus Botanicus: 
    {
        "url": "https://www.google.com/maps/place/Hortus+Botanicus/@52.3669189,4.907623,17z/dat...",
        "place_name": "Hortus Botanicus",
        "place_type": "Botanical garden",
        "price": "$$",
        "coordinate": [52.3669189, 4.907623],
        ...
    }
Vondelpark: 
    {
        "url": "https://www.google.com/maps/place/Vondelpark/@52.3579946,4.8686484,17z/dat..",
        "place_name": "Vondelpark",
        "place_type": "Park",
        "price": "$$",
        "coordinate": [52.3579946, 4.8686484],
        ...
    }
    ...
```
## Optimizations

**Fast response with asynchronous processing :** API scraps data as the Gemini produces response. Also, data scraping is proccessed asynchronously.

## Running Tests

Tests will be updated.

## Contributing

Contributions are welcome! Please check back for development and contributing guidelines and adhere to this project's `code of conduct`.

# License

GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE.md) file for details.
## Authors

- [@elymsyr](https://www.github.com/elymsyr)

