# BE-Scoliosis-Detection

- Base Endpoint : `https://project-example-123.herokuapp.com/`

## Login Request
+ Endpoint : ``/api/v1/auth/login``
+ HTTP Method : ``POST``
+ Request Body :

```json
{
  "password": "admin123",
  "email": "admin@gmail.com"
}
```

- Request Header :
  - Accept : `x-www-form-urlencoded`
- Response Body (Success) :

```json
{
  "error": false,
  "message": "success",
  "user": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MzgyODQ1NSwianRpIjoiZTI1ZThiYzYtYTc0Ni00N2I4LTg2MmQtODFmZWNiMDZlYWMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUzODI4NDU1LCJleHAiOjE2NTM4MjkzNTV9.ruwh8NL3l8lBDHp1ve09YsUjIT1PfdtXrbNlbt9Ie4k",
    "email": "admin@gmail.com",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MzgyODQ1NSwianRpIjoiYzZlM2ZiNTQtZDdmYy00MmExLTg2NjYtYTQ5ZTU3NGNmYTI1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjEsIm5iZiI6MTY1MzgyODQ1NSwiZXhwIjoxNjU2NDIwNDU1fQ.SYBhJI0bnBOaG9RWgyHr9zPXyrRSrQNQrTRRyLzMnPI",
    "user_id": 1
  }
}
```

- Response Body (Fail) :

```json
{
  "code": 401,
  "status": "Unauthorized",
  "error": "Wrong credentials"
}
```

## Register Request

- Endpoint : `/api/v1/auth/register`
- HTTP Method : `POST`
- Request Body :

```json
{
  "password": "admin123",
  "email": "admin@gmail.com"
}
```

- Request Header :
  - Accept : `x-www-form-urlencoded`
- Response Body (Success) :

```json
{
  "error": false,
  "message": "User succesfully created",
  "user": {
    "email": "admin@gmail.com"
  }
}
```

## Get Access Token Request

- Endpoint : `/api/v1/token/refresh`
- HTTP Method : `GET`

- Request Header :
  - Accept : `x-www-form-urlencoded`
  - Authorization : `Bearer {Refresh_Token}`
- Response Body (Success) :

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MzkxNzgzNCwianRpIjoiZDIwZGY3NmYtYTc4ZC00N2MzLWE1NjgtZmU2OTU4NjI3NDBjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUzOTE3ODM0LCJleHAiOjE2NTM5MjUwMzR9.qVG9wtuhJqu9RHQczTjX2DdLmMHpb5IaVSmebgvmfZI"
}
```

## GET Records Detection Request

- Endpoint : `/api/v1/record`
- HTTP Method : `GET`
- Request Header :
  - Accept : `x-www-form-urlencoded`
  - Authorization : `Bearer {Access_Token}`
- Response Body (Success) :

```json
{
    "data": [
        {
            "created_at": "Mon, 30 May 2022 20:37:09 GMT",
            "dateOfBirth": 12,
            "description": "Segera hubungi dokter terdekat anda",
            "detection": "Berisiko",
            "id": 2,
            "image": "https://storage.googleapis.com/scoliosis-detection/tmp/1653917929.png",
            "name": "Phoenix",
            "updated_at": null
        },
        {
            "created_at": "Mon, 30 May 2022 20:37:09 GMT",
            "dateOfBirth": 12,
            "description": "Segera hubungi dokter terdekat anda",
            "detection": "Berisiko",
            "id": 3,
            "image": "https://storage.googleapis.com/scoliosis-detection/tmp/1653919072.png",
            "name": "Phoenix",
            "updated_at": null
        }
    ]
}
```

## GET Records Details Detection Request

- Endpoint : `/api/v1/record/{id}`
- HTTP Method : `GET`
- Request Header :
  - Accept : `x-www-form-urlencoded`
  - Authorization : `Bearer {Access_Token}`
- Response Body (Success) :

```json
{
    "data": [
        {
            "created_at": "Mon, 30 May 2022 20:37:09 GMT",
            "dateOfBirth": 12,
            "description": "Segera hubungi dokter terdekat anda",
            "detection": "Berisiko",
            "id": 2,
            "image": "https://storage.googleapis.com/scoliosis-detection/tmp/1653917929.png",
            "name": "Phoenix",
            "updated_at": null
        }
    ]
}
```

## Add Records Detection Request

- Endpoint : `/api/v1/record`
- HTTP Method : `POST`

- Request Body :

```json
{
  "name": "Zico",
  "dateOfBirth": 12,
  "file": "iVBORw0KGgoAAAANSUhEUgAAAYAAAAAdCAYAAACjSLuWAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAABy8SURBVHhe7V0HfBRl3n6272aTbHoo0oJIlSJIE0EgcEgRIRRR8RP0VBQ4NOfRxAOkIxYQQhFEPOthQdEP9Y4m2A5OBARUTkFqSIAUsm12Zr7nP5tIRDzBg/Ddj3nCbJnyvv9e3pn9YbkiKUWHCRMmTJi47GAtfTdhwoQJE5cZzARgwoQJE5cp"
}
```

- Request Header :
  - Accept : `x-www-form-urlencoded`
  - Authorization : `Bearer {Access_Token}`
- Response Body (Success) :

```json
{
    "message": "Successfully Created",
    "data": [
        {
            "created_at": "Mon, 30 May 2022 20:37:09 GMT",
            "dateOfBirth": 12,
            "description": "Segera hubungi dokter terdekat anda",
            "detection": "Berisiko",
            "id": 2,
            "image": "1653917929.png",
            "name": "Phoenix",
            "updated_at": null
        },
    ]
}
```


## Delete Records Detection Request

- Endpoint : `/api/v1/record/1`
- HTTP Method : `DELETE`
- Request Header :
  - Accept : `x-www-form-urlencoded`
  - Authorization : `Bearer {Access_Token}`
- Response Body (Success) :

```json
{
    "message": "Successfully Deleted",
}
```
