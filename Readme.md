# Autores

Daniel Abad Fundora C411  
Anabel Benítez González C411  
Enzo Rojas D´toste C411  

# Descripción del Problema

Se requiere que dado dos documentos se prevea la probabilidad de plagio entre ambos, señalando las secciones donde este pudiera ocurrir.  

# Consideraciones

El idioma del texto contenidos en los documentos debe ser ```inglés```, y el formato debe ser ```.txt```  

## Especificaciones Visuales

Se suben dos archivos de texto, y se muestran ambos textos en paralelo con las secciones de plagio y temática señaladas usando rojo claro de fondo para el plagio y amarillo para la temática.  
Se cuenta con otra ventana que es para ver en específico los resultados por cada sección de un documento, comparados con las secciones del otro documento.

# Ejecutar el proyecto

La interfaz de usuario está desarrollada en Django, un framework de desarrollo web de alto nivel en Python.  

Antes de la primera ejecución deberá ejecutar en la dirección ```src/gui``` el siguiente comando:  

```python manage migrate```

Luego cada vez que se quiera correr el servidor:  

```python manage runserver```

**Nota**: Durante la primera ejecución se descargará de manera automática un modelo de ```Bert```, más adelante explicaremos que es.

# Informe de Desarrollo de Solución para Detección de Plagio entre Documentos

## Introducción

La detección de plagio es una tarea crítica en diversos ámbitos académicos y profesionales para asegurar la originalidad del contenido. Con el avance tecnológico, la automatización de este proceso se ha vuelto esencial. Este informe detalla el desarrollo de una solución innovadora para la detección de plagio entre documentos, utilizando técnicas avanzadas de procesamiento de lenguaje natural (NLP) y aprendizaje automático.

## Metodología

### Conversión de Texto a Vectores con spaCy

El primer paso en nuestra solución fue convertir el texto de los documentos en una forma numérica que pudiera ser procesada computacionalmente. Para esto, utilizamos spaCy, una biblioteca de NLP que ofrece capacidades de word embedding. El proceso de word embedding asigna a cada palabra un vector en un espacio multidimensional, donde palabras con significados similares tienen vectores cercanos entre sí.

```python
import spacy
nlp = spacy.load("en_core_web_md")
doc = nlp("Example text")
word_vectors = [token.vector for token in doc]
```

### Obtención del Vector Promedio del Documento

Inicialmente, calculamos el vector promedio de todos los vectores de palabras para representar el documento completo. Aunque esta técnica proporciona una primera aproximación para comparar documentos, pierde mucho contexto al promediar indiscriminadamente.

### Mejoras en la Representación Vectorial

#### Uso de N-gramas

Para capturar mejor el contexto, extendimos nuestra estrategia a n-gramas, unidades compuestas por secuencias de n palabras. Calculamos el vector de cada n-grama como el promedio de los vectores de sus palabras componentes, lo que nos permitió preservar más información contextual.

#### Reducción de Dimensionalidad con SVD

Posteriormente, aplicamos Descomposición en Valores Singulares (SVD) para eliminar los componentes menos significativos de la matriz de vectores, buscando concentrarnos en las características más relevantes de los textos.

#### Ponderación con TF-IDF

Implementamos una ponderación mediante TF-IDF (Frecuencia del Término - Inversa de la Frecuencia del Documento) para dar más importancia a los términos más relevantes en el documento. Esta mejora permitió que el vector promedio reflejara con mayor precisión la importancia relativa de cada palabra.

### Uso de Transformers para un Embedding Avanzado

Dado que las técnicas anteriores aún no alcanzaban la precisión deseada, recurrimos a Transformers, específicamente a BERT (Bidirectional Encoder Representations from Transformers). BERT es un modelo de PLN basado en la arquitectura de transformer, entrenado previamente en un amplio corpus de texto, que capta profundidades de contexto y semántica no alcanzadas por enfoques anteriores.

#### Implementación con BERT

Usando un modelo preentrenado de BERT, logramos obtener embeddings de texto de alta precisión, marcando un hito en la capacidad de distinguir entre textos plagiados y aquellos que simplemente tratan temas similares. BERT analiza el texto de forma bidireccional, lo que significa que el contexto de cada palabra se entiende completamente en relación con todas las otras palabras del texto, no solo las precedentes o subsiguientes.

### Detección de Plagio a Nivel de Oración

Para identificar específicamente las partes plagiadas de un texto, empleamos spaCy para segmentar el texto en oraciones. Luego, obtuvimos el embedding de cada oración usando BERT y aplicamos la similitud coseno para compararlas con las oraciones del otro documento. La similitud coseno mide cómo de similares son dos vectores en un espacio n-dimensional, lo que nos permite identificar coincidencias significativas a nivel de oración.

## Conclusión

El desarrollo de esta solución de detección de plagio subraya la importancia de los avances en PLN y aprendizaje automático. A través de un enfoque iterativo, mejorando desde promedios simples de word embedding hasta la implementación de tecnologías de vanguardia como BERT, hemos establecido un método altamente efectivo y preciso para identificar plagios. Este progreso no solo mejora la detección de plagio sino que también contribuye al campo del PLN, demostrando el potencial de las técnicas de modelado de lenguaje avanzadas para comprender y analizar el texto a un nivel profundamente contextualizado.

# Problemas y Soluciones

**Problema**: la precisión de detección correcta de plagio de este algoritmo es buena, pero por supuesto todavía hay margen de error.

**Solución**: a medida que avanza el tiempo se mejoran y surgen nuevas técnicas de **Machine Learning**, las cuales pudieran incorporarse a este proyecto para mejorar los resultados.

#

**Problema**: se trabaja el texto solo teniendo en cuenta los token, y su contexto, lo cual es efectivo pero no se analiza características especiales del lenguaje.

**Solución**: implementar heurísticas específicas para el lenguaje como por ejemplo: realizar un análisis sintáctico del texto, para extraer el sujeto, predicado, y complementos circunstanciales; y realizar comparaciones.

#

**Problema**: la detección de plagio por secciones se hace apartir de oraciones; si se toman dos o más oraciones y se plagean en una sola, puede llevar a una mala detección por parte del algoritmo.

**Solución**: este problema se intentó resolver usando una ventana deslizante por ambos textos, pero esto tiene una alta complejidad temporal por lo tanto no es factible, y se debe seguir buscando otra solución.
