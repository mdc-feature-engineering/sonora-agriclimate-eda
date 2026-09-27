"""Pydantic schemas for the datasets documented in ``references``."""

from datetime import datetime
from math import isnan
from numbers import Real
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DatasetSchema(BaseModel):
    """Common configuration for schemas loaded from tabular or GIS data."""

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    @field_validator("*", mode="before")
    @classmethod
    def normalize_missing_values(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, Real) and isnan(value):
            return None
        return value


class AgriculturaSonoraSchema(DatasetSchema):
    """Schema for the Sonora agriculture production dataset."""

    ANO: Optional[str] = Field(default=None, pattern=r"^\d{4}$")
    CIERREYAVAN: Optional[str] = None
    CICLO: Optional[int] = Field(default=None, ge=1, le=3)
    CDDR: Optional[str] = None
    NDDR: Optional[str] = None
    CMUN: Optional[str] = None
    NMUN: Optional[str] = None
    CVMES: Optional[str] = None
    NMES: Optional[str] = None
    CVECUL: Optional[str] = None
    CULTIVO: Optional[str] = None
    CVEVAR: Optional[str] = None
    DESVAR: Optional[str] = None
    SUPSEM: Optional[float] = Field(default=None, ge=0)
    SUPCOSE: Optional[float] = Field(default=None, ge=0)
    SUPSINI: Optional[float] = Field(default=None, ge=0)
    PRODTON: Optional[float] = Field(default=None, ge=0)
    RENDMNTO: Optional[float] = Field(default=None, ge=0)
    PMR: Optional[float] = Field(default=None, ge=0)
    VALPROD: Optional[float] = Field(default=None, ge=0)

    @field_validator(
        "ANO",
        "CIERREYAVAN",
        "CDDR",
        "NDDR",
        "CMUN",
        "NMUN",
        "CVMES",
        "NMES",
        "CVECUL",
        "CULTIVO",
        "CVEVAR",
        "DESVAR",
        mode="before",
    )
    @classmethod
    def coerce_text_fields(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        return str(value).strip()


class ConaguaSequiaSchema(DatasetSchema):
    """Schema for the tidy CONAGUA drought dataset for Sonora."""

    CVE_CONCATENADA: Optional[int] = None
    CVE_ENT: Optional[int] = Field(default=None, ge=0)
    CVE_MUN: Optional[int] = Field(default=None, ge=0)
    fecha: Optional[datetime] = None
    categoria_sequia: Optional[
        Literal["Sin Sequía", "D0", "D1", "D2", "D3", "D4"]
    ] = None
    Anio: Optional[int] = Field(default=None, ge=1900, le=2200)
    severidad_num: Optional[int] = Field(default=None, ge=0, le=5)


class InegiHidrografiaSchema(DatasetSchema):
    """Schema for the INEGI hydrographic network layer for Sonora."""

    FID: Optional[int] = None
    NOMBRE: Optional[str] = None
    TIPO: Optional[str] = None
    ORDEN: Optional[int] = Field(default=None, ge=0)
    LONGITUD: Optional[float] = Field(default=None, ge=0)
    CVE_ENT: Optional[str] = None
    geometry: Optional[Any] = None


class RepdaConcesionSchema(DatasetSchema):
    """Schema for the REPDA concession metadata documented in the project."""

    name: Optional[str] = None
    type: Optional[str] = None
    alias: Optional[str] = None
    length: Optional[float] = Field(default=None, ge=0)


__all__ = [
    "AgriculturaSonoraSchema",
    "ConaguaSequiaSchema",
    "InegiHidrografiaSchema",
    "RepdaConcesionSchema",
]