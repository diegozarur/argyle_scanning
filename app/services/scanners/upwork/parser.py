from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class Address(BaseModel):
    city: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class BasePay(BaseModel):
    amount: Optional[str] = None
    period: Optional[str] = None
    currency: Optional[str] = None


class PlatformIds(BaseModel):
    employee_id: Optional[str] = None
    position_id: Optional[str] = None
    platform_user_id: Optional[str] = None


class ParsedProfile(BaseModel):
    id: Optional[str] = None
    account: Optional[str] = None
    address: Address = Address()
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    picture_url: Optional[str] = None
    employment_status: Optional[str] = None
    employment_type: Optional[str] = None
    job_title: Optional[str] = None
    ssn: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    original_hire_date: Optional[str] = None
    hire_date: Optional[str] = None
    termination_date: Optional[str] = None
    termination_reason: Optional[str] = None
    employer: Optional[str] = None
    base_pay: BasePay = BasePay()
    pay_cycle: Optional[str] = None
    platform_ids: PlatformIds = PlatformIds()
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    metadata: Dict = Field(default_factory=dict)

    @validator('birth_date', 'original_hire_date', 'hire_date', 'termination_date', 'created_at', 'updated_at',
               pre=True, always=True)
    def validate_dates(cls, value):
        if value in (None, ""):
            return ""
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            return ""


def parse_profile(response_json: Dict[str, Any]) -> ParsedProfile:
    profile = response_json.get("profile", {})
    identity = profile.get("identity", {})
    profile_data = profile.get("profile", {})
    location = profile_data.get("location", {})
    portrait = profile_data.get("portrait", {})
    stats = profile.get("stats", {})

    person_data = response_json.get("person")

    return ParsedProfile(
        id=identity.get("ciphertext", ""),
        account=identity.get("uid", ""),
        address=Address(
            city=location.get("city"),
            state=location.get("state"),
            country=location.get("country"),
        ),
        first_name=person_data.get("first_name", ""),
        last_name=person_data.get("last_name", ""),
        full_name=profile_data.get("name", ""),
        birth_date=person_data.get("dateOfBirth", ""),
        picture_url=portrait.get("portrait", ""),
        job_title=profile_data.get("title", ""),
        base_pay=BasePay(
            amount=str(stats.get("hourlyRate", {}).get("amount", "")),
            currency=stats.get("hourlyRate", {}).get("currencyCode", ""),
        ),
        created_at=profile_data.get("memberSince", ""),
        updated_at=person_data.get("updatedOn", ""),
    )
