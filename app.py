from flask import Flask, request, send_file
import os
import time
from compressor import compress_pdf

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para verificar se o arquivo enviado é um PDF
def allowed_file(filename):
    return filename.lower().endswith('.pdf')

@app.route('/compress', methods=['POST'])
def compress():
    """Rota para compactar o PDF enviado."""
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if not allowed_file(file.filename):
        return "Invalid file format. Only PDFs are allowed.", 400

    # Gerar nomes únicos para os arquivos
    timestamp = int(time.time())
    input_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f'uploaded_file_{timestamp}.pdf')
    output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f'compressed_file_{timestamp}.pdf')

    try:
        # Salvar o arquivo enviado
        file.save(input_pdf)

        # Comprimir o PDF
        compress_pdf(input_pdf, output_pdf)

        # Retornar o PDF compactado
        return send_file(output_pdf, as_attachment=True)
    except Exception as e:
        return f"Error compressing PDF: {str(e)}", 500
    finally:
        # Limpar os arquivos temporários
        if os.path.exists(input_pdf):
            os.remove(input_pdf)
        if os.path.exists(output_pdf):
            os.remove(output_pdf)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
