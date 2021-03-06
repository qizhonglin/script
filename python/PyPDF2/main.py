#!/usr/bin/python
#coding: utf-8

import os
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

def create_watermark(content, pdf_watermark):
    c = canvas.Canvas(pdf_watermark)
    c.setFont('Courier', 10)

    c.saveState()
    c.translate(300, 15)
    c.drawCentredString(0, 0, content)
    c.restoreState()
    c.save()

    pdf_watermark = PdfFileReader(file(pdf_watermark, 'rb'))
    return pdf_watermark


def add_watermark(pdf_file, pdf_watermark):
    pdf_output = PdfFileWriter()
    pdf_input = PdfFileReader(file(pdf_file, 'rb'))
    watermark = pdf_watermark.getPage(0)

    numPages = pdf_input.getNumPages()
    for i in xrange(numPages):
	page = pdf_input.getPage(i)
	page.mergePage(watermark)
	pdf_output.addPage(page)

    with open('output.pdf', 'wb') as f:
	pdf_output.write(f)


if __name__ == '__main__':
    pdf_watermark = create_watermark('www.site-digger.com', 'watermark.pdf')
    add_watermark('test.pdf', pdf_watermark)
