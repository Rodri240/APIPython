# APIPython

REST API en Python para registrar pedidos, consultar productos, procesar pagos y notificar al cliente cuando un pedido queda pagado.

## Requisitos

- Python 3.11+ (probado con 3.12)

## Instalación

1. Crear entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

- `http://127.0.0.1:8000`
- Documentación Swagger: `http://127.0.0.1:8000/docs`

## Ejecutar pruebas

```bash
python -m unittest discover -s tests -v
```

## Endpoints principales

- `GET /products` → lista productos.
- `POST /orders` → crea un pedido y calcula total.
- `GET /orders/{order_id}` → consulta un pedido.
- `POST /orders/{order_id}/payments` → valida/confirmar pago, actualiza pedido a pagado y dispara notificación.