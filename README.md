Сгенерировать спецификацию:
python -m aiohttp_pydantic.oas server.main:app -f json -o openapi.json

Создать клиент:
openapi-python-generator openapi.json ./testclient