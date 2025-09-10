"""
Script para crear un instalador de Dark GPT usando PyInstaller
con opciones para reducir falsos positivos y alertas de SmartScreen
"""
import os
import datetime
from PyInstaller.__main__ import run

# Define los argumentos para PyInstaller
if __name__ == "__main__":
    # Directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(script_dir, "main.py")
    
    # Usar la fecha actual como parte del nombre para reducir alertas de SmartScreen
    # (SmartScreen recuerda archivos por nombre y hash)
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    output_name = f"DarkGPT_{current_date}"
    
    args = [
        main_file,
        f"--name={output_name}",
        "--noconfirm",
        "--windowed",
        "--clean",
        # Agregar icono personalizado
        "--icon=DarkGPT.ico",
        # Crear un directorio en lugar de un único archivo
        # Los antivirus suelen ser menos agresivos con esto
        "--onedir",
        "--noupx",
        # Mejor manejo de módulos
        "--collect-all=flet",
        "--collect-all=requests",
    ]
    
    # Ejecutar PyInstaller
    run(args)
    
    print(f"Compilación completada. La aplicación se encuentra en la carpeta 'dist/{output_name}'.")
    print("Para distribuir:")
    print("1. Comprime la carpeta 'dist/DarkGPT_XXX' en un archivo ZIP")
    print("2. O utiliza el script 'darkgpt_installer.iss' con Inno Setup para crear un instalador revisa el archivo instruccionesfinales.txt")
