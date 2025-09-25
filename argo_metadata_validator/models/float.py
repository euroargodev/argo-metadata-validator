"""Models based for parsed float metadata."""

from pydantic import BaseModel, Field

from argo_metadata_validator.models.platform import PlatformInfo, PlatformInstance
from argo_metadata_validator.models.sensor import SensorInfo, SensorInstance, SensorParameter


class FloatInfo(BaseModel):
    """Model for the float_info property."""

    created_by: str
    date_creation: str
    link: str
    format_version: str
    contents: str
    float_described: str


class Float(BaseModel):
    """Model to hold float metadata."""

    context: dict[str, str] = Field(alias="@context")
    float_info: FloatInfo
    files_merged: list[str]
    platform_info: PlatformInfo
    sensor_info_list: list[SensorInfo]
    PLATFORM: PlatformInstance
    SENSORS: list[SensorInstance]
    PARAMETERS: list[SensorParameter]
