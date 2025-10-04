"""
Smart Cities Data API
A FastAPI REST API for managing urban sensor data and city metrics
Author: Arnau Ropero
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Smart Cities Data API",
    description="RESTful API for managing smart city sensor data and urban metrics",
    version="1.0.0",
    contact={
        "name": "Arnau Ropero",
        "email": "arnauroperouab@gmail.com",
    }
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums for sensor types
class SensorType(str, Enum):
    temperature = "temperature"
    humidity = "humidity"
    air_quality = "air_quality"
    noise_level = "noise_level"
    traffic_flow = "traffic_flow"
    parking = "parking"
    energy_consumption = "energy_consumption"

# Enums for sensor status
class SensorStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    error = "error"

# Pydantic models
class SensorBase(BaseModel):
    name: str = Field(..., example="Temperature Sensor Plaza Catalunya")
    type: SensorType
    latitude: float = Field(..., ge=-90, le=90, example=41.3851)
    longitude: float = Field(..., ge=-180, le=180, example=2.1734)
    status: SensorStatus = SensorStatus.active
    description: Optional[str] = Field(None, example="Environmental sensor for temperature monitoring")

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[SensorStatus] = None
    description: Optional[str] = None

class Sensor(SensorBase):
    id: int
    created_at: datetime
    last_reading: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class SensorReading(BaseModel):
    sensor_id: int
    value: float = Field(..., example=23.5)
    unit: str = Field(..., example="°C")
    timestamp: datetime = Field(default_factory=datetime.now)
    
class CityMetrics(BaseModel):
    city: str = "Barcelona"
    total_sensors: int
    active_sensors: int
    average_temperature: Optional[float] = None
    average_air_quality: Optional[float] = None
    last_update: datetime

# In-memory database (for demo purposes)
sensors_db = []
readings_db = []
sensor_id_counter = 1

# Initialize with sample data
def init_sample_data():
    global sensors_db, sensor_id_counter
    
    sample_sensors = [
        {
            "id": 1,
            "name": "Temperature Sensor - Sagrada Familia",
            "type": "temperature",
            "latitude": 41.4036,
            "longitude": 2.1744,
            "status": "active",
            "description": "Environmental monitoring near Sagrada Familia",
            "created_at": datetime.now(),
            "last_reading": datetime.now()
        },
        {
            "id": 2,
            "name": "Air Quality Monitor - Eixample",
            "type": "air_quality",
            "latitude": 41.3851,
            "longitude": 2.1734,
            "status": "active",
            "description": "Air quality monitoring in Eixample district",
            "created_at": datetime.now(),
            "last_reading": datetime.now()
        },
        {
            "id": 3,
            "name": "Traffic Flow Sensor - Gran Via",
            "type": "traffic_flow",
            "latitude": 41.3755,
            "longitude": 2.1598,
            "status": "maintenance",
            "description": "Traffic monitoring on Gran Via",
            "created_at": datetime.now(),
            "last_reading": None
        }
    ]
    
    sensors_db = sample_sensors
    sensor_id_counter = 4

# Initialize sample data on startup
init_sample_data()

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """
    Welcome endpoint with API information
    """
    return {
        "message": "Welcome to Smart Cities Data API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "sensors": "/api/v1/sensors",
            "readings": "/api/v1/readings",
            "metrics": "/api/v1/metrics"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "sensors_count": len(sensors_db)
    }

# Sensor CRUD Operations

@app.get("/api/v1/sensors", response_model=List[Sensor], tags=["Sensors"])
async def get_sensors(
    type: Optional[SensorType] = None,
    status: Optional[SensorStatus] = None,
    limit: int = 100
):
    """
    Get all sensors with optional filtering
    """
    filtered_sensors = sensors_db
    
    if type:
        filtered_sensors = [s for s in filtered_sensors if s["type"] == type]
    
    if status:
        filtered_sensors = [s for s in filtered_sensors if s["status"] == status]
    
    return filtered_sensors[:limit]

@app.get("/api/v1/sensors/{sensor_id}", response_model=Sensor, tags=["Sensors"])
async def get_sensor(sensor_id: int):
    """
    Get a specific sensor by ID
    """
    sensor = next((s for s in sensors_db if s["id"] == sensor_id), None)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with ID {sensor_id} not found")
    return sensor

@app.post("/api/v1/sensors", response_model=Sensor, tags=["Sensors"], status_code=201)
async def create_sensor(sensor: SensorCreate):
    """
    Create a new sensor
    """
    global sensor_id_counter
    
    new_sensor = {
        "id": sensor_id_counter,
        **sensor.dict(),
        "created_at": datetime.now(),
        "last_reading": None
    }
    
    sensors_db.append(new_sensor)
    sensor_id_counter += 1
    
    return new_sensor

@app.put("/api/v1/sensors/{sensor_id}", response_model=Sensor, tags=["Sensors"])
async def update_sensor(sensor_id: int, sensor_update: SensorUpdate):
    """
    Update a sensor's information
    """
    sensor = next((s for s in sensors_db if s["id"] == sensor_id), None)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with ID {sensor_id} not found")
    
    update_data = sensor_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        sensor[field] = value
    
    return sensor

@app.delete("/api/v1/sensors/{sensor_id}", tags=["Sensors"])
async def delete_sensor(sensor_id: int):
    """
    Delete a sensor
    """
    global sensors_db
    
    sensor = next((s for s in sensors_db if s["id"] == sensor_id), None)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with ID {sensor_id} not found")
    
    sensors_db = [s for s in sensors_db if s["id"] != sensor_id]
    
    return {"message": f"Sensor {sensor_id} deleted successfully"}

# Sensor Readings

@app.post("/api/v1/readings", response_model=SensorReading, tags=["Readings"], status_code=201)
async def create_reading(reading: SensorReading):
    """
    Submit a new sensor reading
    """
    # Check if sensor exists
    sensor = next((s for s in sensors_db if s["id"] == reading.sensor_id), None)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with ID {reading.sensor_id} not found")
    
    # Update sensor's last reading time
    sensor["last_reading"] = reading.timestamp
    
    # Store reading
    readings_db.append(reading.dict())
    
    return reading

@app.get("/api/v1/readings/{sensor_id}", response_model=List[SensorReading], tags=["Readings"])
async def get_sensor_readings(sensor_id: int, limit: int = 100):
    """
    Get readings for a specific sensor
    """
    sensor = next((s for s in sensors_db if s["id"] == sensor_id), None)
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor with ID {sensor_id} not found")
    
    sensor_readings = [r for r in readings_db if r["sensor_id"] == sensor_id]
    return sensor_readings[-limit:]

# City Metrics

@app.get("/api/v1/metrics", response_model=CityMetrics, tags=["Metrics"])
async def get_city_metrics():
    """
    Get aggregated city metrics
    """
    total_sensors = len(sensors_db)
    active_sensors = len([s for s in sensors_db if s["status"] == "active"])
    
    # Calculate average temperature (mock data for demo)
    temp_sensors = [s for s in sensors_db if s["type"] == "temperature" and s["status"] == "active"]
    avg_temp = 22.5 if temp_sensors else None
    
    # Calculate average air quality (mock data for demo)
    air_sensors = [s for s in sensors_db if s["type"] == "air_quality" and s["status"] == "active"]
    avg_air = 2.0 if air_sensors else None  # AQI scale 1-5
    
    return CityMetrics(
        city="Barcelona",
        total_sensors=total_sensors,
        active_sensors=active_sensors,
        average_temperature=avg_temp,
        average_air_quality=avg_air,
        last_update=datetime.now()
    )

@app.get("/api/v1/metrics/summary", tags=["Metrics"])
async def get_metrics_summary():
    """
    Get a summary of all sensor types and their counts
    """
    summary = {}
    
    for sensor_type in SensorType:
        type_sensors = [s for s in sensors_db if s["type"] == sensor_type]
        active_count = len([s for s in type_sensors if s["status"] == "active"])
        
        summary[sensor_type] = {
            "total": len(type_sensors),
            "active": active_count,
            "percentage_active": round((active_count / len(type_sensors) * 100) if type_sensors else 0, 2)
        }
    
    return {
        "summary": summary,
        "total_sensors": len(sensors_db),
        "timestamp": datetime.now()
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
