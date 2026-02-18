# YouTube Bot Detection - Solutions

Si ves este error:
```
YouTube is blocking this video (bot detection).
This video may require authentication or may be age-restricted.
```

## ¿Por qué sucede?

YouTube detecta que la solicitud proviene de un bot (no es un navegador real). Esto sucede especialmente en:
- Servidores sin navegador instalado (como Railway)
- Videos con restricción de edad
- Canales privados o semiconfinados
- Durante períodos de alto tráfico

## Soluciones (por orden de facilidad)

### ✅ Opción 1: Usar un video diferente (Más fácil)

Algunos videos no tienen estas restricciones. Intenta con:
- Videos públicos populares
- Videos de canales verificados
- Videos sin restricción de edad

### ✅ Opción 2: Esperar y reintentar (Recomendado)

YouTube limita reintentos. Si ves el error:
1. Espera **5-10 minutos**
2. Intenta transcribir el mismo video nuevamente
3. El sistema intentará 6 estrategias diferentes con delays exponenciales

### ✅ Opción 3: Usar Cookies de Autenticación (Más robusta)

Esto funciona en cualquier entorno, incluso servidores.

#### Paso 1: Exportar cookies desde tu navegador

**Opción A: Usar la extensión Get Cookies**
1. Instala: https://github.com/kairi003/Get-cookies.txt-LOCALLY
2. Ve a https://www.youtube.com
3. Haz clic en la extensión
4. Selecciona "Export" → "Netscape HTTP Cookie File"
5. Guarda el archivo como `cookies.txt`

**Opción B: Usar el script helper**
```bash
# En tu máquina local (con navegador)
python export_youtube_cookies.py /ruta/a/cookies.txt
```

#### Paso 2: Colocar cookies en la ubicación correcta

Las cookies deben estar en:
```
~/.youtube_cookies.txt
```

En diferentes sistemas:
- **Linux/Mac**: `~/.youtube_cookies.txt`
- **Windows**: `C:\Users\TuUsuario\.youtube_cookies.txt`
- **Railway/Docker**: Necesita ser configurado en el despliegue

#### Paso 3: Probar

Intenta transcribir un video. El sistema detectará las cookies y las usará automáticamente.

## Cómo funciona internamente

El sistema intenta **6 estrategias en orden**:

1. **Headers avanzados** - Parecemos un navegador Chrome real
2. **Extended timeout** - Esperamos más para no ser throttled
3. **Modo básico** - Headers mínimos sin opciones avanzadas
4. **Cookies de archivo local** - Si `~/.youtube_cookies.txt` existe
5. **Cookies de Chrome** - Si Chrome está instalado
6. **Cookies de Firefox** - Si Firefox está instalado

Entre cada estrategia espera con **backoff exponencial** (3s, 6s, 12s, 24s, 30s).

## Para Railway/Producción

Si despliegas en Railway y necesitas cookies:

1. **Exporte cookies** en tu máquina local usando el script
2. **Agregue a Railway secrets/files** (depende de tu configuración)
3. **O use la interfaz** para cargar el archivo

## Debugging

Para ver qué estrategia está funcionando, revisa los logs:
```
Strategy 1/6 (Advanced headers) - 🔧 Configurando...
Strategy 2/6 (Extended timeout) - ⏳ Esperando 3s...
Strategy 3/6 (Basic mode) - 🔧 Configurando...
...
```

## Más información

- [yt-dlp cookies documentation](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)
- [YouTube bot detection explained](https://github.com/yt-dlp/yt-dlp/issues/1654)

## ¿Sigue sin funcionar?

Si aún ves el error:
1. Verifica que el archivo de cookies existe en la ubicación correcta
2. Prueba con un video diferente
3. Espera 10 minutos entre intentos
4. Revisa que tu acceso a YouTube no esté restringido
