# Simulador de Procesador con Pipeline, Caché e Interfaz de E/S

Proyecto final del curso **Arquitectura de Computadores** - Universidad Sergio Arboleda  
Desarrollado en Python por María Parra.

---

## 🎯 Objetivos del Proyecto

- Simular una arquitectura de procesador con pipeline de 5 etapas.
- Implementar manejo de hazards (stalling y forwarding).
- Simular memoria caché de mapeo directo.
- Incorporar I/O programada e interrupciones desde un dispositivo ficticio.
- Evaluar rendimiento usando benchmarks personalizados.

---

## 🧱 Estructura del Proyecto
ProyectoFinal-ARQ/
├── main.py                  # Punto de entrada del simulador
├── cpu/
│   ├── __init__.py
│   ├── isa.py               # Parser y definición de instrucciones
│   ├── pipeline.py          # Implementación del pipeline de 5 etapas
├── memory/
│   ├── __init__.py
│   ├── cache.py             # Simulación de caché de mapeo directo
├── io/
│   ├── __init__.py
│   ├── device.py            # Dispositivo ficticio de entrada (E/S)
│   ├── interrupt.py         # Controlador de interrupciones
├── tests/
│   ├── benchmark1.txt       # Benchmark de suma con memoria
│   ├── benchmark2.txt       # Benchmark con saltos condicionales
│   ├── benchmark3.txt       # Benchmark para stalling y forwarding
│   ├── benchmark4.txt       # Benchmark para simular interrupción


---

## 🚀 ¿Cómo ejecutar?

### 1. Clona el repositorio

git clone https://github.com/tu_usuario/simulador_cpu.git
cd simulador_cpu

### 2. Ejecuta el simulador

python3 main.py
Asegúrate de tener Python 3.10+ instalado.

## ⚙️ Cambiar el benchmark
Puedes editar main.py y cambiar la línea:

programa = cargar_programa("tests/benchmark1.txt")
por cualquier otro archivo de prueba disponible, como:

benchmark2.txt: Saltos condicionales

benchmark3.txt: Hazards

benchmark4.txt: Interrupciones

## 📝 Créditos
Desarrollado por María Parra
Curso: Arquitectura de Computadores
Docente: Oscar Andrés Arias
Universidad Sergio Arboleda, 2025-1
