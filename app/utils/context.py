from contextvars import ContextVar

# Context variable to hold the authorization token for the current request
request_token: ContextVar[str] = ContextVar("request_token", default="")
request_program_id: ContextVar[str] = ContextVar("request_program_id", default="")
request_session_id: ContextVar[str] = ContextVar("request_session_id", default="")