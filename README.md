# ClassConnect Backoffice

**ClassConnect Backoffice** is the administrative and monitoring dashboard for the ClassConnect system. It provides tools for managing users, configuring access permissions, and monitoring the health and usage of services within the platform.

## 📚 Table of Contents

- [Features](<README#🔧 Features>)
- [Tech Stack](<README#🧱 Tech Stack>)
- [Getting Started](<README#🚀 Getting Started>)
- [Project Structure](<README#📁 Project Structure>)
- [License](<README#✍️ License>)
- [Codecov](README#codecov)

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

Here are some curl examples for some endpoints implemented.

To create a new admin use `POST /admins`
```sh
curl -X POST 'http://localhost:3004/admins' \
  -H 'Authorization: Bearer {token}' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "username",
    "email": "mail@example.com",
    "password": "securepassword"
  }'
```

To get a list of all the admins in the system use `GET /admins`
```sh
curl 'http://localhost:3004/admins' \
  -H 'Authorization: Bearer {token}'
```

To get a certain admin use `GET /admins/:id`
```sh
curl 'http://localhost:3004/admins/{id}' \
  -H 'Authorization: Bearer {token}'
```

To delete a certain admin use `DELETE /admins/:id`
```sh
curl -X DELETE 'http://localhost:3004/admins/{id}' \
  -H 'Authorization: Bearer {token}'
```

To login admins: 
```sh
curl -X POST 'http://localhost:3004/admins/login' \
  -H 'Authorization: Bearer {token}' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "admin123@example.com",
  "password": "securepassword"
}'
```

### DevOps
- Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites
- Docker
- Docker Compose

### Clone the repository

```bash
git clone <repo-url> backoffice
```

### Run the entire stack

```bash
docker compose up --build
```

Visit:

- 🌐 Frontend: http://localhost:5173  
- 🔙 Backend API: http://localhost:3004  

## 📁 Project Structure

```
classconnect-backoffice/
├── backend/            # FastAPI app
├── frontend/           # React admin panel
└── docker-compose.yml  # Docker orchestration
```

## ✍️ License

MIT License.

## Codecov

[![codecov](https://codecov.io/gh/IS2-Class-Connect/classconnect-backoffice/graph/badge.svg?token=6QwXr8HFIm)](https://codecov.io/gh/IS2-Class-Connect/classconnect-backoffice)
