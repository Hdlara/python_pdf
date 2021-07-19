import io
from django.http import FileResponse
from django.views.generic import View
from reportlab.lib.colors import HexColor

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus.tables import TableStyle, Table
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib import styles
from reportlab.lib import colors
from datetime import datetime

import codecs

from xhtml2pdf import pisa  # import python module

class IndexView(View):

    def get(self, request, *args, **kwargs):

        #cria um arquivo para receber os dados e gerar o PDF
        buffer = io.BytesIO()

        # cria o arquivo pdf
        pdf = canvas.Canvas(buffer, pagesize=portrait(A4))

        # insere 'coisas' no PDF
        # pdf.drawString(100, 100, "geek University")

        width, height = portrait(A4)  # keep for later
        pdf.setFillColorRGB(0, 0, 0.50)
        pdf.line(20, height - 10, width - 20, height - 10)
        pdf.line(20, height - 100, width - 20, height - 100)

        stylesheet = styles.getSampleStyleSheet()
        normalStyle = stylesheet["Normal"]


        P = Paragraph("""<font color=red>brak</font>""", normalStyle)

        data = [
            ["ID", "Produto", "Valor medio Compra", "Valor medio Venda", "Fabricação", "Validade", "Unidade Med"],
            ["1", "Café", 10.00, 13.50, '12/08/2020', '12/08/2021', "UN"],
            ["2", "Chocolate em pó", 9.00, 15.50, '12/04/2021', '22/08/2021', "UN"],
            ["3", "Miojo", 1.00, 1.50, '22/09/2019', '12/05/2021', "UN"],
            ["4", "Sazon", 1.20, 1.50, '10/08/2021', '12/05/2025', "UN"],
            ["5", "Leite", 2.00, 3.50, '12/08/2021', '15/10/2021', "UN"],
            ["6", "Chá", 2.00, 3.50, '24/12/2020', '02/07/2021', "UN"],
            ["7", "Picanha", 20.00, 43.50, '12/03/2021', '12/07/2021', "KG"],
            ["8", "Linguiça", 9.00, 15.50, '24/04/2021', '22/08/2021', "KG"],
            ["9", "Presunto", 1.00, 1.50, '22/05/2021', '12/08/2021', "100GR"],
            ["10", "Banana", 1.20, 1.50, '10/07/2021', '12/09/2021', "KG"],
            ["Total", "", 46.40, 90.00, '', '', ""],
        ]

        t = Table(data, rowHeights=15, repeatCols=1)

        t.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), 'LEFT'),
            # ('SPAN', (0, 0), (-1, 0)),
            # ("ALIGN", (-2, 1), (-2, -1), "CENTER"),
            # ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            # ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            # ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),

        ]))

        t.wrapOn(pdf, width - 250, height)
        w, h = t.wrap(100, 100)
        t.drawOn(pdf, 20, height - (h + 100), 0)

        pdf.setFont("Helvetica", 7)
        pdf.drawRightString(575, 820, 'Relatório - Reportlab' + datetime.today().strftime('%d/%m/%Y %H:%M'))
        pdf.drawRightString(810, 575, datetime.today().strftime('%d/%m/%Y %H:%M'))
        pdf.drawRightString(820, 10, 'Desenvolvido Por Henrique Dias')
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(HexColor('#090400'))
        pdf.drawRightString(265, 795, 'Relatório desenvolvido com Reportlab')
        pdf.drawRightString(225, 775, 'Solicitado em ' + datetime.today().strftime('%d/%m/%Y %H:%M'))
        pdf.drawRightString(230, 755, 'Relatório de produtos Rede Linx')

        #Quando acabar de inserir coisas no PDF
        pdf.showPage()
        pdf.save()

        #por fim retornamos o buffer para o inicio do arquivo
        buffer.seek(0)

        # Faz o dowload do arquivo em PDF gerado
        # return FileResponse(buffer, as_attachment=True, filename='relatorioreportlab.pdf')

        # Abre o PDF direto no navegador
        return FileResponse(buffer, filename='relatorioreportlab.pdf')
