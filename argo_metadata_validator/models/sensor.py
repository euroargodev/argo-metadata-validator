"""Models based for parsed sensor metadata."""

from pydantic import BaseModel, Field


class SensorInfo(BaseModel):
    """Model for the sensor_info property."""

    created_by: str
    date_creation: str
    link: str
    format_version: str
    contents: str
    sensor_described: str


class SensorInstance(BaseModel):
    """Model for the SENSOR property."""

    SENSOR: str  # URI
    SENSOR_MAKER: str  # URI
    SENSOR_MODEL: str  # URI
    SENSOR_MODEL_FIRMWARE: str
    SENSOR_SERIAL_NO: str
    sensor_vendorinfo: dict | None = None


class SensorParameter(BaseModel):
    """Model for the PARAMETER property."""

    PARAMETER: str  # URI
    PARAMETER_SENSOR: str  # URI
    PARAMETER_UNITS: str
    PARAMETER_ACCURACY: str
    PARAMETER_RESOLUTION: str
    PREDEPLOYMENT_CALIB_EQUATION: str
    PREDEPLOYMENT_CALIB_COEFFICIENT_LIST: dict[str, str]
    PREDEPLOYMENT_CALIB_COMMENT: str
    PREDEPLOYMENT_CALIB_DATE: str
    parameter_vendorinfo: dict | None = None
    predeployment_vendorinfo: dict | None = None


class Sensor(BaseModel):
    """Model to hold sensor metadata."""

    sensor_info: SensorInfo
    SENSORS: list[SensorInstance]
    PARAMETERS: list[SensorParameter]
    context: dict[str, str] = Field(alias="@context")
    instrument_vendorinfo: dict | None = None
