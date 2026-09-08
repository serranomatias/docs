# ContactShip Docs

Documentación pública de ContactShip: [docs.contactship.ai](https://docs.contactship.ai). Construida con [Mintlify](https://mintlify.com); se publica sola al hacer push a `main`.

Esta etapa cubre **solo texto**: 216 páginas de navegación completas, con guías en español e inglés y referencia API compartida. Capturas, videos y GIFs quedan para una etapa posterior.

## Estructura

| Carpeta | Qué contiene |
|---|---|
| `es/` | Documentación en español (idioma por defecto). Un directorio por grupo del menú: `comenzar`, `agentes-de-voz`, `agentes-de-texto`, `mensajes`, `llamadas`, `contactos`, `contact-center`, `enrutamiento`, `reportes`, `organizacion`, `facturacion`, `integraciones`, `mcp`, `casos-de-uso`. |
| `en/` | Espejo en inglés con la misma estructura (`get-started`, `voice-agents`, `text-agents`, `messages`, `calls`, `contacts`, `contact-center`, `lead-routing`, `reports`, `organization`, `billing`, `integrations`, `mcp`, `use-cases`). |
| `api-reference/` | Referencia de la API pública (solo en inglés, compartida por los dos idiomas). Una página por endpoint en `endpoint/`, más `introduction`, `rate-limits` y `webhooks`. |
| `snippets/` | Componentes reutilizables. `availability.mdx` exporta el bloque de disponibilidad (plan, add-on, permiso, dónde) que va al inicio de cada página de producto. |
| `images/` | Capturas y clips. Nombres `images/<grupo>/<pantalla>-es.png` y `-en.png`. |
| `docs.json` | Navegación, idiomas, redirecciones de URLs viejas y configuración del sitio. |
| `.internal/` | Herramientas de QA y registro de rutas retiradas. Las notas de fuentes, inventarios y material sensible se conservan localmente, excluidos de Git; `.mintignore` excluye toda la carpeta del sitio. |

## Antes de escribir

Mantené el tono y la estructura de las páginas actuales: pasos concretos, disponibilidad, preguntas frecuentes y enlaces a contenido relacionado. Conservá la paridad español/inglés. Contrastá comportamientos con la app y su backend antes de afirmarlos. Si tenés las notas internas locales, consultá también `.internal/STYLE-GUIDE.md`.

## Vista previa local

```bash
npx mint@latest dev
```

Abre http://localhost:3000. Para revisar enlaces rotos:

```bash
npx mint@latest broken-links
```

## Control de calidad

```bash
python3 .internal/qa/check-pages.py --strict
python3 -m unittest discover -s .internal/qa -p 'test_*.py'
npx mint@latest validate --disable-openapi
npx mint@latest broken-links --check-anchors --check-snippets --check-redirects
```

El validador local comprueba archivos, navegación, enlaces internos, redirecciones, disponibilidad, preguntas frecuentes y cantidad de páginas ES/EN. Mintlify verifica compilación MDX y anclas. `.mintignore` excluye `.internal/` y este README de la compilación pública.

La revisión combina compilación, validación de enlaces y contraste con el código; no equivale a pruebas autenticadas en producción. Las notas de recuperación y fuentes se conservan localmente y no forman parte de este repositorio público.

## Capturas de pantalla (postergadas)

Algunas páginas conservan marcadores `{/* captura: images/<grupo>/<nombre>-es.png | qué mostrar | app: <ruta> */}` donde va cada imagen. El pipeline de capturas se conserva en las notas internas locales para una etapa posterior.

## Contacto

Soporte: support@contactship.ai
