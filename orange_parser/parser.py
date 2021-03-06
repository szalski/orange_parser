#! /usr/bin/env python
# coding: utf-8

'''
Author: Radosław Szalski
'''

from __future__ import print_function
from pprint import pprint
import re
import sys

from detector import Detector

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTFigure, LTImage, LTTextBox, LTTextLine, LAParams, LTText, LTChar, LTLine, LTAnon
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfparser import PDFDocument, PDFParser

def parsePDF(PDFPath):
    with open(PDFPath, 'rb') as pdfFile:
        parser = PDFParser(pdfFile)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()

        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed

        rsrcmgr = PDFResourceManager()

        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pages = doc.get_pages()
        pageLayouts = []

        for index, page in enumerate(pages, start=1):
            if index == 3:
                interpreter.process_page(page)
                pageLayouts.append(device.get_result())

        detector = Detector(pageLayouts)

def sumCostOfCallsTo(dataList, number):
    cost = 0;

    for data in dataList:
        print(data['number'])
        if str(data['number']) == number:
            cost += float(data['total'])

    return cost


def printBilling(textLines):
    for line in textLines:
        if ':' in line:
            print(line)

def getChars(pageLayout):
    '''
    Chars include actual characters as well as LTAnon objects (spaces, non-printable).
    '''
    for layoutObject in pageLayout._objs:
        if isinstance(layoutObject, LTText):
            for textLine in layoutObject._objs:
                for char in textLine._objs:
                    if isinstance (char, LTChar) or isinstance(char, LTAnon):
                        yield char

if __name__ == '__main__':
    try:
        parsePDF(sys.argv[1])
    except Exception as ex:
        print(ex);
