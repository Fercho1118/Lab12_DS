# Lab 12 — Guía para completar la versión 2 en Windows

## 1. Estado real y archivos preparados

Se revisaron el enunciado, la imagen del reparto, `planificacion.md`, las tablas y las definiciones
de informe contenidas en `observatorio_v1.pbix`. La versión 1 tiene las páginas Panorama y Verificación
del avance; V1 ya utiliza la jerarquía Año › Trimestre › MesNombre. No se modificó el binario.

| Preparado desde este entorno | Falta ejecutar en Power BI Desktop |
|--|--|
| Secciones 4.3 y 4.5 en `diseno.md`, apartados 9 y 10 | Ajustar el texto si la implementación final difiere |
| `powerbi/medidas_v2.dax`: medidas nuevas compatibles con los nombres documentados en v1 | Ejecutarlas, agregarlas al modelo y configurar formatos |
| `powerbi/verificar_v2.dax`: 16 casos con referencias calculadas desde los CSV | Ejecutar y comprobar que todos den `Correcto = TRUE` |
| Campos, interacciones, marcadores y lista de revisión de esta guía | Construir V3–V9, navegación y detalle; guardar `_v2.pbix` |
| 11 pruebas Python aprobadas sobre los datos | Revisar aspecto, filtros, regreso, apertura y actualización del `.pbix` |

No se puede abrir Power BI Desktop ni ejecutar su motor DAX en este entorno macOS. Los archivos DAX
son preparación de implementación, **no evidencia de medidas ejecutadas**. No se entrega un `.pbix`
modificado sin poder comprobarlo. El PDF final y las pruebas comparativas corresponden a la integración
de Nicolás; aquí no se inventan capturas, horas trabajadas ni resultados de esas pruebas.

## 2. Abrir, guardar copia y agregar las medidas

1. Coordinar que nadie más esté editando el `.pbix`. Abrir `powerbi/observatorio_v1.pbix` en
   Power BI Desktop para Windows, versión 2.159 o compatible con la del avance.
2. **Guardar como** `powerbi/observatorio_v2.pbix`; conservar v1 intacto.
3. Si vas a actualizar: Inicio → Transformar datos → Editar parámetros → `RutaDatos`.
   Usar la ruta local absoluta a `powerbi\data\`, terminada en `\`. Aplicar y Actualizar.
   No cambiar tipos `en-US`, claves ni relaciones. Ver `powerbi_avance.md`.
4. Abrir **Vista de consultas DAX**, crear consulta y pegar `powerbi/medidas_v2.dax` completo.
   Ejecutar para comprobar que se acepta la consulta. Después usar **Actualizar modelo con cambios**
   o **Agregar nueva medida** sobre cada definición. Ejecutar sin actualizar no guarda las medidas.
   El `EVALUATE` final solo muestra un mensaje: la verificación numérica se hace en el siguiente paso.
5. Abrir otra consulta, pegar `powerbi/verificar_v2.dax` y ejecutar. Esperar 16 filas con
   `Correcto = TRUE`. Guardar la salida/captura en `docs/lab12/evidencia/` al terminar.
   Si falla una fila, no cambiar el esperado para aprobar: revisar medida, tipo y relaciones.
6. Formatear las medidas: visitantes y errores absolutos con separador de miles y 0 decimales;
   índices con 1 decimal; `Peso país sobre extranjeros` como porcentaje con 1 decimal.
   No formatear el índice 130 como porcentaje: significa 30 % sobre el mes promedio.

Las medidas se agregan a la tabla `Medidas` existente. No se reemplazan las fórmulas del avance.
Los archivos usan comas como separadores DAX y punto decimal; si tu instalación exige separadores
localizados, revisar esa opción de Desktop antes de pegar, sin reemplazar comas dentro de textos.

## 3. Montaje de páginas y gráficos

Reutilizar tema, tipografía y tamaños de v1. No poner las nueve vistas en un solo lienzo. Redimensionar
V1 y V2 en Panorama para dar espacio a V3, sin hacer ilegibles los ejes. Renombrar cada objeto en
el panel Selección con su ID V1–V9 para facilitar las pruebas.

| Página / vista | Visual y campos | Medida y configuración |
|--|--|--|
| Panorama / V1 | Conservar columnas apiladas, `dim_fecha[Jerarquía fecha]` y leyenda `dim_frontera[Vía]` | `[Llegadas]`; comprobar las flechas de bajar/subir nivel existentes |
| Panorama / V2 | Conservar líneas, X `dim_fecha[MesNombre]`, leyenda Vía | `[Llegadas año en foco]`, título existente |
| Panorama / V3 | Barras horizontales, Y `dim_mercado[Mercado]` | `[Llegadas mercados en foco]`; Top N 10 por esa medida, aplicar filtro y ordenar descendente; título por formato condicional `[Título V3]` |
| Mercados / V5 | Treemap, jerarquía `dim_pais[Región]` → `dim_pais[País]` | `[Llegadas extranjeras]`; activar drill down/up; no reemplazar el país por el mercado |
| Mercados / V6 | Barras horizontales apiladas, Y `dim_frontera[Punto]`, leyenda `dim_frontera[Vía]` | `[Llegadas extranjeras]`; ordenar descendente |
| Estacionalidad / V7 | Matriz: filas `dim_fecha[Año]`, columnas `dim_fecha[MesNombre]` | `[Índice estacional]`; quitar subtotales/totales, formato de fondo secuencial 60–140; mostrar elementos sin datos y aclarar que 2026 no tiene año completo; no convertir blancos en cero |
| Estacionalidad / V8 | Líneas, X `dim_fecha[MesNombre]` | `[Índice año en foco]` y `[Perfil mediana]`; banda desde `[Perfil mínimo]` a `[Perfil máximo]`, asociada a la mediana |
| Pronósticos / V4 | Líneas, X `dim_fecha[Fecha]` **sin jerarquía automática**, eje continuo | Cuatro medidas en Y: `[Observado una serie]`, `[Predicción ARIMA]`, `[Predicción Holt-Winters]`, `[Predicción Seasonal Naive]`; no agregar `dim_modelo` como leyenda adicional |
| Pronósticos / V9 | Columnas agrupadas, X `dim_fecha[MesNombre]`, leyenda `dim_modelo[Modelo]` | `[MAE período visible]`; tooltip `[Error firmado medio]` y `[Meses visibles de evaluación]`; eje desde cero |

`MesNombre` ya debe estar ordenado por `Mes`, no alfabéticamente. Vías: Aérea azul `#0072B2`,
Terrestre naranja `#E69F00`, Marítima verde `#009E73`. V4: observado `#1E2A38`, ARIMA `#6A3D9A`,
Holt-Winters `#CC79A7`, Seasonal Naive `#8C8C8C`, con trazos distintos. Fijar colores por serie;
no confiar únicamente en el orden de aparición del tema.

**Banda de V8:** panel Analítica → Barras de error → Por campo. Asociar a `Perfil mediana`, límite
inferior `Perfil mínimo`, superior `Perfil máximo`, relación **Absoluta**, mostrar banda de relleno
neutro claro. No usar porcentaje ni distancia relativa. Si la versión instalada no permite esa banda
con dos medidas, mostrar mínimo y máximo como líneas finas junto con mediana y año en foco, y
documentar esa adaptación. Es rango histórico, no intervalo de confianza ni caja de cuartiles.

**Tabla de modelos (no cuenta como gráfica):** `dim_modelo[Modelo]`, `[MAE]`, `[RMSE]`, `[MAPE]`,
`[Meses evaluados]`. Orden ascendente por MAE. Título: «Evaluación completa: abr-2021 a jun-2026,
63 meses». Bajo V9: «Error absoluto medio de los meses visibles». No ocultar la diferencia de horizonte.
Aviso: «Modelos entrenados hasta marzo de 2021, durante la pandemia; subestiman la recuperación.
Son referencias de comparación, no pronósticos oficiales».

## 4. Segmentadores e interacciones

| Página | Vista inicial del marcador Restablecer |
|--|--|
| Panorama | Año sin filtro; vías Aérea y Terrestre; V1 en nivel Año; V2/V3 usan 2025 por la medida de v1 |
| Mercados y fronteras | Año 2025; todas las vías; V5 en raíz Región, sin selección |
| Estacionalidad | Vías Aérea y Terrestre; selector de año 2025 para V8; V7 mantiene todos los años |
| Pronósticos | Serie Total (selección única), tres modelos, rango completo 2009–junio 2026 |

- Usar `dim_fecha[Año]` en los selectores de Panorama y Mercados. No sustituirlo por `Fecha`:
  las medidas de año en foco de v1 detectan la columna Año. En Pronósticos sí usar `Fecha`, tipo Entre.
- No sincronizar segmentadores entre páginas. El selector de vía no corresponde a la página de
  modelos: allí el selector es Serie, y Total incluye todas las vías.
- En **Formato → Editar interacciones**, configurar V1 → V2 y V3 como **Filtrar**, no Ninguno.
  Probar clic real en una columna; un clic en un segmento apilado también puede seleccionar la vía.
  El segmentador Año permite elegir el año conservando varias vías.
- Configurar V5 → V6 como **Filtrar**. Probar una región y luego un país. No basta con que ambos
  respondan al mismo segmentador. Dejar V6 → V5 en Ninguno para que el ranking no cambie el universo.
- En Estacionalidad, el segmentador Año filtra V8 y el mensaje de perfil, **no V7**. V7 ↔ V8 en
  Ninguno: seleccionar una celda no debe reducir la curva a un mes. El selector Vía filtra ambos.
  La mediana y la banda usan la historia completa de las vías elegidas, sin 2020–2021 ni años incompletos.
- En Pronósticos, Serie y Modelo filtran V4, V9 y la tabla; Fecha filtra V4/V9. La tabla permanece
  fija por diseño del modelo. Desactivar clics V9 → tabla/V4 y tabla → V4/V9; evitar cambiar de
  horizonte o modelo accidentalmente. El rango se controla con el segmentador.

Power BI normalmente interpreta limpiar un segmentador como seleccionar todos sus valores. No
esperar el comportamiento de «ninguna vía marcada» de Dash. Comprobar el estado sin datos con
Marítima y año 2025, no desmarcando todo.

## 5. Navegación, mensajes y regreso

1. Insertar → Botones → Navegador de páginas en las cuatro páginas principales. Mostrar solo
   Panorama, Mercados y fronteras, Estacionalidad y Pronósticos. Resaltar el estado Seleccionado.
   Ocultar Verificación del avance y Detalle de país del navegador, sin borrar la verificación.
2. Agregar segmentadores y una tarjeta de texto `[Selección de llegadas]` en Panorama/Mercados;
   `[Estado llegadas]` como ayuda. En Estacionalidad usar `[Estado perfil]`, y rotular el selector
   «Año de la línea; calendario y banda conservan historia». En Pronósticos, `[Estado pronósticos]`.
   Estos elementos no cuentan entre las ocho gráficas.
3. Para cada página, establecer su vista inicial de la tabla anterior, borrar selecciones de gráficos
   y volver al nivel superior de jerarquías. Vista → Marcadores → Agregar:
   `Inicio_Panorama`, `Inicio_Mercados`, `Inicio_Estacionalidad`, `Inicio_Pronosticos`.
   Activar Datos, Mostrar y Página actual; aplicar a todos los objetos de esa página. Actualizar
   el marcador después de configurar el estado. Un marcador de otra página no sirve como reset local.
4. Insertar botón «Restablecer», acción Marcador, enlazado al marcador de **esa** página.
   Probar tras filtrar y hacer drill down. En modo edición, usar Ctrl+clic para ejecutar botones.
5. Crear «Detalle de país», página oculta. En el área Drillthrough agregar `dim_pais[País]` y activar
   Mantener todos los filtros. Incluir tarjeta `[Llegadas extranjeras]`, `[Peso país sobre extranjeros]`,
   líneas por `dim_fecha[MesNombre]` y ranking por `dim_frontera[Punto]` con `[Llegadas extranjeras]`.
   Agregar botón Volver con acción **Atrás**, no un marcador a Panorama.
6. Entrar desde V5 en el nivel País: clic derecho sobre El Salvador → Obtener detalles → Detalle de
   país. V3 representa **mercados**, no países; no habilitar este detalle inventando una relación
   Mercado–País. Volver debe regresar a Mercados con su contexto; Restablecer debe volver a la raíz.

El drillthrough hereda Región si se entró desde Centroamérica. La medida de peso elimina el filtro
de país **y región del denominador**, pero conserva año/vías: El Salvador debe representar 47.2 %
de todos los extranjeros de 2025, no su proporción únicamente dentro de Centroamérica.

## 6. Revisión antes de entregar v2

- [ ] `verificar_v2.dax`: 16 resultados correctos. No se da por aprobado aquí: requiere ejecución en Desktop.
- [ ] V1–V6, V8 y V9 presentes: ocho gráficas sin contar V7, tarjetas ni tabla de métricas.
- [ ] Clic en V1 cambia V2/V3; clic en V5 cambia V6; capturas antes/después.
- [ ] Drill down/up de V1 y V5 funcional; al regresar se identifica el nivel activo.
- [ ] Detalle de El Salvador conserva año/vía y vuelve mediante Atrás.
- [ ] Restablecer en cada página elimina selecciones y recupera el estado documentado.
- [ ] Marítima 2025 muestra ayuda sin dibujar ceros; V8 en 2026 no inventa un índice de año completo.
- [ ] Pronósticos no suma varias series; ocultar un modelo oculta su curva sin duplicar lo observado.
- [ ] Tabla de métricas rotulada como 63 meses; V9 identifica su rango y cantidad de meses efectivos.
- [ ] Leyendas, ejes, colores y foco seleccionado legibles al tamaño real; orden de tabulación y
  textos alternativos de los gráficos revisados en el panel Formato/General.
- [ ] Guardar, cerrar, volver a abrir `_v2.pbix` y comprobar actualización con la nueva `RutaDatos`.
- [ ] Registrar horas **reales** en `planificacion.md`; guardar capturas en `docs/lab12/evidencia/`
  y avisar al siguiente integrante antes de editar el binario de nuevo.

Referencias numéricas de los CSV: terrestres 2025, diciembre 238,290 y septiembre 147,654;
El Salvador 2025, 1,582,844.620768 y 47.2168 % de extranjeros; Valle Nuevo, 39.2883 % de ese país;
Holt-Winters Aérea en julio, MAE 60,048.1682822. Para los indicadores del protocolo: aéreas 2025,
1,188,971; MAE Total ARIMA, 154,494.16500384128. No son tiempos ni resultados de una prueba de UI.

## 7. Rúbrica y alcance pendiente

| Criterio | Preparación disponible | Lo que falta comprobar en Windows |
|--|--|--|
| Diseño y facilidad de uso · 25 puntos | Paleta del avance, estados iniciales, mensajes, navegación y justificación | Aspecto, legibilidad, selección activa y regreso |
| Visualización e interacción · 35 puntos | Especificación V1–V9 y medidas preparadas | Ocho gráficas reales, enlaces, detalle y tres modelos funcionales |
| Comparación · 20 puntos | Protocolo existente, sin modificar resultados esperados | Pruebas en ambas herramientas, tiempos, matriz, costos y recomendaciones: siguiente integrante |
| Funcionamiento y reproducibilidad · 20 puntos | CSV consistentes, 11 pruebas aprobadas e instrucciones de carga | DAX ejecutado, `.pbix` final abierto y fuentes actualizadas sin errores |

No se puede certificar desde aquí la rúbrica completa ni la entrega del avance. No se necesita
Power BI Service, licencia de pago, prueba de licencia ni publicación web. El requisito 3.4 permite
jerarquía **o** detalle contextual, pero el reparto acordó ambos, por lo que esta guía conserva ambos.

Documentación oficial consultada el 6-nov-2026:
- Microsoft. [Vista de consultas DAX y actualización del modelo](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view).
- Microsoft. [Panel Analítica: barras y bandas de error por campo](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-analytics-pane).
