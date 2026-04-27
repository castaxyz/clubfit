# ClubFit — Sistema de Gestión de Gimnasio

API REST para gestión de miembros y planes de entrenamiento, construida con **Arquitectura Hexagonal** (Ports & Adapters), Flask, PostgreSQL y Redis.

---

## Requisitos previos

- [Docker](https://www.docker.com/get-started) >= 24.x
- [Docker Compose](https://docs.docker.com/compose/) >= 2.x

---

## Levantar el entorno completo

```bash
# 1. Clonar el repositorio
git clone https://github.com/castaxyz/clubfit.git
cd clubfit

# 2. Levantar todos los servicios en segundo plano
docker-compose up -d

# 3. Verificar que los contenedores estén corriendo
docker-compose ps
```

Los servicios disponibles serán:

| Servicio | URL / Puerto |
|----------|-------------|
| API REST (Flask) | http://localhost:5000 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

```bash
# Ver logs del API
docker-compose logs -f web

# Ver logs del worker de vencimientos
docker-compose logs -f worker

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (borra la BD)
docker-compose down -v
```

---

## Arquitectura del sistema

```
┌──────────────────────────────────────────────────────┐
│                   Docker Compose                     │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌────────────────┐  │
│  │  web     │    │  worker  │    │   db           │  │
│  │  :5000   │    │(background│   │  PostgreSQL    │  │
│  │  Flask   │    │  worker) │    │  :5432         │  │
│  └────┬─────┘    └────┬─────┘    └───────┬────────┘  │
│       │               │                  │           │
│       └───────────────┼──── SQLAlchemy ──┘           │
│                       │                              │
│              ┌────────┴────────┐                     │
│              │     redis       │                     │
│              │     :6379       │                     │
│              └─────────────────┘                     │
└──────────────────────────────────────────────────────┘
```

### Capas de la Arquitectura Hexagonal

```
app/
├── domain/          # Entidades y lógica de negocio pura
├── application/     # Casos de uso + Puertos (interfaces)
│   ├── ports/
│   │   ├── input/   # Contratos de entrada (use cases)
│   │   └── out/     # Contratos de salida (repositorios, publisher)
│   └── use_cases/   # Implementaciones: MemberService, TrainingService, ExpiryService
└── infrastructure/  # Adaptadores técnicos
    └── adapters/
        ├── input/   # Flask controllers + RedisSubscriber
        └── output/  # SQLAlchemy repositories + RedisPublisher
```

---

## Documentación de la API

### Miembros

```bash
# Listar todos los miembros
curl http://localhost:5000/members

# Crear un miembro
curl -X POST http://localhost:5000/members \
     -H "Content-Type: application/json" \
     -d '{"id": 10, "name": "Julian Casablancas", "email": "julian@thestrokes.com", "phone": "555-9876"}'

# Obtener miembro por ID
curl http://localhost:5000/members/10

# Actualizar miembro
curl -X PUT http://localhost:5000/members/10 \
     -H "Content-Type: application/json" \
     -d '{"name": "Julian C. Updated", "email": "julian_new@mail.com", "phone": "555-0000"}'

# Renovar membresía (aplica MES_BONIFICADO si > 12 meses)
curl -X POST http://localhost:5000/members/10/renew

# Eliminar miembro
curl -X DELETE http://localhost:5000/members/10
```

### Planes de Entrenamiento

```bash
# Ver opciones disponibles (objetivos y niveles de actividad)
curl http://localhost:5000/training-plans/options

# Generar plan de entrenamiento
curl -X POST http://localhost:5000/training-plans \
     -H "Content-Type: application/json" \
     -d '{"member_id": 10, "weight_kg": 75, "height_cm": 175, "age": 28, "activity_level": "MODERATE", "goal": "LOSE_WEIGHT"}'

# Obtener plan por ID
curl http://localhost:5000/training-plans/1

# Planes de un miembro
curl http://localhost:5000/training-plans/member/10

# Eliminar plan
curl -X DELETE http://localhost:5000/training-plans/1
```

### Administración

```bash
# Disparar revisión manual de membresías vencidas
curl -X POST http://localhost:5000/admin/trigger-expiry-check
```

---

## Escenarios de prueba

### Miembro nuevo (sin bono)

```bash
curl -X POST http://localhost:5000/members -H "Content-Type: application/json" \
     -d '{"id": 101, "name": "Carlos Nuevo", "email": "carlos@mail.com", "phone": "111"}'

curl -X POST http://localhost:5000/members/101/renew
# Resultado: +30 días (sin bono)
```

### Miembro antiguo (con MES_BONIFICADO)

```bash
curl -X POST http://localhost:5000/members -H "Content-Type: application/json" \
     -d '{"id": 999, "name": "Ana Antigua", "email": "ana@mail.com", "phone": "222", "join_date": "2024-01-01T10:00:00"}'

curl -X POST http://localhost:5000/members/999/renew
# Resultado: +60 días (30 normales + 30 de bono MES_BONIFICADO)
```

---

## Ejecución sin Docker (desarrollo local)

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Requiere Redis corriendo localmente o via Docker:
docker run -d -p 6379:6379 redis:7-alpine

python run.py      # API en :5000
python worker.py   # Worker en proceso separado
```
