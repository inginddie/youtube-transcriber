"""
Script para encontrar la ubicación de FFmpeg en el sistema
"""
import os
import shutil
from pathlib import Path

def find_ffmpeg():
    """Encuentra la ubicación de FFmpeg en el sistema"""
    
    # Método 1: Buscar en PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return str(Path(ffmpeg_path).parent)
    
    # Método 2: Buscar en ubicaciones comunes de Windows
    possible_locations = [
        # WinGet
        Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages',
        # Chocolatey
        Path('C:/ProgramData/chocolatey/lib'),
        # Instalación manual común
        Path('C:/ffmpeg/bin'),
        Path('C:/Program Files/ffmpeg/bin'),
    ]
    
    for base_path in possible_locations:
        if not base_path.exists():
            continue
        
        # Buscar recursivamente
        for root, dirs, files in os.walk(base_path):
            if 'ffmpeg.exe' in files:
                return root
    
    return None

if __name__ == "__main__":
    print("🔍 Buscando FFmpeg...")
    print()
    
    ffmpeg_location = find_ffmpeg()
    
    if ffmpeg_location:
        print(f"✅ FFmpeg encontrado en:")
        print(f"   {ffmpeg_location}")
        print()
        
        # Verificar que funcione
        ffmpeg_exe = Path(ffmpeg_location) / "ffmpeg.exe"
        if ffmpeg_exe.exists():
            print("✅ ffmpeg.exe verificado")
            
            ffprobe_exe = Path(ffmpeg_location) / "ffprobe.exe"
            if ffprobe_exe.exists():
                print("✅ ffprobe.exe verificado")
            else:
                print("⚠️  ffprobe.exe no encontrado")
        
        print()
        print("Para usar esta ruta, agrégala a tu PATH o usa:")
        print(f'$env:Path += ";{ffmpeg_location}"')
    else:
        print("❌ FFmpeg no encontrado")
        print()
        print("Instala FFmpeg con:")
        print("  winget install ffmpeg")
        print("  o")
        print("  choco install ffmpeg")
