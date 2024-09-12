# Place Suggestion API

This project aims to develop a RESTful API that uses Gemini AI to suggest places based on user prompts. The API will return detailed place information, including names, locations, and multimedia content, and will be deployed in a Docker environment on AWS.

## Features

- **AI-Powered Recommendations:** Suggest places based on user input.
- **Detailed Place Information:** Includes scraped names, prices, starts, place features, locations, and multimedia etc.

## Planned Features

- **Google Maps API Implementation**: Google Maps API will be optional for fast and more accurate results.
- **Docker Deployment:** Containerized for easy deployment.
- **AWS Integration:** Planned deployment on AWS services.

## API Reference

#### Get suggestion data

```http
  GET /api/scrape?gemini_api_key={gemini_api_key}&api_key={api_key}&query={query}&language={language}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string` | **Required** Query seach |
| `gemini_api_key` | `string` | **Required** GEMINI API key|
| `api_key` | `string` | Enter to use Google Maps API. (Planned Feature)|
| `language` | `string` | **Defalut='en'** |

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

