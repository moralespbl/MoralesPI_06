***

# 📊 Dashboard de Análisis Educativo - Operativo Aprender

Este proyecto es una herramienta de Business Intelligence diseñada para procesar y visualizar los microdatos del operativo nacional **Aprender**. Permite cruzar factores sociales con el rendimiento académico real en Matemática y Lengua.

## 🚀 Cómo Ejecutar la Aplicación (Guía Rápida)

Para poner en marcha el dashboard en tu equipo local, seguí estos pasos:

1. **Instalar Dependencias:** Abrir la terminal en la carpeta del proyecto y ejecutar:
   ```bash
   pip install pandas matplotlib streamlit
   ```
2. **Preparar los Datos:** Asegurarse de que el archivo `df_nacional.pkl` se encuentre en la ruta:
   `df_nacional.pkl`
   *(O modificar la ruta en el código fuente si se movió el archivo).*
3. **Lanzar el Dashboard:** En la terminal, ejecutar el siguiente comando:
   ```bash
   streamlit run app_aprender.py
   ```
4. **Acceder:** El sistema abrirá automáticamente una pestaña en tu navegador (usualmente en `http://localhost:8501`).

---

## 📖 Manual de Operación de la Planilla

Una vez iniciada la interfaz, el análisis se realiza a través del panel lateral:

* **Configurar Jurisdicción:** Seleccionar una provincia específica (ej. **Jujuy**) para un análisis local o **"Todas"** para obtener el promedio ponderado nacional.
* **Elegir Variable de Contexto:** Seleccionar el factor del cuestionario que se desea investigar (ej. "Horas de estudio", "Uso de dispositivos"). El motor de búsqueda filtrará las columnas técnicas automáticamente.
* **Seleccionar Materia:** Elegir entre Matemática, Lengua o la comparativa de ambas en un mismo gráfico.
* **Generar Visualización:** Presionar el botón para procesar los datos. El gráfico mostrará barras horizontales donde el ancho de **0.4** garantiza una lectura clara de los niveles de desempeño.

---

## 📋 Conclusiones Técnicas para el Analista
* **Normalizar** los datos mediante factores de expansión para que los resultados representen a la población total y no solo a la muestra.
* **Optimizar** el rendimiento mediante el uso de archivos **Pickle (.pkl)**, permitiendo que el procesamiento de millones de registros sea instantáneo.
* **Identificar** tendencias: un mayor predominio de colores fríos (azul/verde) indica un desempeño satisfactorio/avanzado en relación a la variable de contexto elegida.
* **Detectar** inconsistencias en los datos para asegurar que las conclusiones del proyecto de grado se basen en información depurada.

---
**Autor:** Pablo - Analista de Datos

***

### 📝 Resumen para el "About" de GitHub
Dashboard interactivo para el análisis de microdatos del Operativo Aprender. Implementación de ETL y visualización estadística mediante factores de expansión y segmentación por jurisdicción.

### 💻 Comandos de Subida Final
1. `git init`
2. `git add .`
3. `git commit -m "Versión Final - Guía de ejecución incluida"`
4. `git branch -M main`
5. `git remote add origin https://github.com/tu-usuario/nombre-del-repo.git`
6. `git push -u origin main`
