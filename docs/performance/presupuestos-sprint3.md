# Presupuestos de rendimiento — Sprint 3

## 1. Objetivo

Evaluar el rendimiento de las pantallas principales de GanadApp en el entorno desplegado en Render y contrastar los resultados obtenidos con los presupuestos definidos para el proyecto.

Las mediciones se realizaron sobre las rutas `/animales` y `/sanidad`, utilizando Chrome DevTools y Lighthouse en configuración Mobile.

## 2. Resultados de Lighthouse

| Métrica | Gestión de Animales | Sanidad |
|---|---:|---:|
| Performance | 61 | 84 |
| Best Practices | 96 | 96 |
| First Contentful Paint | 2,0 s | 1,7 s |
| Largest Contentful Paint | 3,6 s | 1,8 s |
| Total Blocking Time | 1.500 ms | 590 ms |
| Cumulative Layout Shift | 0 | 0 |
| Speed Index | 3,9 s | 2,1 s |

### 2.1. Evaluación

La pantalla de Sanidad cumple el objetivo de LCP inferior a 2,5 segundos, con un resultado de 1,8 segundos.

La pantalla de Gestión de Animales registra un LCP de 3,6 segundos, por encima del límite establecido. También presenta un TBT de 1.500 ms, mientras que Sanidad registra 590 ms. Estos resultados evidencian diferencias de rendimiento entre ambas pantallas.

Las dos pantallas obtuvieron un CLS de cero, por lo que no se detectaron desplazamientos acumulativos de diseño durante las mediciones.

Los resultados de Best Practices fueron de 96 puntos en ambas pantallas.

## 3. Presupuesto de JavaScript inicial

Se estableció un límite máximo de 200 KB gzip para el JavaScript inicial de cada pantalla.

La medición contempló los archivos JavaScript externos propios de GanadApp y los scripts integrados directamente en los documentos HTML. Se excluyeron los recursos inyectados por extensiones del navegador, ya que no forman parte de la aplicación.

### 3.1. Gestión de Animales

| Recurso | Tamaño |
|---|---:|
| `auth.js` | 1,8 KB |
| Scripts integrados, sin comprimir | 14.470 bytes |
| Scripts integrados, gzip | 2.743 bytes |
| Total estimado gzip | 4,54 KB |

La pantalla contiene dos bloques de scripts integrados y un archivo JavaScript externo propio.

### 3.2. Sanidad

| Recurso | Tamaño |
|---|---:|
| `auth.js` | 1,8 KB |
| `sanidad-ui.js` | 2,8 KB |
| Scripts integrados, sin comprimir | 1.132 bytes |
| Scripts integrados, gzip | 419 bytes |
| Total estimado gzip | 5,02 KB |

La pantalla contiene un bloque de scripts integrado y dos archivos JavaScript externos propios.

Los totales son estimaciones obtenidas mediante la suma de los tamaños transferidos de los archivos externos y el tamaño gzip calculado independientemente para los scripts integrados. No equivalen a una medición directa del tamaño comprimido de toda la respuesta HTML.

### 3.3. Evaluación del presupuesto

Ambas pantallas cumplen el límite de 200 KB gzip. Los tamaños estimados son considerablemente inferiores al presupuesto establecido.

## 4. Estado de cumplimiento

| Presupuesto | Objetivo | Sanidad | Gestión de Animales |
|---|---|---|---|
| LCP | Inferior a 2,5 s | Cumple | No cumple |
| INP | Inferior a 200 ms en p75 de campo | No medido | No medido |
| JavaScript inicial | Inferior a 200 KB gzip | Cumple | Cumple |

El INP no se considera verificado porque no se dispone de mediciones de campo recopiladas mediante `web-vitals`. El TBT de Lighthouse se registra como métrica de laboratorio, pero no sustituye al INP.

## 5. Conclusión

Las mediciones muestran que GanadApp cumple el presupuesto de JavaScript inicial en las dos pantallas evaluadas y presenta estabilidad visual durante las pruebas, con CLS igual a cero.

Sin embargo, el rendimiento no es uniforme. Gestión de Animales supera el límite establecido para LCP y presenta un TBT considerablemente mayor que Sanidad. Por lo tanto, el presupuesto de rendimiento se cumple parcialmente: el tamaño de JavaScript está dentro del límite, pero el objetivo de LCP no se alcanza en todas las pantallas. El INP permanece sin verificar por falta de datos de campo.

## 6. Evidencias de medición

Los informes completos generados por Lighthouse se incluyen en el directorio `docs/performance/` del repositorio, mediante los archivos `lighthouse-animales.html` y `lighthouse-sanidad.html`. Estos documentos conservan los resultados de las evaluaciones realizadas sobre las rutas `/animales` y `/sanidad`, respectivamente, incluyendo las métricas de rendimiento, las auditorías de buenas prácticas y los diagnósticos identificados. Constituyen la evidencia de respaldo de los valores registrados y analizados en este documento.