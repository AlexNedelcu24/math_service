from pydantic import BaseModel


class ComputeRequest(BaseModel):
    operation: str
    value: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "operation": "fib",
                    "value": 10
                }
            ]
        }
    }


class PowRequest(BaseModel):
    base: int
    exponent: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "base": 2,
                    "exponent": 5
                }
            ]
        }
    }


class JobResponse(BaseModel):
    job_id: int
    status: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "job_id": 1,
                "status": "pending"
            }
        }
    }

class ResultResponse(BaseModel):
    operation: str
    input: str
    result: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "operation": "fib",
                "input": "10",
                "result": "55"
            }
        }
    }

