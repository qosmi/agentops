from pydantic import BaseModel


class ToolDefinition(BaseModel):
    name: str
    description: str