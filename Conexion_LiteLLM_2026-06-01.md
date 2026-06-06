# Datos de Conexión y Endpoints - LiteLLM Proxy

**Fecha de Generación:** 1 de junio de 2026
**Ubicación del Servicio:** Servidor Local (Docker)
**Última Verificación General de Modelos:** 1 de junio de 2026 (15 de 20 modelos operativos)

Este documento contiene las credenciales, rutas y estados actualizados de los modelos del proxy de LiteLLM configurado en el servidor local.

---

## 🔗 1. Credenciales y Servidor Base

- **Base URL (Endpoint Raíz):** `http://localhost:4000`
  *(Usa la IP de tu máquina en la red local si te conectas desde otro dispositivo, ej. `http://192.168.1.X:4000`)*
- **API Key (Master):** `sk-1234`
- **Puerto expuesto:** `4000`

---

## 🛤️ 2. Endpoints Principales (Compatibles con OpenAI)

Para configurar cualquier cliente que pida "URL de la API" (como AnythingLLM, n8n, etc.), debes usar la URL base o la ruta de chat correspondiente.

| Acción | Método HTTP | URL Completa |
| :--- | :--- | :--- |
| **Generación de Chat (Chat Completions)** | `POST` | `http://localhost:4000/v1/chat/completions` |
| **Listar Modelos Disponibles** | `GET` | `http://localhost:4000/v1/models` |
| **Verificar Estado (Healthcheck)** | `GET` | `http://localhost:4000/health/liveliness` |

*Recuerda que todas las peticiones a `/v1/*` deben incluir el Header: `Authorization: Bearer sk-1234`*

---

## 🧪 3. Estado Actualizado y Testeo de Modelos (1 de junio de 2026)

Se realizó un testeo automático exhaustivo uno a uno consultando la API local. De los **20 modelos configurados**, **15 están 100% operativos** respondiendo con éxito (`OK`) y latencias mínimas.

### 🟢 Modelos Operativos y Recomendados (15 Modelos)
Estos modelos respondieron de forma exitosa e inmediata:

| Modelo | Proveedor de Backend | Latencia | Observaciones |
| :--- | :--- | :--- | :--- |
| `llama-3.3-70b-nim` | Nvidia NIM | ~0.10s | **Excelente velocidad y razonamiento general.** |
| `llama-4-maverick-nim` | Nvidia NIM | ~0.08s | **Excelente velocidad.** |
| `llama-4-scout` | Nvidia NIM | ~0.08s | **Excelente velocidad.** |
| `deepseek-v4-pro-nim` | Nvidia NIM | ~0.12s | **Muy recomendado para programación.** |
| `kimi-k2-thinking-nim` | Nvidia NIM | ~0.08s | **Modelo de razonamiento profundo.** |
| `qwen3-coder-480b-nim` | Nvidia NIM | ~0.25s | **Súper modelo para desarrollo/código.** |
| `glm-5.1` | Nvidia NIM | ~0.17s | **Funcional y estable.** |
| `nemotron-3-super-120b` | Nvidia NIM | ~0.28s | **Excelente modelo de gran tamaño.** |
| `nemotron-3-nano-reasoning` | Nvidia NIM | ~0.43s | **Modelo liviano con capacidad de razonamiento.** |
| `gemma-4-31b-it-free` | OpenRouter (Gratuito) | ~0.17s | **Excelente alternativa de Google.** |
| `glm-4.5-air-free` | OpenRouter (Gratuito) | ~0.19s | **Funcional y estable.** |
| `gpt-oss-120b-free` | OpenRouter (Gratuito) | ~0.20s | **Alternativa de código abierto masiva.** |
| `nemotron-3-super-120b-free` | OpenRouter (Gratuito) | ~0.07s | **Gran velocidad.** |
| `owl-alpha` | OpenRouter (Gratuito) | ~0.07s | **Modelo experimental rápido.** |
| `qwen` | OpenRouter (Gratuito) | ~0.05s | **Responde con tag `<think>` de razonamiento.** |

---

### ⚠️ Modelos No Operativos / Con Errores (5 Modelos)
Te recomendamos evitar el uso de los siguientes nombres por el momento debido a errores de API o congestión externa:

* **`gemma-4-31b-it-nim`** (Nvidia NIM) - *Timeout (10s)*: Los servidores de NIM para este modelo experimentaron congestión o tiempos de espera prolongados.
* **`qwen3-coder-free`** (OpenRouter) - *Timeout (10s)*: La capa gratuita de OpenRouter para este modelo se encuentra saturada.
* **`nvidia-nemotron-4-340b-instruct`** (Nvidia NIM) - *Error 404 (Not Found)*: El identificador del modelo ya no es válido en el backend de Nvidia NIM.
* **`deepseek-v4-flash-free`** (OpenRouter) - *Error 404 (Not Found)*: El identificador exacto del modelo no se encuentra en el catálogo actual de OpenRouter.
* **`glm-5.1-or`** (OpenRouter) - *Error 403 (Forbidden)*: Requiere autenticación diferente o fondos en la cuenta (ha dejado de pertenecer a la capa completamente gratuita).

---

## 📄 4. Ejemplo Práctico de Conexión (Python / Requests)

Puedes usar este script rápido para verificar la disponibilidad de cualquiera de los modelos recomendados:

```python
import requests

url = "http://localhost:4000/v1/chat/completions"
headers = {
    "Authorization": "Bearer sk-1234",
    "Content-Type": "application/json"
}

data = {
    "model": "llama-3.3-70b-nim",
    "messages": [
        {"role": "user", "content": "¡Hola! ¿Cómo estás?"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```
