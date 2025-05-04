# ClassConnect Backoffice

**ClassConnect Backoffice** is the administrative and monitoring dashboard for the ClassConnect system. It provides tools for managing users, configuring access permissions, and monitoring the health and usage of services within the platform.

## 📚 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [License](#️-license)

## 🔧 Features

- 🧑‍💼 **Admin Registration & Login**  
  Secure authentication for administrators with role-based access.

- 🔒 **User Management**  
  - Block/unblock users  
  - Grant or revoke access permissions  
  - View user activity and status

- 📊 **System Monitoring**  
  Integrated with **Prometheus** and **Grafana** for real-time metrics visualization and alerting.

- ⚙️ **Service Management**  
  Tools for tracking service health, usage statistics, and logs.

## 🧱 Tech Stack

### Frontend
- React with Vite
- React Router DOM
- Axios
- Vanilla CSS (no utility frameworks like Tailwind)

### Backend
- Python 3.13 (FastAPI)
- Prometheus Client for metrics
- Uvicorn as ASGI server

#### Endpoints

Here are some curl examples for every endpoint implemented.

To create a new admin use `POST /admins`
```sh
curl -X 'POST' \
  'http://localhost:3004/admins' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "username",
    "email": "mail@example.com",
    "password": "securepassword"
  }'
```

To get a list of all the admins in the system use `GET /admins`
```sh
curl -X GET "http://localhost:3004/admins" \
  -H 'Content-Type: application/json'
```

To get a certain admin use `GET /admins/:id`
```sh
curl -X GET "http://localhost:3004/admins/{id}" \
  -H 'Content-Type: application/json'
```

To delete a certain admin use `DELETE /admins/:id`
```sh
curl -X DELETE \
  "http://localhost:3004/admins/{id}" \
  -H 'Content-Type: application/json'
```

To login admins: 
```sh
curl --location 'http://localhost:3004/admins/login' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "admin123@example.com",
  "password": "securepassword"
}
'
```

### DevOps
- Docker & Docker Compose
- Prometheus
- Grafana

## 🚀 Getting Started

### Prerequisites
- Docker
- Docker Compose

### Clone the repository

```bash
git clone https://github.com/your-org/classconnect-backoffice.git
cd classconnect-backoffice
```

### Run the entire stack

```bash
docker-compose up --build
```

Visit:

- 🌐 Frontend: http://localhost:5173  
- 🔙 Backend API: http://localhost:8000  
- 📈 Prometheus: http://localhost:9090  
- 📊 Grafana: http://localhost:3000 (default login: `admin` / `admin`)

## 📁 Project Structure

```
classconnect-backoffice/
├── backend/            # FastAPI app
├── frontend/           # React admin panel
├── prometheus/         # Prometheus config
├── grafana/            # Grafana dashboards (optional)
└── docker-compose.yml  # Docker orchestration
```

## ✍️ License

MIT License.
