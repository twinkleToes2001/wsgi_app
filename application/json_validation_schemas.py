"""JSON Schemas for validate POST request data
using jsonschema library"""

ONE_WORD_CAPITALIZE = "^[A-Z][a-z]+"
EMAIL = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

employee_json_schema = {
            "type": "object",
            "properties": {
                "department_id": {
                    "type": "integer",
                    "minimum": 1
                },
                "email": {
                    "type": "string",
                    "pattern": EMAIL
                },
                "first_name": {
                    "type": "string",
                    "pattern": ONE_WORD_CAPITALIZE
                },
                "job_id": {
                    "type": "integer",
                    "minimum": 1
                },
                "last_name": {
                    "type": "string",
                    "pattern": ONE_WORD_CAPITALIZE
                }
            },
            "required": [
                "department_id",
                "email",
                "first_name",
                "job_id",
                "last_name"
            ],
            "title": "Temperatures"
        }

job_json_schema = {
    "type": "object",
    "properties": {
        "job_title": {
            "type": "string",
            "minLength": 3,
            "maxLength": 20,
            "pattern": ONE_WORD_CAPITALIZE
        },
        "salary": {
            "type": "integer",
            "minimum": 100,
            "maximum": 10000
        }
    },
    "required": [
        "job_title",
        "salary"
    ]
}

department_json_schema = {
    "type": "object",
    "properties": {
        "department_name": {
            "type": "string",
            "minLength": 5,
            "maxLength": 20,
            "pattern": ONE_WORD_CAPITALIZE
        },
        "location": {
            "type": "string",
            "minLength": 5,
            "maxLength": 30,
            "pattern": ONE_WORD_CAPITALIZE
        }
    },
    "required": [
        "department_name",
        "location"
    ]
}
