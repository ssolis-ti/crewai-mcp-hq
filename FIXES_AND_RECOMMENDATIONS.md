# CrewAI MCP - Fixes & Optimization Recommendations

## 🔧 Issues Fixed

### 1. **Interactive CLI Blocking Issue** ✅
**Problem**: El servidor MCP levantaba un CLI interactivo de CrewAI que esperaba entrada del usuario, evitando que los agentes ejecuten herramientas correctamente.

**Root Cause**: Los subprocesos invocados desde MCP (stdio transport) no tenían `stdin=subprocess.DEVNULL`, permitiendo que CrewAI esperara entrada interactiva.

**Solution Applied**:
```python
subprocess.run(
    cmd,
    cwd=project_path,
    capture_output=True,
    text=True,
    check=False,
    stdin=subprocess.DEVNULL,  # ← AGREGADO AQUÍ
)
```

**Files Modified**:
- `src/crewai_mcp/tools/observability.py` - 3 funciones (test, train, replay)
- `src/crewai_mcp/tools/flow_orchestration.py` - 2 funciones (plot, run)
- `src/crewai_mcp/tools/knowledge_memory.py` - 1 función (reset-memories)
- `src/crewai_mcp/tools/project_management.py` - 2 funciones (install, extra packages)

---

### 2. **Flow Execution Refactored** ✅
**Problem**: `crewai_flow_run()` usaba CLI (`crewai run`), inconsistente con `crewai_kickoff()`.

**Solution**: Reescrito para usar **Python API directa**:

**Before** (CLI-based):
```python
result = subprocess.run(["crewai", "run"], ...)
```

**After** (API-based):
```python
flow_instance = FlowClass()
result = flow_instance.kickoff(inputs=inputs)
```

**Benefits**:
- ✅ No CLI bloqueante
- ✅ Coherencia con `crewai_kickoff()`
- ✅ Mejor manejo de errores
- ✅ Soporte para inputs parametrizados

---

## 📋 Verificación & Testing

Para validar los cambios:

```bash
# 1. Activar entorno
cd c:\Users\P0zcl\Desktop\cwai-mcp
.\.venv\Scripts\Activate.ps1

# 2. Ejecutar servidor MCP
python -m crewai_mcp.server

# 3. Probar en tu asistente IA (Claude, Gemini, etc.)
# - Crear un proyecto: crewai_create_project("test_flow", "flow")
# - Ejecutar con herramientas: crewai_kickoff("test_flow", {"topic": "AI agents"})
```

---

## 🚀 Recomendaciones Adicionales

### A. Mejorar Documentación de Herramientas
Agregar a [README.md](README.md):
```markdown
### Non-Interactive Execution
When running under MCP (stdio transport), all subprocess calls use `stdin=subprocess.DEVNULL` 
to prevent interactive prompts. Flows and Crews execute via Python API, not CLI.
```

### B. Agregar Timeouts
Para subprocesos que pueden tardar:
```python
subprocess.run(
    cmd,
    ...,
    timeout=300,  # 5 minutos máximo
    stdin=subprocess.DEVNULL,
)
```

### C. Mejor Manejo de Errores para Herramientas
Crear un wrapper para consistencia:
```python
def _run_subprocess_safely(cmd, cwd, timeout=120):
    """Ejecuta subprocess con stdin=DEVNULL y manejo de errores."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
            check=False,
        )
        return result
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(cmd)}")
        raise
```

### D. Validar Herramientas en Agentes
Asegurarse que los agentes tengan herramientas definidas:
```python
# En agents.yaml:
researcher:
  role: "Research Agent"
  goal: "Find information"
  backstory: "Expert researcher"

# En crew.py:
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=[SerperDevTool(), WebsiteSearchTool()],  # ← IMPORTANTE
        verbose=True
    )
```

### E. Logueo Mejorado
Agregar logs detallados para debugging:
```python
logger.info(f"Kickoff inputs: {inputs}")
logger.debug(f"Agent tools: {agent.tools}")
logger.info(f"Crew result type: {type(result)}")
```

---

## 🧪 Testing Workflow

### Test 1: Basic Project Execution
```python
# Usar crewai_create_project para crear uno nuevo
project = "test_crew"
inputs = {"topic": "AI Safety", "current_year": "2026"}
result = crewai_kickoff(project, inputs)
assert "successful" in result.lower() or len(result) > 0
```

### Test 2: Flow Execution
```python
# Crear un flow project
project = "test_flow"
inputs = {"topic": "Machine Learning"}
result = crewai_flow_run(project, inputs)
assert "successful" in result.lower() or len(result) > 0
```

### Test 3: Multi-Agent Crews
```python
# Asegurar que todos los agentes ejecutan con herramientas
project = "complex_crew"
inputs = {"query": "research AI trends", "max_depth": 3}
result = crewai_kickoff(project, inputs)
# Validar que se usaron herramientas (buscar en el output)
```

---

## 🔍 Debugging Tips

Si aún ves problemas:

### 1. Verificar stderr
```python
logger.error(f"STDERR: {result.stderr}")
```

### 2. Validar estructura de proyecto
```bash
ls -la workspace/test_demo/src/test_demo/
# Debe tener: agents.yaml, tasks.yaml, crew.py
```

### 3. Test de importación
```python
import sys
sys.path.insert(0, r"C:\path\to\project\src")
from test_demo.crew import TestDemo
crew_obj = TestDemo()
crew_obj.load_configurations()
print(crew_obj.agents)  # Validar que carga agentes
```

### 4. Revisar logs del servidor
El MCP server loguea a stderr:
```bash
# Desde VS Code o terminal
# Ver salida del servidor en la consola
```

---

## ✅ Checklist Post-Fix

- [x] Todos los subprocess.run() tienen `stdin=subprocess.DEVNULL`
- [x] `crewai_flow_run()` usa API Python
- [x] Funciones de observability no bloquean stdin
- [ ] Testing en múltiples asistentes IA (Claude, Gemini, etc.)
- [ ] Documentación actualizada
- [ ] Changelog actualizado
- [ ] Versión incrementada si es necesario

---

## 📚 Referencias

- [CrewAI Documentation](https://docs.crewai.com/)
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)

---

**Última actualización**: 2026-06-07
