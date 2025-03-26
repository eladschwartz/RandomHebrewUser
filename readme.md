# Random Hebrew User Generator API

A FastAPI-based asynchronous API that generates random user data with support for gender filtering and seed-based regeneration. The API provides consistent user data when using the same seed value, making it perfect for testing and development scenarios.

## Features

- Asynchronous database operations
- Gender-based filtering
- Seed-based user regeneration
- Comprehensive user data including:
  - Personal information (name, gender)
  - Contact details (phone)
  - Location data (street, city, coordinates)
  - Date of birth and age

## API Endpoints

### Generate Random User


#### Query Parameters

| Parameter | Type     | Description                                                           |
| :-------- | :------- | :------------------------------------------------------------------ |
| `gender`  | `string` | Optional. Filter by gender. Values: 'זכר' (male) or 'נקבה' (female) |
| `seed`    | `string` | Optional. Seed value for consistent user generation                  |

#### Response Format

```json
{
  "seed": "generated-or-provided-seed",
  "data": {
    "name": {
      "first_name": "string",
      "last_name": "string",
      "title": "string"
    },
    "gender": "string",
    "phone": "string",
    "dob": {
      "date_of_birth": "YYYY-MM-DD",
      "age": 0
    },
    "location": {
      "street": {
        "number": 0,
        "name": "string"
      },
      "city": "string",
      "postcode": 0,
      "coordinates": {
        "latitude": "string",
        "longitude": "string"
      }
    }
  }
}
```

## Examples

### Generate Random User (No Parameters)

```http
GET https://www.randomhebrewuser.xyz/api/
```

Generates a completely random user with a new seed.

### Generate User with Specific Gender

```http
GET https://www.randomhebrewuser.xyz/api/?gender=זכר
```

Generates a random male user.

### Generate User with Specific Seed

```http
GET https://www.randomhebrewuser.xyz/api/?seed=test123
```

Generates a user based on the provided seed. Using the same seed will always return the same user data.

### Generate User with Both Gender and Seed

```http
GET https://www.randomhebrewuser.xyz/api/?gender=נקבה&seed=test123
```

Generates a female user based on the provided seed.

## Technical Details

- Built with FastAPI and SQLAlchemy
- Uses async database operations for improved performance
- Implements concurrent database queries using `asyncio.gather`
- Uses Pydantic models for request/response validation
- Uses slowapi for rate limting(default = 5/min)

## Database Schema

The application uses several tables to store and manage user data:

- `users`: Basic user information
- `phones`: Phone numbers
- `dob`: Dates of birth
- `locations`: Address and coordinate information
- `seeds`: Stores seed mappings for consistent user generation

## Getting Started

1. Set up your environment variables in a `.env` file:
```env
DATABASE_HOSTNAME=your_host
DATABASE_PORT=your_port
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_username
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## Features Still in Developemnt

- Random password generation for each user
- More query parms(resutls,password,format,email)
- Random pictures for each user
- Testing

