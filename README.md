# Travel Planner App

A full-stack travel planning web application built with Django REST Framework (backend) and React (frontend).

## 🚀 Features
- User authentication (JWT)
- Create & manage trips with itineraries
- Real-time weather updates (OpenWeather API)
- Google Maps integration
- Wishlist and cart system for planning
---

## 🔧 Setup Instructions

### 1. Clone the repository 

git clone https://github.com/yourusername/travel-planner-app.git
cd travel-planner-app/backend

### 2. Create & activate a virtual environment 
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4.Configure environment variables
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True

### 5. Apply migrations & run server
python manage.py migrate
python manage.py runserver

### Frontend Setup (React)
cd ../frontend
npm install
npm run dev
