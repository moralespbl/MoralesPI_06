***

# 📊 Dashboard de Análisis Educativo - Operativo Aprender

Este proyecto es una herramienta de Business Intelligence diseñada para procesar y visualizar los microdatos del operativo nacional **Aprender**. Permite cruzar factores sociales con el rendimiento académico real en Matemática y Lengua.

## 📂 Origen de los Datos
Los microdatos utilizados en este análisis son públicos y fueron obtenidos de la **Secretaría de Educación de la Nación Argentina**:
- **Fuente:** [Datos Abiertos - Secretaría de Educación](https://www.argentina.gob.ar/educacion/evaluacion-e-informacion-educativa/datos-abiertos-de-la-secretaria-de-educacion)
- **Procesamiento:** Los archivos originales fueron depurados, filtrados y convertidos a formato **Pickle (.pkl)** para optimizar la performance del dashboard.

---

## 🚀 Cómo Ejecutar la Aplicación

1. **Instalar Dependencias:** Abrir la terminal y ejecutar:
   ```bash
   pip install pandas matplotlib streamlit
   ```
2. **Configurar el Archivo de Datos:** Asegurarse de que el archivo `df_nacional.pkl` esté en la ruta:
   `df_nacional.pkl`
3. **Lanzar el Dashboard:** Desde la terminal, ejecutar:
   ```bash
   streamlit run app_proyecto.py
   ```

---

## 📖 Manual de Operación y Ejemplos

La interfaz permite realizar análisis dinámicos mediante los filtros laterales:

### 1. Configuración de Filtros
* **Jurisdicción:** Seleccionar una provincia específica (ej. **Jujuy**) para un análisis local o **"Todas"** para el promedio nacional.
* **Materia:** Elegir entre Matemática, Lengua o la comparativa de ambas.

### 2. Ejemplos de Variables de Contexto
El sistema permite cruzar el desempeño con preguntas clave del cuestionario del alumno. Algunos ejemplos que podés analizar son:
* **`ap20c` (Hacer deportes):** Analizar si la actividad física regular se correlaciona con mejores niveles de desempeño.
* **`ap35` (Uso de tecnología):** Observar cómo impacta el acceso a dispositivos digitales en los resultados de aprendizaje.
* **`ap12` (Horas de estudio):** Cuantificar la relación entre el tiempo dedicado fuera del aula y el éxito en las evaluaciones.

---

**Autor:** Pablo - Analista de Datos

***


