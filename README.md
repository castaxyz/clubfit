# ClubFit - Gestión de Miembros (Arquitectura Hexagonal)

Este proyecto es una implementación académica de un sistema de gestión de miembros para un gimnasio ("ClubFit"), desarrollado bajo los principios de **Arquitectura Hexagonal**.

## Requisitos del Taller
- **Funcionalidad Total (CRUD):** Gestión completa de miembros (Crear, Listar, Obtener, Actualizar/Renovar, Eliminar).
- **Regla de Negocio:** Beneficio de `MES_BONIFICADO` si el miembro tiene más de 12 meses de antigüedad al renovar.
- **Arquitectura Hexagonal:** Separación estricta entre Dominio, Aplicación e Infraestructura.

## Estructura de Capas (Mapping)
La arquitectura hexagonal se mapea de la siguiente manera en el proyecto:

1.  **DOMINIO (Núcleo):**
    - `app/domain/entities/`: Definición de entidades de negocio (`Member`) y reglas de renovación.
    - `app/domain/ports/`: Interfaces (Puertos de Salida) que definen cómo se comunica el dominio con el exterior (`MemberRepository`).
2.  **APLICACIÓN (Casos de Uso):**
    - `app/application/use_cases/`: Orquestación de la lógica de negocio (`MemberUseCases`). Aquí se coordina el uso de puertos y entidades.
3.  **INFRAESTRUCTURA (Adaptadores):**
    - **Entrada (Input):** `app/infrastructure/adapters/input/` (Controladores Flask que exponen la API).
    - **Salida (Output):** `app/infrastructure/adapters/output/` (Implementación de persistencia con SQLAlchemy).
    - **Persistencia:** `app/infrastructure/persistence/` (Modelos de base de datos y configuración).

## Patrones de Diseño Aplicados
- **Repository Pattern:** Desacopla la lógica de negocio de la implementación específica de la base de datos (SQLAlchemy).
- **Dependency Injection:** Los casos de uso reciben sus dependencias (repositorio) a través del constructor, facilitando el testing y la inversión de dependencias.
- **Adapter Pattern:** Los controladores (Flask) y los repositorios (SQLAlchemy) actúan como adaptadores que conectan el mundo exterior con el corazón de la aplicación.

## Instalación y Ejecución
1. Clonar el repositorio.
2. Crear entorno virtual: `python -m venv venv`.
3. Activar entorno: `source venv/bin/activate` (Linux).
4. Instalar dependencias: `pip install -r requirements.txt`.
5. Ejecutar: `python run.py`.

## Documentación de la API (Endpoints & cURL)

### 1. Crear Miembro
**POST** `/members`
```bash
curl -X POST http://127.0.0.1:5000/members \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "name": "Carlos Gomez"}'
```

### 2. Listar Miembros
**GET** `/members`
```bash
curl -G http://127.0.0.1:5000/members
```

### 3. Obtener Miembro por ID
**GET** `/members/<id>`
```bash
curl -G http://127.0.0.1:5000/members/1
```

### 4. Renovar Membresía (Regla de Negocio)
**POST** `/members/<id>/renew`
*Aplica +30 días base, o +60 días si el miembro tiene >12 meses de antigüedad.*
```bash
curl -X POST http://127.0.0.1:5000/members/1/renew
```

### 5. Eliminar Miembro
**DELETE** `/members/<id>`
```bash
curl -X DELETE http://127.0.0.1:5000/members/1
```
