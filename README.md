# Risk Engine API

## Requirements:
Flask 1.0.2+

## Excecution:

### Flask server
`$ python app.py`
Waits for POST requests on `http://127.0.0.1:5000/risk_profile`


---

# Backend Take-Home Assignment
Orign offers its users an insurance package personalized to their specific needs without requiring the user to understand anything about insurance. This allows Orign to act as their *de facto* insurance advisor.

Orign determines the user’s insurance needs by asking personal & risk-related questions and gathering information about the user’s vehicle(s) and house(s). Using this data, Orign determines their risk profile for **each** line of insurance and then suggests an insurance plan (`"economic"`, `"regular"`, `"responsible"`) corresponding to her risk profile.

For this assignment, you will create a simple version of that application by coding a simple API endpoint that receives a JSON payload with the user information and returns her risk profile (JSON again) – you don’t have to worry about the frontend of the application.

## The input
First, the would-be frontend of this application asks the user for her **personal information**. Then, it lets her add her **house(s)** and **vehicle(s)**. Finally, it asks her to answer 3 binary **risk questions**. The result produces a JSON payload, posted to the application’s API endpoint, like this example:

```JSON
{
  "age": 35,
  "dependents": 2,
  "houses": [
    {"key": 1, "ownership_status": "owned"},
    {"key": 2, "ownership_status": "mortgaged"}
  ],
  "income": 0,
  "marital_status": "married",
  "risk_questions": [0, 1, 0],
  "vehicles": [
    {"key": 1, "year": 2018}
  ]
}
```

### User attributes
All user attributes are required:

- Age (a positive integer).
- Number of dependents (a positive integer).
- Income (a positive integer).
- Marital status (`”single"` or `”married"`).
- Risk answers (an array with 3 booleans).

### House(s)
The user can have from 0 to N houses, all with just one attribute: `ownership_status`, which can be `"owned"` or `”mortgaged"`.

### Vehicles
The user can have from 0 to N vehicles, all with just one attribute: a positive integer corresponding to the `year` it was manufactured.

## The risk algorithm
The application receives the JSON payload through the API endpoint and transforms it into a *risk profile* by calculating a *risk score* for each line of insurance (life, disability, home, auto & umbrella) based on the information provided by the user.

First, it calculates the *base score* by summing the answers from the risk questions, resulting in a number ranging from 0 to 3. Then, it applies the following rules to determine a *risk score* for each line of insurance*.

1. If the user doesn’t have income, a vehicle or a house, she is ineligible for disability, auto, and home insurance, respectively.
2. If the user is over 60 years old, she is ineligible for disability and life insurance.
3. If the user is under 30 years old, deduct 2 risk points from all lines of insurance. If she is between 30 and 40 years old, deduct 1.
4. If her income is above $200k, deduct 1 risk point from all lines of insurance. 
5. If the house is mortgaged, add 1 risk point to that home’s score. If the user has at least one mortgaged house, add 1 risk point to her disability score. 
6. If the user has dependents, add 1 risk point to both the disability and life scores. 
7. If the user is married, add 1 risk point to the life score and remove 1 risk point from disability. 
8. If the vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.
9. If the user has only one vehicle, add 1 point to that vehicle’s score. This same rule applies to houses. 
10. If the user got an economic score in any of the four main lines of insurance (life, disability, home & auto), he is eligible to get umbrella insurance. 

This algorithm results in a final score for each line of insurance, which should be processed using the following ranges:

- **0 and below** maps to **“economic”**.
- **1 and 2** maps to **“regular”**.
- **3 and above** maps to **“responsible”**.

*NB:  If the user has more than one vehicle or house, each item will have its own risk score.

## The output
Considering the data provided above, the application should return the following JSON payload:

```JSON
{
    "auto": [
        {
            "key": 1,
            "value": "regular"
        }
    ],
    "disability": "ineligible",
    "home": [
        {
            "key": 1,
            "value": "economic"
        },
        {
            "key": 2,
            "value": "regular"
        }
    ],
    "life": "regular",
    "umbrella": "regular"
}
```

## Criteria
You may use any language and framework, provided that you build a solid system with an emphasis on code quality, simplicity, readability, maintainability, and reliability; particularly with regards to architecture and testing.

This assignment should be doable in less than one day. We expect you to learn fast, **communicate with us**, and make decisions regarding its implementation & scope to achieve the expected results on time.

It is not necessary to build the screens a user would interact with, however, as the API is intended to power a user-facing application, we expect the implementation to be as close as possible to what would be necessary in real-life.