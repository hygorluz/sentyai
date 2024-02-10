# :robot: Senty AI: Sentiment Analysis

Project created as part of the specialization in Fullstack Web Development to implement an Integrated Projects
applications.
The SentyAI is a sentiment analysis AI to classify messages in positive, negative or neutral.  

## Endpoints

- **/sentiments** - Generate the sentiment analysis of a message.
- **/docs** - Swagger UI.
- **/redoc** - ReDoc UI.
- **/health** - Health checker endpoint.

## Documentation

- ReDoc: http://127.0.0.1:8080/docs
- Swagger UI: http://127.0.0.1:8080/redoc
- OpenAPI Specs: http://127.0.0.1:8080/openapi.json
- Postman collection: Please import the postman request collection from the postman [folder](/postman) in the root of
  the repository.

## Sentiments types

- Positive
- Negative
- Neutral

## How to run?
Docker version (This version may take sometime to build and execute, depending on the Network):
- cd sentyai (access the project root folder)
- docker-compose build
- docker-compose up

Python directly:
- cd sentyai (access the project root folder)
- pip install -r requiriments.txt (Install dependencies)
- ./start.sh (Start gunicorn process)

Python directly alternative:
- cd sentyai (access the project root folder)
- cd service (access service folder)
- python application.py (Start unicorn process)

## Links / References

* https://huggingface.co/pysentimiento/robertuito-sentiment-analysis
* https://fastapi.tiangolo.com/
* https://gunicorn.org/#docs
* https://www.uvicorn.org/
* https://docs.pydantic.dev/latest/
* https://pymongo.readthedocs.io/en/stable/
* https://pypi.org/project/transformers/
* https://huggingface.co/
