"""Models based for parsed platform metadata."""

from pydantic import BaseModel, Field


class PlatformInfo(BaseModel):
    """Model for the platform_info property."""

    created_by: str
    date_creation: str
    link: str | None = None
    format_version: str
    contents: str
    platform_described: str


class PlatformInstance(BaseModel):
    """Model for the PLATFORM property."""

    PTT: str
    POSITIONING_SYSTEM: list[str]
    TRANS_SYSTEM: list[str]
    PLATFORM_FAMILY: str
    PLATFORM_TYPE: str
    PLATFORM_MAKER: str
    WMO_INST_TYPE: str | None = None
    FIRMWARE_VERSION: str
    MANUAL_VERSION: str
    FLOAT_SERIAL_NO: str
    BATTERY_TYPE: str
    BATTERY_PACKS: str | None = None
    CONTROLLER_BOARD_TYPE_PRIMARY: str
    CONTROLLER_BOARD_SERIAL_NO_PRIMARY: str
    CONTROLLER_BOARD_TYPE_SECONDARY: str | None = None
    CONTROLLER_BOARD_SERIAL_NO_SECONDARY: str | None = None
    platform_vendorinfo: dict | None = None


class Platform(BaseModel):
    """Model to hold sensor metadata."""

    platform_info: PlatformInfo
    PLATFORM: PlatformInstance
    context: dict[str, str] = Field(alias="@context")
