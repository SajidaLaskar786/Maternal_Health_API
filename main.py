from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from Maternal_Health_Model.src.model_logic.gdm_predict import predict_gdm
from Maternal_Health_Model.src.model_logic.anemia_predict import predict_anemia

app = FastAPI()



class MaternalHealthInput(BaseModel):
    # GDM
    age: int = Field(gt=0, le=100)
    gravida: int = Field(ge=1)
    gest_weeks: int = Field(ge=1, le=42)
    prev_gdm: bool
    family: bool
    pcod: bool
    waist: float = Field(gt=0)
    bp_sys: int = Field(gt=0)
    bp_dia: int = Field(gt=0)
    activity: str
    thirst: bool
    urination: bool
    hunger: bool
    dark: bool

    # Anemia
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    iron_intake: str
    diet_quality: str
    fatigue: bool
    dizziness: bool
    pale_eyelids: bool
    pale_nails: bool
    tongue: str
    history: bool



def prepare_gdm_input(data: MaternalHealthInput):
    return {
        "Age": data.age,
        "Gravida": data.gravida,
        "Gestational_Age_weeks": data.gest_weeks,
        "Previous_GDM": "Yes" if data.prev_gdm else "No",
        "Family_Diabetes": "Yes" if data.family else "No",
        "PCOD": "Yes" if data.pcod else "No",
        "Waist_cm": data.waist,
        "BP_Systolic": data.bp_sys,
        "BP_Diastolic": data.bp_dia,
        "Physical_Activity": data.activity,
        "Excess_Thirst": "Yes" if data.thirst else "No",
        "Frequent_Urination": "Yes" if data.urination else "No",
        "Excess_Hunger": "Yes" if data.hunger else "No",
        "Dark_Skin_Patches": "Yes" if data.dark else "No",
    }


def prepare_anemia_input(data: MaternalHealthInput):
    return {
        "Height_cm": data.height_cm,
        "Weight_kg": data.weight_kg,
        "Iron_Intake": data.iron_intake,
        "Diet_Quality": data.diet_quality,
        "Fatigue": "Yes" if data.fatigue else "No",
        "Dizziness": "Yes" if data.dizziness else "No",
        "Pale_Eyelids": "Yes" if data.pale_eyelids else "No",
        "Pale_Nails": "Yes" if data.pale_nails else "No",
        "Tongue_Color": data.tongue,
        "Anemia_History": "Yes" if data.history else "No",
    }



@app.get("/")
def home():
    return {"message": "Maternal Health API running 🚀"}



@app.post("/gdm")
def gdm_endpoint(data: MaternalHealthInput):
    try:
        gdm_input = prepare_gdm_input(data)
        result = predict_gdm(gdm_input)
        return {"gdm_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/anemia")
def anemia_endpoint(data: MaternalHealthInput):
    try:
        anemia_input = prepare_anemia_input(data)
        result = predict_anemia(anemia_input)
        return {"anemia_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/mht")
def combined_endpoint(data: MaternalHealthInput):
    try:
        gdm_input = prepare_gdm_input(data)
        anemia_input = prepare_anemia_input(data)

        gdm_result = predict_gdm(gdm_input)
        anemia_result = predict_anemia(anemia_input)

        return {
            "gdm": gdm_result,
            "anemia": anemia_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))