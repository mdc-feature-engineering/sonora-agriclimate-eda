"""Pydantic schemas for the datasets documented in ``references``."""

from datetime import datetime
from math import isnan
from numbers import Real
from typing import Any, Literal, Optional
import pandas as pd
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


class SequiaSonoraSchema(DatasetSchema):
    """Schema for the tidy CONAGUA drought dataset for Sonora."""
    model_config = ConfigDict(extra="ignore")

    CVE_CONCATENADA: Optional[int] = Field(default=None, ge=0)
    CVE_ENT: Optional[int] = Field(default=None, ge=1)
    CVE_MUN: Optional[int] = Field(default=None, ge=1)
    fecha: Optional[str] = None
    categoria_sequia: Optional[str] = None
    Anio: Optional[int] = Field(default=None, ge=1900, le=2100)
    severidad_num: Optional[int] = Field(default=None, ge=0, le=5)

    @field_validator("*", mode="before")
    @classmethod
    def normalize_missing_values(cls, value):
        # If it is None, an empty string, or pandas NaN, convert it to None
        if value is None or pd.isna(value) or str(value).strip() == "":
            return None
        return value

    @field_validator("fecha", "categoria_sequia", mode="before")
    @classmethod
    def convert_text_fields(cls, value):
        if value is None or pd.isna(value):
            return None
        return str(value).strip()

    @field_validator(
        "CVE_CONCATENADA", "CVE_ENT", "CVE_MUN", "Anio", "severidad_num", mode="before"
    )
    @classmethod
    def convert_numeric_fields(cls, value):
        if value is None or pd.isna(value) or str(value).strip() == "":
            return None
        try:
            return int(float(value))  # float() in case it comes with .0 from pandas
        except (ValueError, TypeError):
            return None


class RepdaAgricolaSchema(BaseModel):
    """Schema for the REPDA concession metadata documented in the project."""

    model_config = ConfigDict(extra="ignore")

    FID: Optional[int] = Field(default=None, ge=0)
    NUM_TITULO: Optional[str] = None
    NUM_APROVE: Optional[str] = None
    NOMBRE: Optional[str] = None
    ESTADO: Optional[int] = Field(default=None, ge=1)
    CLAVE_MUN: Optional[int] = Field(default=None, ge=1)
    MUNICIPIO: Optional[str] = None
    LOCALIDAD: Optional[str] = None
    ACUIFERO: Optional[str] = None
    CUENCA: Optional[str] = None
    USO: Optional[str] = None
    USO_SUB: Optional[str] = None
    USO_LIMPIO: Optional[str] = None
    VOL_CONS: Optional[float] = Field(default=None, ge=0)
    FECHA_HASTA: Optional[str] = None  # Can be adjusted to datetime if preferred
    LATITUD: Optional[float] = None
    LONGITUDE: Optional[float] = None

    @field_validator("*")
    @classmethod
    def normalize_missing_values(cls, value):
        if value is None or pd.isna(value):
            return None
        return value

    @field_validator(
        "NUM_TITULO",
        "NUM_APROVE",
        "NOMBRE",
        "MUNICIPIO",
        "LOCALIDAD",
        "ACUIFERO",
        "CUENCA",
        "USO",
        "USO_SUB",
        "USO_LIMPIO",
        "FECHA_HASTA",
        mode="before",
    )
    @classmethod
    def convert_text_fields(cls, value):
        if value is None or pd.isna(value):
            return None
        return str(value).strip()


class AcuiferoSonoraSchema(BaseModel):
    """Schema for the Sonora aquifers dataset."""
    model_config = ConfigDict(extra="ignore")

    CLAVE: Optional[str] = None
    ACUIFERO: Optional[str] = None
    R: Optional[float] = None
    DNC: Optional[float] = None
    VEAS: Optional[float] = None
    DMA: Optional[float] = None
    DOCUMENTO: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def normalize_missing_values(cls, value):
        # If it is None, an empty string, or pandas NaN, convert it to None
        if value is None or pd.isna(value) or str(value).strip() == "":
            return None
        return value

    @field_validator("CLAVE", "ACUIFERO", "DOCUMENTO", mode="before")
    @classmethod
    def convert_text_fields(cls, value):
        if value is None or pd.isna(value):
            return None
        return str(value).strip()

    @field_validator("R", "DNC", "VEAS", "DMA", mode="before")
    @classmethod
    def convert_numeric_fields(cls, value):
        if value is None or pd.isna(value) or str(value).strip() == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None


__all__ = [
    "AgriculturaSonoraSchema",
    "SequiaSonoraSchema",
    "RepdaAgricolaSchema",
    "AcuiferoSonoraSchema",
]