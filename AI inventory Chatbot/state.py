from typing import TypedDict, Union

class State(TypedDict):

    question: str
    sql_query: str
    sql_result: Union[list[dict], str]
    response : str
    error: str

    