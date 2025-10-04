# 🚀 Smart Cities Data API

RESTful API built with FastAPI for managing smart city sensor data and urban metrics.

## 📋 Overview

A modern REST API designed for Smart Cities applications, providing endpoints to manage IoT sensors, collect readings, and analyze urban metrics. Built with FastAPI for high performance and automatic API documentation.

## ✨ Features

- **Complete CRUD operations** for sensor management
- **Real-time sensor readings** collection and storage
- **City metrics aggregation** for data analysis
- **Automatic API documentation** with Swagger/OpenAPI
- **Data validation** using Pydantic models
- **CORS enabled** for web application integration
- **Type hints** throughout the codebase

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server
- **Python 3.7+** - Type hints and async support

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/arnauropero/smart-cities-api.git
cd smart-cities-api
pip install -r requirements.txt
```
Run the API
```bash
python main.py
```
Or with Uvicorn directly:
```bash
uvicorn main:app --reload
```
The API will be available at http://localhost:8000

##📚 API Documentation
Once running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

🔌 API Endpoints
Sensors

GET /api/v1/sensors - List all sensors
GET /api/v1/sensors/{id} - Get specific sensor
POST /api/v1/sensors - Create new sensor
PUT /api/v1/sensors/{id} - Update sensor
DELETE /api/v1/sensors/{id} - Delete sensor

Readings

POST /api/v1/readings - Submit sensor reading
GET /api/v1/readings/{sensor_id} - Get sensor readings

Metrics

GET /api/v1/metrics - Get city metrics
GET /api/v1/metrics/summary - Get metrics summary

## 💡 Example Usage
Create a new sensor
```python
import requests

sensor_data = {
    "name": "Temperature Sensor Park Güell",
    "type": "temperature",
    "latitude": 41.4145,
    "longitude": 2.1527,
    "status": "active",
    "description": "Monitoring temperature at Park Güell"
}

response = requests.post("http://localhost:8000/api/v1/sensors", json=sensor_data)
print(response.json())
```
Submit a reading
```python
reading_data = {
    "sensor_id": 1,
    "value": 23.5,
    "unit": "°C"
}

response = requests.post("http://localhost:8000/api/v1/readings", json=reading_data)
print(response.json())
```

## 🏗️ Project Structure
```bash
smart-cities-api/
│
├── main.py              # FastAPI application
├── requirements.txt     # Project dependencies
├── README.md           # Documentation
└── .gitignore          # Git ignore file
```

## 🎯 Use Cases

IoT Integration: Connect city sensors and devices
Urban Monitoring: Track environmental conditions
Data Analytics: Analyze city patterns and trends
Smart City Dashboards: Backend for visualization tools
Research Projects: Academic urban studies

## 📊 Sensor Types Supported

Temperature sensors
Humidity monitors
Air quality sensors
Noise level meters
Traffic flow counters
Parking availability
Energy consumption meters

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Authentication & authorization
- [ ] WebSocket support for real-time updates
- [ ] Data export (CSV/JSON/Excel)
- [ ] Advanced analytics endpoints
- [ ] Rate limiting
- [ ] Docker containerization

## 👨‍💻 Author
**Arnau Ropero**

Smart Cities Engineering Student at UAB
- GitHub: [@arnauropero](https://github.com/arnauropero)
- LinkedIn: [arnau-ropero-garcia](https://linkedin.com/in/arnau-ropero-garcia)

## 📝 License
MIT License


