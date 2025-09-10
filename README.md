
# Dark GPT - LLaMA 3.1 Chat Interface

Una interfaz de chat moderna y oscura para interactuar con el modelo LLaMA 3.1 8B Uncensored, con traducción automática español-inglés.

## 🚀 Características

- 🤖 Interfaz con el modelo LLaMA 3.1 8B Uncensored (DARE)
- 🌐 Traducción automática bidireccional (Español ↔ Inglés)
- 🎨 Interfaz oscura moderna con Flet
- 💬 Chat en tiempo real con historial
- 📋 Soporte para bloques de código con resaltado
- 📱 Interfaz responsive

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/DarkPierc/Dark_GPT.git
cd Dark_GPT
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

1. Ejecuta la aplicación:
```bash
python main.py
```

2. La aplicación se abrirá en una nueva ventana
3. Escribe tu mensaje en español o inglés
4. Presiona "Enviar" o Enter para enviar tu mensaje
5. Espera la respuesta del modelo

## 🛠️ Tecnologías Utilizadas

- **Flet**: Framework para crear aplicaciones web, móviles y de escritorio
- **Requests**: Para realizar peticiones HTTP a la API del modelo
- **LLaMA 3.1 8B**: Modelo de lenguaje grande sin censura

## 📝 Estructura del Proyecto

```
dark-gpt/
│
├── main.py              # Archivo principal de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación del proyecto
└── .venv/              # Entorno virtual (no incluir en git)
```

## 🔍 Funcionalidades Principales

### Traducción Automática
- Detecta automáticamente el idioma del mensaje
- Traduce mensajes en español al inglés antes de enviarlos al modelo
- Traduce las respuestas del modelo de vuelta al español

### Interfaz de Usuario
- Tema oscuro moderno
- Mensajes diferenciados por color para usuario y AI
- Indicadores de estado y progreso
- Botón para limpiar el historial del chat

## ⚠️ Notas Importantes

- El modelo LLaMA 3.1 8B Uncensored puede generar contenido sin restricciones
- La API utilizada es gratuita y puede tener limitaciones de uso
- La traducción utiliza Google Translate API (endpoint gratuito)

## 🐛 Solución de Problemas

### Error de conexión
- Verifica tu conexión a internet
- La API puede estar temporalmente no disponible

### Error de traducción
- El servicio de traducción puede estar limitado
- Los mensajes muy largos pueden no traducirse completamente

