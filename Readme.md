# 🤖 JIRA AI Classifier - Guía de Setup

Sistema completo para clasificar automáticamente tickets de JIRA usando IA local con Gemma 8B.

## 📋 Requisitos Previos

- Python 3.8 o superior
- Acceso a una instancia de JIRA con API token
- Al menos 8GB de RAM disponible para el modelo Gemma

## 🚀 Instalación Paso a Paso

### 1. Instalar Ollama

**Ubuntu/Debian:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Descarga el instalador desde: https://ollama.ai/download

### 2. Descargar el modelo Gemma 8B

```bash
# Iniciar Ollama (si no se inició automáticamente)
ollama serve

# En otra terminal, descargar Gemma 8B
ollama pull gemma:8b
```

**Nota:** La descarga del modelo puede tomar varios minutos (aproximadamente 5GB).

### 3. Configurar el proyecto Python

```bash
# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env
```

### 4. Configurar credenciales de JIRA

Edita el archivo `.env` con tus credenciales:

```bash
# Abre el archivo .env en tu editor favorito
nano .env
```

Completa los siguientes valores:

```env
JIRA_SERVER=https://tucompania.atlassian.net
JIRA_EMAIL=tu-email@empresa.com
JIRA_API_TOKEN=tu_api_token_de_jira
JIRA_PROJECT_KEY=PROJ  # Opcional: clave de tu proyecto
```

#### 🔑 ¿Cómo obtener tu JIRA API Token?

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Haz clic en "Create API token"
3. Dale un nombre descriptivo (ej: "JIRA AI Classifier")
4. Copia el token generado (guárdalo en lugar seguro)

## 🧪 Verificar la Instalación

### Verificar Ollama y Gemma:
```bash
# Verificar que Ollama esté funcionando
curl http://localhost:11434/api/version

# Probar el modelo Gemma
ollama run gemma:7b "Hola, ¿cómo estás?"
```

### Verificar conexión con JIRA:
```bash
# Ejecutar el clasificador en modo test
python main.py
```

## 📚 Uso del Sistema

### 1. Crear tickets de prueba (opcional)

```bash
# Ejecutar el seeder para crear 25 tickets de ejemplo
python seeder.py
```

### 2. Ejecutar el clasificador

```bash
# Clasificar tickets
python main.py
```

El sistema te dará 3 opciones:
1. **Clasificar tickets actualizados hoy** - Procesa solo tickets modificados hoy
2. **Clasificar TODOS los tickets** - Procesa todos los tickets del proyecto
3. **Solo analizar** - Muestra las clasificaciones sin aplicar cambios

### 3. Opciones adicionales

```bash
# Mostrar ayuda
python main.py --help

# Mostrar versión
python main.py --version
```

## 🏷️ Categorías de Clasificación

El sistema clasifica tickets en las siguientes categorías:

- **mantenimiento** - Tareas de mantenimiento y correcciones menores
- **soporte** - Tickets de soporte técnico y ayuda al usuario
- **iniciativa** - Nuevas funcionalidades e iniciativas de negocio
- **bug** - Errores y fallos del sistema
- **optimizacion** - Mejoras de rendimiento y optimizaciones
- **documentacion** - Creación y actualización de documentación
- **infraestructura** - Cambios en infraestructura y DevOps
- **seguridad** - Vulnerabilidades y mejoras de seguridad

## 🛠️ Comandos de Desarrollo

### Reiniciar Ollama:
```bash
# Detener Ollama
pkill ollama

# Iniciar Ollama
ollama serve
```

### Ver logs de Ollama:
```bash
# En macOS/Linux
tail -f ~/.ollama/logs/server.log
```

### Verificar modelos instalados:
```bash
ollama list
```

## 🔧 Solución de Problemas

### ❌ Error: "No se puede conectar con Ollama"

**Solución:**
```bash
# Verificar que Ollama esté ejecutándose
ps aux | grep ollama

# Si no está ejecutándose:
ollama serve

# Verificar el puerto:
netstat -an | grep 11434
```

### ❌ Error: "No se puede conectar con JIRA"

**Soluciones:**
1. Verifica que las credenciales en `.env` sean correctas
2. Asegúrate de que tu JIRA_SERVER tenga el formato: `https://company.atlassian.net`
3. Verifica que tu API token sea válido
4. Comprueba que tengas permisos para leer tickets en el proyecto

### ❌ Error: "Model not found"

**Solución:**
```bash
# Descargar el modelo nuevamente
ollama pull gemma:8b

# Verificar que se descargó correctamente
ollama list
```

### ❌ El clasificador tarda mucho

**Causas posibles:**
- Gemma 8B requiere recursos significativos
- Considera usar `gemma:2b` para menos RAM:
```bash
ollama pull gemma:2b
```
Luego edita `main.py` y cambia `model_name="gemma:2b"`

## 📊 Rendimiento Esperado

- **Tiempo por ticket:** 3-10 segundos (dependiendo de hardware)
- **RAM necesaria:** 8-16GB para Gemma 8B
- **Precisión esperada:** 80-90% en clasificaciones

## 🔒 Consideraciones de Seguridad

- Los datos de JIRA se procesan localmente
- El modelo Gemma se ejecuta completamente offline
- Las credenciales se almacenan en archivo `.env` local
- **Importante:** No compartas tu archivo `.env` ni tu API token

## 📞 Soporte

Si encuentras problemas:

1. Revisa esta guía de setup
2. Verifica los logs de Ollama
3. Asegúrate de que las credenciales sean correctas
4. Comprueba que tengas suficiente RAM disponible

## 🚀 ¡Listo para Comenzar!

Una vez completado el setup:

```bash
# 1. Crear tickets de prueba
python seeder.py

# 2. Clasificar tickets
python main.py

# 3. ¡Disfruta de la clasificación automática! 🎉
```