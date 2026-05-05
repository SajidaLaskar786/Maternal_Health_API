from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mock_model import call_maternal_health_model

app = FastAPI()

# Combined Input Model (GDM + Anemia) with validation
class MaternalHealthInput(BaseModel):
    # GDM Inputs
    age: int = Field(gt=0, le=100)  # Age must be positive and realistic
    gravida: int = Field(ge=1)  # Gravida at least 1
    gest_weeks: int = Field(ge=1, le=42)  # Gestational weeks realistic
    prev_gdm: bool  # Changed to bool for yes/no
    family: bool
    pcod: bool
    waist: float = Field(gt=0)
    bp_sys: int = Field(gt=0)
    bp_dia: int = Field(gt=0)
    activity: str = Field(min_length=1)
    thirst: bool
    urination: bool
    hunger: bool
    dark: bool

    # Anemia Inputs
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    iron_intake: bool
    diet_quality: str = Field(min_length=1)
    fatigue: bool
    dizziness: bool
    pale_eyelids: bool
    pale_nails: bool
    tongue: bool
    history: bool

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/mht/")
def submit_health_status(data: MaternalHealthInput):
    try:
        health_status = call_maternal_health_model(
            age=data.age,
            gravida=data.gravida,
            gest_weeks=data.gest_weeks,
            prev_gdm=data.prev_gdm,
            family=data.family,
            pcod=data.pcod,
            waist=data.waist,
            bp_sys=data.bp_sys,
            bp_dia=data.bp_dia,
            activity=data.activity,
            thirst=data.thirst,
            urination=data.urination,
            hunger=data.hunger,
            dark=data.dark,
            height_cm=data.height_cm,
            weight_kg=data.weight_kg,
            iron_intake=data.iron_intake,
            diet_quality=data.diet_quality,
            fatigue=data.fatigue,
            dizziness=data.dizziness,
            pale_eyelids=data.pale_eyelids,
            pale_nails=data.pale_nails,
            tongue=data.tongue,
            history=data.history
        )
        return {"health_status": health_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")