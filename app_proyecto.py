import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CARGAR Y NORMALIZAR EL DATASET ---
@st.cache_data
def cargar_datos_analisis():
    # Leer archivo serializado desde la ruta local especificada
    ruta = "df_nacional.pkl"
    try:
        df = pd.read_pickle(ruta)
        # Eliminar espacios residuales en nombres de provincias
        if 'jurisdiccion' in df.columns:
            df['jurisdiccion'] = df['jurisdiccion'].str.strip()
        return df
    except Exception as e:
        st.error(f"Error al acceder al archivo .pkl: {e}")
        st.stop()

df_nacional = cargar_datos_analisis()

# --- 2. DEFINIR ESTRUCTURAS DE CONTROL (DICCIONARIOS) ---

# Mapear descripciones del cuestionario a prefijos de columna
diccionario_variables = {
    "Código de Jurisdicción": "jurisdiccion",
    "departamento": "departamento",
    "Sector de Gestión": "sector",
    "Ámbito": "ambito",
    "¿En qué mes naciste?": "ap01_",
    "¿En qué año naciste?": "ap02_",
    "¿Cuál es el sexo que figura en tu DNI?": "ap03_",
    "¿En qué país naciste?": "ap04_",
    "¿Dónde nacieron tu papá, mamá o persona adulta responsable? [Mamá]": "ap05a_",
    "¿Dónde nacieron tu papá, mamá o persona adulta responsable? [Papá]": "ap05b_",
    "¿Dónde nacieron tu papá, mamá o persona adulta responsable? [Persona adulta responsable]": "ap05c_",
    "¿Tu mamá, papá o persona adulta responsable se reconoce de un pueblo índigena u originario o descendiente de una familia indígena u originaria?": "ap06_",
    "¿Tu mamá, papá o persona adulta responsable se reconoce afrodescendiente o tiene antepasados negros o afrodescendientes?": "ap07_",
    "Queremos conocer más del lugar donde vivís. Por lo general, ¿dónde dormís más días?": "ap10_",
    "En donde vivís, ¿cuántas habitaciones para dormir hay en total?": "ap11_",
    "Contándote a vos, ¿con cuántas personas vivís?": "ap12_",
    "¿Con quién o quiénes vivís? [Mamá]": "ap13a_",
    "¿Con quién o quiénes vivís? [Papá]": "ap13b_",
    "¿Con quién o quiénes vivís? [Pareja de mi mamá o papá]": "ap13c_",
    "¿Con quién o quiénes vivís? [Hijo(s)]": "ap13d_",
    "¿Con quién o quiénes vivís? [Hermano(s)]": "ap13e_",
    "¿Con quién o quiénes vivís? [Tío(s)]": "ap13f_",
    "¿Con quién o quiénes vivís? [Abuelo(s)]": "ap13g_",
    "¿Con quién o quiénes vivís? [Novia o novio]": "ap13h_",
    "¿Con quién o quiénes vivís? [Amistades]": "ap13i_",
    "¿Con quién o quiénes vivís? [Otra(s) persona(s)]": "ap13j_",
    "¿Tenés hijo(s)?": "ap14_",
    "En donde vivís, ¿tenés un espacio tranquilo para estudiar?": "ap15_",
    "En donde vivís, ¿hay estos objetos o servicios? [Servicio de streaming por suscripción (Netflix, Amazon, Disney+, otros)]": "ap16a_",
    "En donde vivís, ¿hay estos objetos o servicios? [Canilla con agua potable (apta para el consumo)]": "ap16b_",
    "En donde vivís, ¿hay estos objetos o servicios? [Lavarropas]": "ap16c_",
    "En donde vivís, ¿hay estos objetos o servicios? [Heladera con freezer]": "ap16d_",
    "En donde vivís, ¿hay estos objetos o servicios? [Televisor]": "ap16e_",
    "En donde vivís, ¿hay estos objetos o servicios? [Celular propio]": "ap16f_",
    "En donde vivís, ¿hay estos objetos o servicios? [Computadora (computadora de escritorio, laptop, netbook, etc.)]": "ap16g_",
    "En donde vivís, ¿hay estos objetos o servicios? [Tablet]": "ap16h_",
    "En donde vivís, ¿hay estos objetos o servicios? [Lector de libros digitales (ebook)]": "ap16i_",
    "En donde vivís, ¿hay estos objetos o servicios? [Consola de videojuegos (PlayStation, Nintendo Wii, Xbox, PC Gamer, otras)]": "ap16j_",
    "En donde vivís, ¿hay estos objetos o servicios? [Conexión a internet]": "ap16k_",
    "En donde vivís, ¿hay estos objetos o servicios? [Baño en el interior del lugar donde vivís]": "ap16l_",
    "En donde vivís, ¿cuántos baños hay?": "ap17_",
    "Quienes viven con vos, ¿tienen auto?": "ap18_",
    "Aproximadamente, ¿cuántos libros hay en el lugar donde vivís? (pueden ser libros de poesía, cuentos, novelas, manuales escolares, diccionarios, enciclopedias, etc. en papel)": "ap19_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Aprender idiomas]": "ap20a_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Leer en formato papel libros, cómics, diarios, revistas, etc. que no sean los que me pidieron leer en la escuela]": "ap20b_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Leer en formato digital libros, cómics, diarios, revistas, etc. que no sean los que me pidieron leer en la escuela]": "ap20c_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Participar de un taller de escritura, literario y/o periodístico]": "ap20d_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Escribir ficción, notas, novelas, cuentos u otros]": "ap20e_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Ir a eventos culturales (cine, teatro, recital, museo, etc.)]": "ap20f_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Hacer actividades deportivas, físicas o de relajación]": "ap20g_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Hacer actividades artísticas (dibujo, música, danza, canto, teatro, etc.)]": "ap20h_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Participar de actividades comunitarias o solidarias (en comedores, asistencia a personas mayores, acciones religiosas, etc.)]": "ap20i_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Asistir a fiestas, bailes o boliches]": "ap20j_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Crear contenido para redes sociales (por ejemplo, subir videos a Tiktok)": "ap20k_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Jugar juegos online u offline (en la computadora, tablet o celular))": "ap20l_",
    "En el último mes, durante tu tiempo libre, ¿hiciste lo siguiente? [Realizar actividades relacionadas a la programación, robótica, etc.)": "ap20m_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Tareas como hacer las compras, limpiar, lavar platos o ropa, o cocinar en el lugar donde vivís]": "ap21a_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Cuidar a alguien de tu familia sin ayuda de un adulto]": "ap21b_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Llevar o buscar a alguien de tu familia a la escuela u otros lugares, sin ayuda de un adulto]": "ap21c_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Ayudar a construir o hacer arreglos en el lugar donde vivís]": "ap21d_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Buscar agua o leña, cosechar la huerta o cuidar u ordeñar animales de granja o campo]": "ap21e_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Trabajar por cuenta propia]": "ap22a_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Trabajar para un empleador]": "ap22b_",
    "La semana pasada, ¿hiciste estas actividades?, ¿por cuánto tiempo? [Trabajar en el emprendimiento familiar o ayudar a familiares en su trabajo]": "ap22c_",
    "¿Recibiste dinero por hacer las actividades del cuadro anterior?": "ap23_",
    "¿Fuiste al jardín de infantes?, ¿desde qué sala?": "ap24_",
    "¿Repetiste de grado alguna vez?, ¿en qué ciclo escolar? [Primaria]": "ap25a_",
    "¿Repetiste de grado alguna vez?, ¿en qué ciclo escolar? [Secundaria: Ciclo Básico ]": "ap25b_",
    "¿Repetiste de grado alguna vez?, ¿en qué ciclo escolar? [Secundaria: Ciclo Orientado]": "ap25c_",
    "¿Tenés materias previas?": "ap26_",
    "En lo que va del año, ¿cuántas faltas tenés?": "ap27_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Problemas de salud propios]": "ap28a_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Problemas de salud de algún familiar]": "ap28b_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Problemas de acceso a la escuela (debido al clima o al transporte)]": "ap28c_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [No tenía ganas de ir a la escuela]": "ap28d_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Tenía que ayudar con las tareas del hogar]": "ap28e_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Tenía que cuidar a alguna persona de la familia]": "ap28f_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Estaba cursando un embarazo]": "ap28g_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Estaba con mi periodo menstrual]": "ap28h_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Estaba de vacaciones o de viaje]": "ap28i_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Estaba trabajando]": "ap28j_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Por llegar tarde]": "ap28k_",
    "¿Cuáles fueron las tres razones principales por las que acumulaste faltas? [Otro motivo]": "ap28l_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Auto o moto]": "ap29a_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Remis, taxi, Uber, Cabify u otras aplicaciones]": "ap29b_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Colectivo]": "ap29c_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Transporte escolar]": "ap29d_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Bicicleta]": "ap29e_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Tren o subterráneo]": "ap29f_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Caminando]": "ap29g_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Lancha, bote u otro]": "ap29h_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Caballo o mula]": "ap29i_",
    "Habitualmente, ¿cuáles son los dos medios que más usás para ir a la escuela? [Otros medios]": "ap29j_",
    "Aproximadamente, ¿cuánto tiempo tardás en llegar a la escuela?": "ap30_",
    "La semana pasada, fuera del horario escolar, aproximadamente, ¿cuánto tiempo estudiaste o hiciste tarea para la escuela?": "ap31_",
    "Según tu opinión...[¿Cómo leés?]": "ap32a_",
    "Según tu opinión...[¿Cómo escribís un texto?]": "ap32b_",
    "Según tu opinión...[¿Cómo resolvés los problemas que tienen cálculos matemáticos?]": "ap32c_",
    "Según tu opinión...[¿Cómo resolvés los problemas de geometría (construir figuras, etc.)? ]": "ap32d_",
    "En tu escuela...[¿Hay normas o acuerdos de convivencia?]": "ap33a_",
    "En tu escuela...[¿Son conocidas las normas o acuerdos de convivencia?]": "ap33b_",
    "En tu escuela...[¿Los estudiantes participan en la construcción de las normas o acuerdos de convivencia?]": "ap33c_",
    "En tu escuela, ¿hay organización estudiantil?, ¿qué forma de organización hay? [Sí, hay Centro de estudiantes]": "ap34a_",
    "En tu escuela, ¿hay organización estudiantil?, ¿qué forma de organización hay? [Sí, hay delegados por curso]": "ap34b_",
    "En tu escuela, ¿hay organización estudiantil?, ¿qué forma de organización hay? [Sí, hay otra forma de organización estudiantil]": "ap34c_",
    "En tu escuela, ¿hay organización estudiantil?, ¿qué forma de organización hay? [No, no hay organización estudiantil]": "ap34d_",
    "En tu escuela, ¿hay organización estudiantil?, ¿qué forma de organización hay? [No sé]": "ap34e_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Compañeros de curso]": "ap35a_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Estudiantes de otros cursos]": "ap35b_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Profesores]": "ap35c_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Preceptores]": "ap35d_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Equipo directivo]": "ap35e_",
    "Por lo general, ¿cómo es tu relación con las diferentes personas de la escuela? [Auxiliares (portero, personal de maestranza)]": "ap35f_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [Te molestaron o dejaron de lado]": "ap36a_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [En redes sociales, te amenazaron, agredieron o dijeron mentiras sobre vos]": "ap36b_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [De forma física o verbal, te amenazaron, agredieron o dijeron mentiras sobre vos]": "ap36c_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [Te sacaron tus cosas o las rompieron]": "ap36d_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [Trataste mal a algún compañero]": "ap36e_",
    "Durante este año, ¿viviste alguna de las siguientes situaciones con personas de tu escuela? [Viste alguna situación donde agredieran a algún compañero]": "ap36f_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Calificaciones]": "ap37a_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Lugar en el que naciste]": "ap37b_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Situación socioeconómica de tu familia]": "ap37c_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Discapacidad]": "ap37d_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Religión]": "ap37e_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Intereses y gustos]": "ap37f_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Aspectos físicos]": "ap37g_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Vestimenta]": "ap37h_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Orientación sexual]": "ap37i_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Por reconocerte o descender de un pueblo indígena (por ejemplo: Mapuche, Kolla, Toba, Wichi, Diaguita, Guaraní, Qom, otro) ]": "ap37j_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [Otros motivos]": "ap37k_",
    "¿Por cuáles de los siguientes motivos te molestan o discriminan? [No me molestan ni discriminan en la escuela]": "ap37l_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se habla con profesores, preceptores o directores]": "ap38a_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se comunican con las familias]": "ap38b_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se hacen charlas o talleres para reflexionar]": "ap38c_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Interviene el Equipo de Orientación Escolar]": "ap38d_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se hacen actividades reparadoras, colaborativas o comunitarias]": "ap38e_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se aborda en los espacios de participación (Consejo de aula, Consejo de convivencia, etc.) ]": "ap38f_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Se aplican sanciones]": "ap38g_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [No se le da importancia y se deja pasar ]": "ap38h_",
    "Cuando en tu curso hay un problema de convivencia, ¿cuáles son las tres formas más habituales que usan en tu escuela para resolverlo? [Otra forma]": "ap38i_",
    "¿Sentís que en tu escuela pasa lo siguiente? [Podés contarle a tus profesores o preceptores lo que te pasa]": "ap39a_",
    "¿Sentís que en tu escuela pasa lo siguiente? [Tus profesores o preceptores se preocupan por saber cómo te sentís]": "ap39b_",
    "¿Sentís que en tu escuela pasa lo siguiente? [Los profesores, preceptores o directores te dan contención y te acompañan cuando lo necesitás]": "ap39c_",
    "¿Sentís que en tu escuela pasa lo siguiente? [Los directores de la escuela te escuchan cuando lo necesitás]": "ap39d_",
    "¿Usás las siguientes redes sociales? [WhatsApp]": "ap40a_",
    "¿Usás las siguientes redes sociales? [TikTok]": "ap40b_",
    "¿Usás las siguientes redes sociales? [Instagram]": "ap40c_",
    "¿Usás las siguientes redes sociales? [Threads]": "ap40d_",
    "¿Usás las siguientes redes sociales? [Facebook]": "ap40e_",
    "¿Usás las siguientes redes sociales? [Messenger]": "ap40f_",
    "¿Usás las siguientes redes sociales? [X-Twitter]": "ap40g_",
    "¿Usás las siguientes redes sociales? [YouTube]": "ap40h_",
    "¿Usás las siguientes redes sociales? [Snapchat]": "ap40i_",
    "¿Usás las siguientes redes sociales? [Twitch]": "ap40j_",
    "¿Usás las siguientes redes sociales? [Discord]": "ap40k_",
    "¿Usás las siguientes redes sociales? [Telegram]": "ap40l_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Aceptás en las redes sociales a personas que no conocés]": "ap41a_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Hablás con desconocidos en línea]": "ap41b_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Hacés amigos nuevos por las redes sociales, aplicaciones o juegos online]": "ap41c_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Bloqueás a contactos desconocidos]": "ap41d_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Cambiás las opciones de privacidad de las aplicaciones ]": "ap41e_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Ponés privacidad a tus fotos y videos]": "ap41f_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Compartís información personal (datos personales o familiares, fotos, etc.)]": "ap41g_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Recibís consejos de personas adultas sobre cómo cuidarte en las redes sociales, aplicaciones o juegos on-line]": "ap41h_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Tenés límite de horario para el uso del celular, computadora o tablet ]": "ap41i_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Alguien de tu familia conoce o supervisa lo que hacés cuando usás celular, computadora o tablet ]": "ap41j_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [En tus dispositivos tenés alguna aplicación de control parental]": "ap41k_",
    "Cuando usás dispositivos (celular, computadora o tablet), ¿pasa lo siguiente? [Participás en juegos de apuestas]": "ap41l_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Cansancio, falta de energía y sensación de agotamiento]": "ap42a_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Sensación de nerviosismo acompañado de miedo y respiración acelerada]": "ap42b_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Dolores de cabeza acompañado de falta de concentración]": "ap42c_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Tristeza acompañada de miedo, falta de confianza en vos y pensamientos negativos]": "ap42d_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [. Sentimiento de soledad acompañado de irritabilidad y tristeza]": "ap42e_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Dificultad para conciliar el sueño por cambios en los horarios de la rutina]": "ap42f_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Bienestar personal acompañado de entusiasmo y seguridad en vos]": "ap42g_",
    "¿En los últimos tres meses, tuviste durante un tiempo o en forma continua los estados de ánimo mencionados en el siguiente cuadro? [Conductas que afectan a la alimentación]": "ap42h_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Trabajar]": "ap43a_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Continuar estudios superiores (universitario o no universitario)]": "ap43b_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Hacer cursos de capacitación laboral (electricidad, peluquería, manicuría, de huerta, artesanías, del área de construcciones, etc.)]": "ap43c_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Ayudar a mi familia con las tareas del hogar]": "ap43d_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Producir contenidos para las redes sociales]": "ap43e_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Jugar videojuegos para generar dinero]": "ap43f_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Realizar trabajos solidarios o comunitarios (participación en comedores, asistencia a personas mayores, acciones religiosas, etc.)]": "ap43g_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Desarrollar un emprendimiento personal o familiar]": "ap43h_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Desarrollar otras actividades (viajar, hacer deportes, actividades artísticas, etc.)]": "ap43i_",
    "Al finalizar el secundario, ¿qué proyectos inmediatos tenés? [Aún no lo decidí]": "ap43j_",
    "¿Sentís que tu familia apoya tus proyectos a futuro y te ayuda en la toma de decisiones?": "ap44_",
    "Nivel Lengua": "ldesemp_",
    "Nivel Matemática": "mdesemp_",
    "Edad hasta el 30 de junio": "edadA_",
    "Sobreedad": "sobreedad_",
    "Migración": "migracion_",
    "Repitencia": "repitencia_",
    "Clima Escolar": "clima_",
    "NSE por quintiles": "NSE_",
    "Máximo nivel educativo madre": "Nivel_Ed_Madre_",
    "Máximo nivel educativo padre": "Nivel_Ed_Padre_",
    "Máximo nivel educativo adulto responsable": "Nivel_Ed_Persona_Resp_"
}

# Extraer valores únicos de jurisdicción para el filtrado dinámico
provincias_disponibles = sorted(df_nacional['jurisdiccion'].unique().tolist())

# --- 3. PROCESAMIENTO ESTADÍSTICO Y GENERACIÓN DE VISUALES ---

def generar_grafico_desempeño(df, variable_txt, materia_opt=None, juris_opt=None):
    # Recuperar el selector de columna desde el diccionario de variables
    selector = diccionario_variables.get(variable_txt)
    if not selector: return None

    # Definir vectores de columnas de desempeño por área
    cols_mat = ['mdesemp_Por_debajo_del_nivel_básico', 'mdesemp_Básico', 'mdesemp_Satisfactorio', 'mdesemp_Avanzado']
    cols_len = ['ldesemp_Por_debajo_del_nivel_básico', 'ldesemp_Básico', 'ldesemp_Satisfactorio', 'ldesemp_Avanzado']
    niveles_label = [c.split('_', 1)[1].replace('_', ' ') for c in cols_mat]

    # Aplicar segmentación geográfica según selección
    if juris_opt and juris_opt != "Todas":
        df_segmento = df[df['jurisdiccion'] == juris_opt].copy()
        contexto_geo = juris_opt
    else:
        df_segmento = df.copy()
        contexto_geo = "Total País"

    # Localizar columnas de respuesta asociadas al selector
    cols_pregunta = [c for c in df.columns if c.startswith(selector)]

    def tabular_materia(df_input, area, columnas_desemp):
        # Filtrar registros específicos de la materia
        sub = df_input[df_input['materia'] == area].copy()
        # Forzar conversión a numérico para garantizar operaciones aritméticas
        for c in columnas_desemp + cols_pregunta:
            sub[c] = pd.to_numeric(sub[c], errors='coerce').fillna(0)
            
        dict_acumulado = {}
        for col in cols_pregunta:
            # Acumular factores de expansión para respuestas positivas (> 0)
            dict_acumulado[col] = sub[sub[col] > 0][columnas_desemp].sum().values
            
        return pd.DataFrame(dict_acumulado, index=niveles_label).T

    # Consolidar dataframes de las materias requeridas
    lista_resultados = []
    materias_target = [materia_opt] if materia_opt else ["Matematica", "Lengua"]

    for m in materias_target:
        config_cols = cols_mat if m == "Matematica" else cols_len
        df_res = tabular_materia(df_segmento, m, config_cols)
        
        if not df_res.empty and df_res.sum().sum() > 0:
            tag = "MAT" if m == "Matematica" else "LEN"
            # Limpiar etiquetas del eje vertical eliminando el código técnico
            df_res.index = [f"{i.replace(selector, '')} ({tag})" for i in df_res.index]
            lista_resultados.append(df_res)

    # Construir objeto visual final
    if lista_resultados:
        df_final = pd.concat(lista_resultados).sort_index(ascending=False)
        
        # Calcular dimensiones del canvas según volumen de datos
        fig, ax = plt.subplots(figsize=(12, max(5, len(df_final) * 0.55)))
        
        # Ejecutar renderizado de barras horizontales apiladas (ancho 0.4)
        df_final.plot(kind='barh', stacked=True, ax=ax, colormap='Spectral', width=0.4)
        
        # Aplicar formato estético y títulos dinámicos
        ax.set_title(f"Distribución de Desempeño: {variable_txt}\n({contexto_geo})", fontsize=14, pad=15)
        ax.legend(title="Nivel", bbox_to_anchor=(1.02, 1), loc='upper left')
        ax.set_xlabel("Población (Suma de Factores de Expansión)")
        
        plt.tight_layout()
        return fig
    return None

# --- 4. INTERFAZ DE USUARIO (STREAMLIT) ---

st.title("📊 Dashboard Analítico - Evaluación Aprender")
st.sidebar.header("Filtros de Datos")

# Configurar selectores dinámicos en barra lateral
juris_pick = st.sidebar.selectbox("Jurisdicción", ["Todas"] + provincias_disponibles)
var_pick = st.sidebar.selectbox("Variable de Cuestionario", list(diccionario_variables.keys()))
mat_pick = st.sidebar.radio("Materia Seleccionada", ["Ambas", "Matematica", "Lengua"])

# Traducir selección de radio a parámetro de función
materia_param = None if mat_pick == "Ambas" else mat_pick

# Procesar y mostrar visualización
if st.sidebar.button("Actualizar Gráfico"):
    fig_output = generar_grafico_desempeño(
        df_nacional, 
        var_pick, 
        materia_opt=materia_param, 
        juris_opt=juris_pick
    )
    
    if fig_output:
        st.pyplot(fig_output)
    else:
        st.warning("No se detectaron registros válidos (Desempeño > 0) para la combinación de filtros seleccionada.")