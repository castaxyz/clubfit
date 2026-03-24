# ClubFit - Gestión de Miembros (Arquitectura Hexagonal + UI)

Este proyecto es una implementación de un sistema de gestión de miembros para un gimnasio ("ClubFit"), desarrollado bajo los principios de **Arquitectura Hexagonal**. Incluye una interfaz web para pruebas rápidas y visualización de respuestas JSON.

## Requisitos del Taller
- **Funcionalidad Total (CRUD):** Gestión completa de miembros.
- **Regla de Negocio:** Beneficio de `MES_BONIFICADO` si el miembro tiene más de 12 meses de antigüedad al renovar.
- **Arquitectura Hexagonal:** Aplicación de separación estricta entre Dominio, Aplicación e Infraestructura.

## Estructura de Capas (Mapping)
La arquitectura sigue el principio de inversión de dependencias: la infraestructura depende de la aplicación mediante la implementación de los puertos, pero la aplicación no depende de detalles técnicos.
1.  **DOMINIO:** Entidades (Member) y lógica de negocio.
2.  **APLICACIÓN:** Casos de uso que orquestan el negocio y definen los puertos (interfaces de entrada y salida).
3.  **INFRAESTRUCTURA:** Adaptadores de Entrada (Flask + HTML) y Salida (SQLAlchemy).

## Instalación y Ejecución
1. Crear entorno virtual: `python -m venv venv`.
2. Activar entorno: `source venv/bin/activate`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Ejecutar: `python run.py`.

## Interfaz de Exploración (UI)
Acceda a la raíz del proyecto en su navegador para usar el **API Explorer**:
- **URL:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Documentación de la API (Endpoints & cURL)

### 1. Listar todos los Miembros
```bash
curl -X GET http://127.0.0.1:5000/members
```

### 2. Crear un Miembro
**Nota:** Los campos `id`, `name`, `email` y `phone` son obligatorios.
```bash
curl -X POST http://127.0.0.1:5000/members \
     -H "Content-Type: application/json" \
     -d '{
       "id": 10, 
       "name": "Julian Casablancas", 
       "email": "julian@thestrokes.com", 
       "phone": "555-9876"
     }'
```

### 3. Obtener un Miembro por ID
```bash
curl -X GET http://127.0.0.1:5000/members/10
```

### 4. Actualizar Datos de un Miembro
```bash
curl -X PUT http://127.0.0.1:5000/members/10 \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Julian C. Updated", 
       "email": "julian_new@mail.com",
       "phone": "555-0000"
     }'
```

### 5. Renovación y Regla de Negocio (Bono)
Este endpoint extiende la membresía por 30 días. Si el miembro tiene más de 12 meses de antigüedad, se otorgan 30 días adicionales de regalo (`MES_BONIFICADO`).
```bash
curl -X POST http://127.0.0.1:5000/members/10/renew
```

### 6. Eliminar un Miembro
```bash
curl -X DELETE http://127.0.0.1:5000/members/10
```

---

## Escenarios de Prueba para Validación de Negocio

### Escenario A: Miembro Nuevo (Sin Bono)
```bash
# 1. Crear miembro actual
curl -X POST http://127.0.0.1:5000/members -H "Content-Type: application/json" \
     -d '{"id": 101, "name": "Carlos Nuevo", "email": "carlos@mail.com", "phone": "111"}'

# 2. Renovar (Debe dar 30 días normales)
curl -X POST http://127.0.0.1:5000/members/101/renew
```

### Escenario B: Miembro Antiguo (Con Bono "MES_BONIFICADO")
Usamos `join_date` para simular que el miembro se unió hace más de un año.
```bash
# 1. Crear miembro con fecha de 2024
curl -X POST http://127.0.0.1:5000/members -H "Content-Type: application/json" \
     -d '{
       "id": 999, 
       "name": "Ana Antigua", 
       "email": "ana@mail.com", 
       "phone": "222", 
       "join_date": "2024-01-01T10:00:00"
     }'

# 2. Renovar (Debe aplicar MES_BONIFICADO: +60 días en total)
curl -X POST http://127.0.0.1:5000/members/999/renew
```
