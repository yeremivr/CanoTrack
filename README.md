# 🐕‍🦺 CanoTrack — Simulador y Analítica de Carreras de Canódromo

> Sistema de consola en **Python** para gestionar un canódromo: registro de perros,
> generación de carreras con simulación de velocidades y un **panel estadístico**
> con gráficos. Proyecto académico enfocado en **Programación Orientada a Objetos**
> y análisis de datos.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![POO](https://img.shields.io/badge/Paradigma-POO-success)
![pandas](https://img.shields.io/badge/pandas-data-150458?logo=pandas&logoColor=white)
![matplotlib](https://img.shields.io/badge/matplotlib-charts-11557c)

---

## ✨ Características

- **Registro de perros** con validación de datos (nombre, pista, raza, velocidad base).
- **Dos tipos de competidor** (`Perro_Mediano`, `Perro_Grande`) con cálculo de
  velocidad diferenciado.
- **Generación de carreras**: simula la velocidad final de cada perro, ordena por
  distancia y determina al ganador.
- **Persistencia en CSV**: perros y carreras se guardan y se recargan entre sesiones.
- **Panel estadístico** con `matplotlib`: velocidad promedio, distancia máxima,
  victorias por perro y porcentaje de victorias.

## 🧠 Conceptos de POO demostrados

| Concepto | Dónde |
|----------|-------|
| **Abstracción** | Clase abstracta `Perro(ABC)` con `@abstractmethod calcular_velocidad_final()` |
| **Herencia** | `Perro_Mediano` y `Perro_Grande` heredan de `Perro` |
| **Encapsulamiento** | Atributos privados con `@property` y *setters* |
| **Polimorfismo** | Cada raza redefine el cálculo de velocidad (`super()` + *override*) |
| **Composición** | `Canodromo` gestiona listas de `Perro` y `Carrera` |

## 🛠️ Tecnologías

- **Python 3.10+** (usa `match/case`)
- **pandas** — lectura/escritura de CSV y agregaciones (`groupby`, `iterrows`)
- **matplotlib** — visualización de estadísticas

## 📁 Estructura

```
CanoTrack/
├── canodromo.py          # Aplicación (clases + menú de consola)
├── archivo_perros.csv    # Datos persistentes de perros
├── archivo_carreras.csv  # Datos persistentes de carreras
└── README.md
```

## ▶️ Cómo ejecutar

```bash
# 1) Instalar dependencias
pip install pandas matplotlib

# 2) Ejecutar
python canodromo.py
```

Al iniciar verás un menú:

```
1. Registrar perros al sistema
2. Mostrar perros registrados
3. Registrar y generar carrera
4. Mostrar información de carrera específica
5. Mostrar todos los gráficos de carreras y perros 📈
6. Mostrar carreras registradas
7. Salir
```

## 📊 Estadísticas

La opción **5** abre un panel con cuatro gráficos (`matplotlib`): velocidad promedio
por perro, distancia máxima alcanzada, victorias por perro y porcentaje de victorias.

---

## 📝 Nota

Proyecto desarrollado en el marco del curso de **Programación Orientada a Objetos**.
Publicado como parte de mi portafolio académico.

## 👤 Autor

**Yeremi Tanner Villavicencio Ríos** · [github.com/yeremivr](https://github.com/yeremivr)
