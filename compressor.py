import pikepdf


def compress_pdf(input_pdf, output_pdf):
    with pikepdf.open(input_pdf) as pdf:
        pdf.save(output_pdf, compress_streams=True)
