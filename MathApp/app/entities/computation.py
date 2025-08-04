from datetime import datetime


class Computation:
    def __init__(
        self,
        id: int,
        operation: str,
        input_value: str,
        result: str,
        status: str,
        timestamp: datetime
    ):
        self.__id = id
        self.__operation = operation
        self.__input_value = input_value
        self.__result = result
        self.__status = status
        self.__timestamp = timestamp

    # --- getters ---
    def get_id(self) -> int:
        return self.__id

    def get_operation(self) -> str:
        return self.__operation

    def get_input_value(self) -> str:
        return self.__input_value

    def get_result(self) -> str:
        return self.__result

    def get_status(self) -> str:
        return self.__status

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    # --- setters ---
    def set_id(self, new_id: int):
        self.__id = new_id

    def set_operation(self, new_operation: str):
        self.__operation = new_operation

    def set_input_value(self, new_input: str):
        self.__input_value = new_input

    def set_result(self, new_result: str):
        self.__result = new_result

    def set_status(self, new_status: str):
        self.__status = new_status

    def set_timestamp(self, new_timestamp: datetime):
        self.__timestamp = new_timestamp

    def __eq__(self, other) -> bool:
        if not isinstance(other, Computation):
            return False
        return (
                self.__id == other.get_id() and
                self.__operation == other.get_operation() and
                self.__input_value == other.get_input_value() and
                self.__result == other.get_result() and
                self.__status == other.get_status() and
                self.__timestamp == other.get_timestamp()
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.get_id()}; "
            f"Operation: {self.get_operation()}; "
            f"Input: {self.get_input_value()}; "
            f"Result: {self.get_result()}; "
            f"Status: {self.get_status()}; "
            f"Timestamp: {self.get_timestamp()}"
        )
