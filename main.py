import flet as ft
import requests
import json
import threading
import urllib.parse
import re
from datetime import datetime

class DarkGPTApp:
    def __init__(self):
        self.page = None
        self.chat_messages = []
        self.user_input = None
        self.send_button = None
        self.status_text = None
        self.progress_ring = None
        
    def main(self, page: ft.Page):
        self.page = page
        page.title = "Dark GPT - LLaMA 3.1 8B Uncensored - Friends School"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.bgcolor = "#1f1f1f"
        page.window.width = 1000
        page.window.height = 800
        page.window.min_width = 800
        page.window.min_height = 600
        
        # Header
        header_container = ft.Container(
            content=ft.Column([
                ft.Text("Dark GPT Curso de Python Friends School", size=32, weight=ft.FontWeight.BOLD, color="#ffcc00"),
                ft.Text("Powered by LLaMA 3.1 - 8B Uncensored (DARE)- TG @worldfriendsx", size=16, color="#cccccc"),
                ft.Text("🌐 Traducción automática Español/Inglés habilitada", 
                       size=12, italic=True, color="#aaaaaa"),
            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
            margin=ft.margin.only(bottom=20),
        )
        
        # Chat area
        self.chat_area = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            padding=20,
        )
        
        chat_container = ft.Container(
            content=self.chat_area,
            expand=True,
            border=ft.border.all(1, "#333333"),
            border_radius=10,
            bgcolor="#2b2b2b",
            padding=10,
        )
        
        # Input area
        self.user_input = ft.TextField(
            hint_text="Escribe tu mensaje aquí (Español o Inglés)...",
            border_color="#444444",
            bgcolor="#333333",
            color="white",
            multiline=True,
            min_lines=2,
            max_lines=5,
            expand=True,
            on_submit=self.send_message,
        )
        
        self.send_button = ft.ElevatedButton(
            text="Enviar",
            icon=ft.icons.SEND,
            bgcolor="#007bff",
            color="white",
            on_click=self.send_message,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )
        
        input_row = ft.Row(
            [
                self.user_input,
                self.send_button,
            ],
            spacing=10,
        )
        
        # Status bar
        self.progress_ring = ft.ProgressRing(
            width=16, 
            height=16, 
            stroke_width=2, 
            visible=False,
            color="#007bff"
        )
        
        self.status_text = ft.Text("Listo", color="#aaaaaa", size=12)
        
        status_row = ft.Row(
            [
                self.progress_ring,
                self.status_text,
                ft.Container(expand=True),
                ft.ElevatedButton(
                    text="Limpiar Chat",
                    icon=ft.icons.CLEAR_ALL,
                    on_click=self.clear_chat,
                    bgcolor="#555555",
                    color="white",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Add everything to the page
        page.add(
            header_container,
            chat_container,
            ft.Container(input_row, margin=ft.margin.only(top=10, bottom=10)),
            status_row,
        )
        
        # Initialize with a welcome message
        self.add_message(
            "¡Bienvenido a Dark GPT creado por Curso de python Friends school! Estoy impulsado por LLaMA 3.1 - 8B Uncensored (DARE). Pregúntame cualquier cosa en español o inglés. 🤖", 
            is_user=False
        )
    
    def add_message(self, message, is_user=True, show_translation_info=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        avatar = ft.CircleAvatar(
            content=ft.Text("Tú" if is_user else "AI", color="white", size=14),
            bgcolor="#007bff" if is_user else "#ffcc00",
            radius=20,
        )
        
        sender_name = ft.Text(
            "Tú" if is_user else "Dark GPT",
            weight=ft.FontWeight.BOLD,
            color="#75c0ff" if is_user else "#ffcc00",
            size=14,
        )
        
        time_text = ft.Text(
            f"[{timestamp}]",
            color="#aaaaaa",
            size=12,
        )
        
        header = ft.Row([
            avatar,
            ft.Column([
                sender_name,
                time_text,
            ], spacing=2, alignment=ft.MainAxisAlignment.START),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Process message content
        message_content = self.format_message_content(message, is_user)
        
        content_items = [header, ft.Container(height=5), message_content]
        
        # Add translation info if provided
        if show_translation_info:
            translation_text = ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.TRANSLATE, size=14, color="#888888"),
                    ft.Text(
                        show_translation_info,
                        size=11,
                        color="#888888",
                        italic=True,
                    ),
                ]),
                bgcolor="#1e1e1e",
                border_radius=5,
                padding=5,
                margin=ft.margin.only(top=5),
            )
            content_items.append(translation_text)
        
        message_container = ft.Container(
            content=ft.Column(
                content_items,
                spacing=5,
            ),
            bgcolor="#333333" if is_user else "#2d2d2d",
            border_radius=10,
            padding=10,
            margin=ft.margin.only(bottom=5),
        )
        
        self.chat_area.controls.append(message_container)
        self.page.update()
    
    def format_message_content(self, message, is_user):
        if is_user:
            return ft.Text(message, selectable=True, color="white", size=14)
        else:
            if "```" in message or "`` `` ``" in message:
                return self.format_with_code_blocks(message)
            else:
                return ft.Text(message, selectable=True, color="white", size=14)
    
    def format_with_code_blocks(self, message):
        parts = []
        lines = message.split("\n")
        in_code_block = False
        code_lines = []
        language = ""
        regular_text = []
        
        for line in lines:
            # Check for both standard and non-standard code block delimiters
            is_code_delimiter = line.startswith("```") or line.strip() == "`` `` ``"
            
            if is_code_delimiter:
                # First, add any accumulated regular text
                if regular_text and not in_code_block:
                    text = "\n".join(regular_text)
                    parts.append(ft.Text(text, selectable=True, color="white", size=14))
                    regular_text = []
                
                if in_code_block:
                    # End of code block
                    in_code_block = False
                    code_text = "\n".join(code_lines)
                    parts.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(f"📋 Código {f'({language})' if language else ''}", 
                                           size=12, color="#00ff00"),
                                    ft.IconButton(
                                        icon=ft.icons.COPY,
                                        icon_size=16,
                                        tooltip="Copiar código",
                                        on_click=lambda e, code=code_text: self.copy_to_clipboard(code),
                                    ),
                                ]),
                                ft.Text(
                                    code_text,
                                    selectable=True,
                                    size=14,
                                    color="#00ffff",
                                    font_family="monospace",
                                ),
                            ]),
                            bgcolor="#1e1e1e",
                            border_radius=5,
                            padding=10,
                            margin=ft.margin.symmetric(vertical=5),
                        )
                    )
                    code_lines = []
                else:
                    # Start of code block
                    in_code_block = True
                    # Extract language if present in standard format
                    if line.startswith("```"):
                        language = line[3:].strip()
            elif in_code_block:
                code_lines.append(line)
            else:
                regular_text.append(line)
        
        # Add any remaining regular text
        if regular_text:
            text = "\n".join(regular_text)
            parts.append(ft.Text(text, selectable=True, color="white", size=14))
        
        return ft.Column(parts, spacing=5)
    
    def copy_to_clipboard(self, text):
        self.page.set_clipboard(text)
        self.status_text.value = "¡Código copiado al portapapeles!"
        self.page.update()
        threading.Timer(2.0, lambda: self.update_status("Listo")).start()
    
    def send_message(self, e=None):
        if not self.user_input.value or self.user_input.value.isspace():
            return
        
        user_message = self.user_input.value.strip()
        self.user_input.value = ""
        self.page.update()
        
        # Add user message to chat
        self.add_message(user_message, is_user=True)
        
        # Show progress and update status
        self.progress_ring.visible = True
        self.status_text.value = "Procesando..."
        self.send_button.disabled = True
        self.page.update()
        
        # Start a thread to fetch the response
        threading.Thread(target=self.fetch_response, args=(user_message,), daemon=True).start()
    
    def detect_language(self, text):
        """Detect if text is in Spanish or English using simple heuristics"""
        # Spanish common words and patterns
        spanish_indicators = [
            # Articles and prepositions
            r'\b(el|la|los|las|un|una|unos|unas|del|al)\b',
            # Common verbs
            r'\b(es|está|son|están|fue|fueron|ser|estar|hacer|tener|haber|poder|decir|ir|ver|dar|saber|querer)\b',
            # Question words
            r'\b(qué|cómo|cuándo|dónde|quién|cuál|cuánto|por qué)\b',
            # Common words
            r'\b(para|por|con|sin|sobre|entre|pero|porque|cuando|donde|muy|más|menos|también|siempre|nunca|ahora|después|antes|aquí|allí)\b',
            # Spanish-specific characters in words
            r'[áéíóúñü]',
        ]
        
        # English common words and patterns
        english_indicators = [
            # Articles and common words
            r'\b(the|a|an|is|are|was|were|have|has|had|will|would|could|should|may|might)\b',
            # Pronouns
            r'\b(i|you|he|she|it|we|they|me|him|her|us|them)\b',
            # Question words
            r'\b(what|when|where|who|why|how|which)\b',
            # Common words
            r'\b(for|with|without|about|from|into|through|during|before|after|above|below|between)\b',
        ]
        
        text_lower = text.lower()
        
        # Count matches for each language
        spanish_score = sum(1 for pattern in spanish_indicators if re.search(pattern, text_lower, re.IGNORECASE))
        english_score = sum(1 for pattern in english_indicators if re.search(pattern, text_lower, re.IGNORECASE))
        
        # Return the language with higher score
        if spanish_score > english_score:
            return 'es'
        elif english_score > spanish_score:
            return 'en'
        else:
            # Default to Spanish if unsure (since the app is primarily for Spanish speakers)
            return 'es'
    
    def translate_text(self, text, source_lang, target_lang):
        """Translate text using Google Translate API (free endpoint)"""
        try:
            # Don't translate if source and target are the same
            if source_lang == target_lang:
                return text
            
            # Google Translate free API endpoint
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,  # source language
                'tl': target_lang,  # target language
                'dt': 't',          # translation
                'q': text           # query text
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Extract translated text from the response
                if result and isinstance(result, list) and result[0]:
                    translated_parts = []
                    for sentence in result[0]:
                        if sentence[0]:
                            translated_parts.append(sentence[0])
                    return ''.join(translated_parts)
            
            # If translation fails, return original text
            return text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def fetch_response(self, prompt):
        try:
            detected_lang = self.detect_language(prompt)
            
            # Translate to English if the text is in Spanish
            if detected_lang == 'es':
                self.update_ui(lambda: self.update_status("Traduciendo al inglés..."))
                prompt_en = self.translate_text(prompt, 'es', 'en')
                
                # Only use translation if it's different from original
                if prompt_en != prompt and prompt_en:
                    prompt = prompt_en
            
            # Update status
            self.update_ui(lambda: self.update_status("Consultando modelo LLM..."))
            
            # Encode the prompt for URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # API endpoint
            api_url = f"https://laama.revangeapi.workers.dev/chat?prompt={encoded_prompt}"
            
            # Send request with timeout
            response = requests.get(api_url, timeout=30)
            
            if response.status_code == 200:
                # Format the response
                formatted_response = self.format_response(response.text)
                
                # Translate response to Spanish if original was in Spanish
                if detected_lang == 'es':
                    self.update_ui(lambda: self.update_status("Traduciendo respuesta al español..."))
                    translated_response = self.translate_text(formatted_response, 'en', 'es')
                    
                    # Only show translation info if translation actually occurred
                    if translated_response != formatted_response:
                        response_translation_info = "Respuesta traducida del inglés"
                    else:
                        response_translation_info = None
                    
                    self.update_ui(
                        lambda: self.add_message(
                            translated_response, 
                            is_user=False, 
                            show_translation_info=response_translation_info
                        )
                    )
                else:
                    # Add response without translation
                    self.update_ui(lambda: self.add_message(formatted_response, is_user=False))
            else:
                error_message = f"Error: No se pudo obtener respuesta (Código: {response.status_code})"
                self.update_ui(lambda: self.add_message(error_message, is_user=False))
                
        except requests.Timeout:
            error_message = "Error: Tiempo de espera agotado. Por favor, intenta de nuevo."
            self.update_ui(lambda: self.add_message(error_message, is_user=False))
        except requests.RequestException as e:
            error_message = f"Error de conexión: {str(e)}"
            self.update_ui(lambda: self.add_message(error_message, is_user=False))
        except Exception as e:
            error_message = f"Error inesperado: {str(e)}"
            self.update_ui(lambda: self.add_message(error_message, is_user=False))
        
        finally:
            # Reset UI state back in the main thread
            self.update_ui(self.reset_ui_state)
    
    def format_response(self, response_text):
        try:
            response_json = json.loads(response_text)
            
            if "reply" in response_json:
                return response_json["reply"]
            elif "response" in response_json:
                return response_json["response"]
            elif "message" in response_json:
                return response_json["message"]
            
            # If no known field, return formatted JSON
            return json.dumps(response_json, indent=2, ensure_ascii=False)
            
        except json.JSONDecodeError:
            # If not JSON, return as plain text
            return response_text.strip()
    
    def update_status(self, status):
        self.status_text.value = status
        self.page.update()
    
    def update_ui(self, fn):
        """Helper method to update UI from a background thread"""
        fn()
        self.page.update()
    
    def reset_ui_state(self):
        self.progress_ring.visible = False
        self.status_text.value = "Listo"
        self.send_button.disabled = False
        self.page.update()
    
    def clear_chat(self, e=None):
        self.chat_area.controls.clear()
        self.update_status("Chat limpiado")
        
        # Add welcome message back
        self.add_message(
            "¡Bienvenido a Dark GPT! Estoy impulsado por LLaMA 3.1 - 8B Uncensored (DARE). Pregúntame cualquier cosa en español o inglés. 🤖", 
            is_user=False
        )

if __name__ == "__main__":
    app = DarkGPTApp()
    ft.app(target=app.main)