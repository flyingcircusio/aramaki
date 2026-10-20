import datetime
import hashlib
import hmac
import uuid
from typing import Annotated, Any, Literal, Self

import rfc8785
from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    ValidationInfo,
    field_serializer,
    model_validator,
)

from aramaki import utils


class MessageAuthenticationError(Exception):
    pass


class MessageTooOldError(MessageAuthenticationError):
    pass


class InvalidSignatureError(MessageAuthenticationError):
    pass


class MessageSignature(BaseModel):
    alg: str = "HS256"
    signature: str | None = None


class Message(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )

    id: str = Field(default_factory=lambda: uuid.uuid4().hex, alias="@id")
    type: str = Field(alias="@type")
    context: str = Field(default="https://flyingcircus.io/ns/aramaki", alias="@context")
    version: int = Field(default=1, alias="@version")
    signature: MessageSignature = Field(
        default_factory=MessageSignature, alias="@signature"
    )
    principal: str = Field(alias="@principal")
    application: str | None = Field(default=None, alias="@application")
    issued: AwareDatetime = Field(default_factory=utils.now, alias="@issued")
    expiry: AwareDatetime = Field(
        default_factory=lambda: utils.now() + datetime.timedelta(hours=1),
        alias="@expiry",
    )

    @field_serializer("issued", "expiry")
    def serialize_timestamp(self, dt: AwareDatetime, _info: Any) -> str:
        return dt.isoformat()

    @model_validator(mode="after")
    def _validate_lifecycle_and_wire(self, info: ValidationInfo) -> Self:
        allow_defaults = (info.context or {}).get("allow_defaults", True)
        if not allow_defaults:
            missing = [
                field_info.alias or name
                for name, field_info in type(self).model_fields.items()
                if name not in self.model_fields_set and field_info.default is not None
            ]
            if missing:
                formatted = ", ".join(sorted(missing))
                raise ValueError(f"Missing required fields for validation: {formatted}")

        return self

    def _sign_and_return_signature(self, secret: bytes | bytearray) -> str:
        """
        Signs the message and returns the signature. Can be used for signing and validation.
        """
        message = self.model_dump(mode="json")
        message["@signature"].pop("signature", None)
        return hmac.new(
            secret,
            rfc8785.dumps(message),
            hashlib.sha256,
        ).hexdigest()

    def sign(self, secret: bytes | bytearray) -> None:
        """
        Signs the message and sets the signature on the message.
        """
        self.signature.signature = self._sign_and_return_signature(secret)

    def authenticate(self, secret: bytes | bytearray) -> None:
        """
        Checks if the message is authenticated.

        This does NOT prevent replaying attacks, users of this library must protect
        against such attack on their side.

        Returns None.
        Raises an Exception of type MessageAuthenticationError or subclasses if unauthenticated.
        """
        if self.expiry < datetime.datetime.now(datetime.UTC):
            raise MessageTooOldError(f"message too old (expired at {self.expiry})")

        new_sig = self._sign_and_return_signature(secret)
        if new_sig != self.signature.signature:
            raise InvalidSignatureError(
                f"signature mismatch {new_sig} != {self.signature.signature}"
            )


class SubscriptionMatch(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )
    type: str = Field(alias="@type")
    scope: dict[str, str]


class SubscriptionMessage(Message):
    type: Literal["aramaki.subscription"] = Field(
        default="aramaki.subscription", alias="@type"
    )
    matches: list[SubscriptionMatch]


class CollectionScope(BaseModel):
    principal: str
    application: str
    collection: str


class CollectionCatchupRequestMessage(Message):
    type: Literal["directory.collection.catchup.request"] = Field(
        default="directory.collection.catchup.request", alias="@type"
    )

    collection: str
    partition: str | None
    current_version: int


class CollectionCatchupStartMessage(Message):
    type: Literal["directory.collection.catchup.start"] = Field(
        default="directory.collection.catchup.start", alias="@type"
    )

    scope: CollectionScope | None = Field(default=None, alias="@scope")
    collection: str
    partition: str
    start_version: int


class CollectionCatchupStepMessage(Message):
    type: Literal["directory.collection.catchup.step"] = Field(
        default="directory.collection.catchup.step", alias="@type"
    )

    scope: CollectionScope | None = Field(default=None, alias="@scope")
    collection: str
    partition: str
    from_version: int
    to_version: int
    is_final_record: bool
    record_id: int
    change: Literal["update", "delete", "null"]
    data: Any


class CollectionUpdateMessage(Message):
    type: Literal["directory.collection.update"] = Field(
        default="directory.collection.update", alias="@type"
    )

    scope: CollectionScope | None = Field(default=None, alias="@scope")
    collection: str
    partition: str
    version: int
    change: Literal["update", "delete", "null"]
    data: Any
    record_id: str | int


KnownMessages = Annotated[
    CollectionCatchupRequestMessage
    | CollectionCatchupStartMessage
    | CollectionCatchupStepMessage
    | CollectionUpdateMessage,
    Field(discriminator="type"),  # Points to the Python field name that handles '@type'
]
AnyMessage = Annotated[KnownMessages | Message, Field(union_mode="left_to_right")]

message_adapter = TypeAdapter(AnyMessage)
