"""API Schemas."""
import json
from datetime import datetime
from typing import Optional, Any

from humps import camelize
from pydantic import BaseModel, Field, model_validator
from starlette.responses import Response


class CustomBaseModel(BaseModel):
    """Custom base model that changes the default pydantic settings."""

    class Config:
        """Model config class to customize some pydantic options."""

        str_strip_whitespace = True  # Trim strings by default
        alias_generator = camelize  # Forces lowerCamelCase
        populate_by_name = True  # Allow the alias trick
        use_enum_values = True  # Better enums


class PrettyJSONResponse(Response):
    """Helps setup FastAPI to pretty print the responses."""

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        """Render the json results."""
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


class MessageReference(CustomBaseModel, BaseModel):
    """The MessageReference model containing only its Primary Keys."""

    class Config:
        """Allow this class to be hashable and used in sets."""

        frozen = True  # MUST be frozen otherwise several set-based algorithms will fail.

    id: Optional[str] = Field(default=None, description="The id of this Message.")
    message: str = Field(default=None, description="The id of this Message.")

    def __hash__(self):
        """Case-insensitive hash."""
        return hash((str(self.blockchain).lower().strip(), str(self.address).lower().strip(),
                     str(self.token_id).lower().strip()))

    def __eq__(self, other):
        """Equality check for the MessageReference class."""
        return isinstance(other, MessageReference) and (self.__hash__() == other.__hash__() or
                                                        (other.id is not None and self.id is not None
                                                         and other.id.lower().strip() == self.id.lower().strip()))

    @model_validator(mode='before')
    def fix_id(cls, values):
        """Generate the ids from messages."""
        # Ensure the elrond data is correct
        if values.get('message'):
            values['id'] = str(hash(values.get('message')))
        return values


class Sentiment(MessageReference):
    """The Sentiment model."""

    sentiment: Optional[str] = Field(default=None, description="The sentiment of this Message.")
    score: Optional[float] = Field(default=None, description="The sentiment score of the Message.")
    sentiment_updated_at: Optional[datetime] = Field(default=None,
                                                     description="The last time this message was update.")


class MessagesPayloadList(CustomBaseModel):
    """Sentiment Endpoint Payload List."""

    messages: list[MessageReference] = Field(default_factory=list,
                                             description="The list of messages to calculate the sentiment")


class SentimentResults(CustomBaseModel):
    """Checklist endpoint output schema."""

    data: list[Sentiment] = Field(default_factory=list, description="Results list.")


class HealthcheckResult(CustomBaseModel):
    """Healthcheck output schema."""

    api_server_online: bool = Field(default=False, description="True if the api server is online.")
