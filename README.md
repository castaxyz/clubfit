# ClubFit - Gestión de Miembros (Arquitectura Hexagonal)

Este proyecto es una implementación académica de un sistema de gestión de miembros para un gimnasio ("ClubFit"), desarrollado bajo los principios de **Arquitectura Hexagonal**.

## Requisitos del Taller
- **Funcionalidad Total (CRUD):** Gestión completa de miembros (Crear, Listar, Obtener, Actualizar/Renovar, Eliminar).
- **Regla de Negocio:** Beneficio de `MES_BONIFICADO` si el miembro tiene más de 12 meses de antigüedad al renovar.
- **Arquitectura Hexagonal:** Aplicación de separación estricta entre Dominio, Aplicación e Infraestructura.

## Estructura de Capas (Mapping)
La arquitectura hexagonal se mapea de la siguiente manera:

1.  **DOMINIO (Núcleo):**
    - `app/domain/entities/`: Entidades de negocio (`Member`) y sus reglas.
    - `app/domain/ports/`: Interfaces (Puertos) que definen el contrato de persistencia.
2.  **APLICACIÓN (Casos de Uso):**
    - `app/application/use_cases/`: Casos de uso que orquestan el negocio (Crear, Listar, Actualizar, Eliminar, Renovar).
3.  **INFRAESTRUCTURA (Adaptadores):**
    - **Entrada (Input):** Flask (Adaptador para recibir peticiones HTTP).
    - **Salida (Output):** SQLAlchemy (Adaptador para persistencia en base de datos).

## Patrones de Diseño Aplicados
- **Repository Pattern:** Desacopla la lógica de negocio del acceso a datos.
- **Dependency Injection:** Inyección de dependencias en los casos de uso para invertir el control.
- **Adapter Pattern:** Flask y SQLAlchemy conectan el núcleo con tecnologías externas.

## Instalación y Ejecución
1. Clonar el repositorio.
2. Crear entorno virtual: `python -m venv venv`.
3. Activar entorno: `source venv/bin/activate`.
4. Instalar dependencias: `pip install -r requirements.txt`.
5. Ejecutar: `python run.py`.

## Documentación de la API (CRUD Completo)

Comandos `cURL` verificados para probar toda la funcionalidad:

### 1. Crear un Miembro (Create)
```bash
curl -X POST http://127.0.0.1:5000/members \
     -H "Content-Type: application/json" \
     -d '{"id": 2, "name": "Ana Perez"}'
```

### 2. Listar todos los Miembros (Read All)
```bash
curl -X GET http://127.0.0.1:5000/members
```

### 3. Obtener un Miembro por ID (Read One)
```bash
curl -X GET http://127.0.0.1:5000/members/2
```

### 4. Actualizar un Miembro (Update)
Actualiza el nombre del miembro.
```bash
curl -X PUT http://127.0.0.1:5000/members/2 \
     -H "Content-Type: application/json" \
     -d '{"name": "Ana Maria Perez"}'
```

### 5. Renovar Membresía (Business Logic)
Regla: +30 días base. Si antigüedad > 12 meses, +30 días adicionales de bonificación.
```bash
curl -X POST http://127.0.0.1:5000/members/2/renew
```

### 6. Eliminar un Miembro (Delete)
```bash
curl -X DELETE http://127.0.0.1:5000/members/2
```
