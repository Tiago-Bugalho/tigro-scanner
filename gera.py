from PIL import Image
import os

# Caminho da imagem original
original_icon = "site/tigro.png"

# Pasta de saída para os ícones
output_folder = "site/icons/"

# Cria a pasta de saída se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Tamanhos padrão para PWA
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

try:
    # Abre a imagem original
    img = Image.open(original_icon)

    # Gera os ícones nos tamanhos definidos
    for size in sizes:
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_folder, f"icon-{size}.png")
        resized_img.save(output_path)
        print(f"Ícone gerado: {output_path}")

    print("Todos os ícones foram gerados com sucesso!")

except FileNotFoundError:
    print(f"Erro: arquivo original não encontrado em '{original_icon}'")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
