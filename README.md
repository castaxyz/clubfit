# ClubFit - Gestión de Miembros (Arquitectura Hexagonal)

Este proyecto es una implementación académica de un sistema de gestión de miembros para un gimnasio ("ClubFit"), desarrollado bajo los principios de **Arquitectura Hexagonal**.

## Requisitos del Taller
- **Funcionalidad Total (CRUD):** Gestión completa de miembros.
- **Regla de Negocio:** Beneficio de `MES_BONIFICADO` si el miembro tiene más de 12 meses de antigüedad al renovar.
- **Arquitectura Hexagonal:** Aplicación de separación estricta entre Dominio, Aplicación e Infraestructura.

## Estructura de Capas (Mapping)
1.  **DOMINIO:** Entidades (`Member`) y Puertos (Interfaces de Repositorio).
2.  **APLICACIÓN:** Casos de uso que orquestan el negocio.
3.  **INFRAESTRUCTURA:** Adaptadores de Entrada (Flask) y Salida (SQLAlchemy).

## Patrones de Diseño Aplicados
- **Repository Pattern:** Abstracción de la base de datos.
- **Dependency Injection:** Inversión de control en los casos de uso.
- **Adapter Pattern:** Conexión con Flask y SQLAlchemy.
- **Factory Method:** Creación de entidades con lógica de negocio inicial.

## Instalación y Ejecución
1. Crear entorno virtual: `python -m venv venv`.
2. Activar entorno: `source venv/bin/activate`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Ejecutar: `python run.py`.

## Documentación de la API (CRUD Básico)

### 0. Crear un miembro
```bash
curl -X POST http://127.0.0.1:5000/members \
     -H "Content-Type: application/json" \
     -d '{"id": 10, "name": "Julian Casablancas", "email": "julian@casablancas.com", "phone": "12345678"}'
```

### 1. Listar todos los Miembros
```bash
curl -X GET http://127.0.0.1:5000/members
```

### 2. Obtener un Miembro por ID
```bash
curl -X GET http://127.0.0.1:5000/members/10
```

### 3. Actualizar Datos de un Miembro (Nombre)
```bash
curl -X PUT http://127.0.0.1:5000/members/10 \
     -H "Content-Type: application/json" \
     -d '{"name": "Julian C. Updated", "email": "julian_new@casablancas.com"}'
```

### 4. Eliminar un Miembro
```bash
curl -X DELETE http://127.0.0.1:5000/members/10
```

## Escenarios de Prueba (Validación de Regla de Negocio)

Para validar la lógica de antigüedad (>12 meses), usamos el campo `join_date` (migración de datos).

### Paso A: Crear Miembros con diferentes antigüedades
```bash
# Miembro Nuevo (Antigüedad: 0 días)
curl -X POST http://127.0.0.1:5000/members -H "Content-Type: application/json" -d '{"id": 101, "name": "Carlos Nuevo", "email": "carlos@mail.com", "phone": "111111"}'

# Miembro Antiguo (Antigüedad: > 2 años)
curl -X POST http://127.0.0.1:5000/members -H "Content-Type: application/json" -d '{"id": 999, "name": "Ana Antigua", "email": "ana@mail.com", "phone": "222222", "join_date": "2024-01-01T10:00:00"}'
```

### Paso B: Probar Renovación y Validar Bono
```bash
# Caso 1: Miembro 101 -> Recibirá +30 días (Normal)
curl -X POST http://127.0.0.1:5000/members/101/renew

# Caso 2: Miembro 999 -> Recibirá +60 días (Bono Aplicado)
curl -X POST http://127.0.0.1:5000/members/999/renew
```
