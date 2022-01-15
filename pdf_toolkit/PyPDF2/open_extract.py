# ---------------------------------------------------------------------------- #
#     Note: PyPDF2 is not actively maintained so use 'pikepdf' if possible     #
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

import inspect
import PyPDF2
import os

# ---------------------------------------------------------------------------- #
#                                 Open and Read                                #
# ---------------------------------------------------------------------------- #

os.getcwd()
# Open in read binary mode
with open('./meetingminutes.pdf', mode='rb') as pdf:
    # Instantiate PdfFileReader object
    pdfReader = PyPDF2.PdfFileReader(pdf)

    # Get document info function, returns a DocumentInformation instance, or None if none exists
    # If returned, the instance will be a document information dictionary
    docinfo = pdfReader.getDocumentInfo()
    # Read-only property that accesses the document info attribute
    docinfo_attr = pdfReader.documentInfo

    # Get outline function, returns a PageObject instance
    # Cannot be accessed once closed
    outline = pdfReader.getOutlines()
    # Read-only property that accesses the outline attribute
    outline_attr = pdfReader.outlines

    # Get page number function, returns an integer
    page_num = pdfReader.getNumPages()
    # Read-only property that accesses page number attribute
    page_num_attr = pdfReader.numPages

    # Retrieves a page by number from this PDF file, returns a PageObject instance
    # Cannot be accessed once closed
    list_of_pageobjects = [pdfReader.getPage(num) for num in range(page_num)]
    # Call extractText() method on PageObject objects in the list above
    list_of_extracted_texts = [page.extractText()
                               for page in list_of_pageobjects]

# ---------------------------------------------------------------------------- #
#                                  Decrypting                                  #
# ---------------------------------------------------------------------------- #

# Open
pdfReader = PyPDF2.PdfFileReader(open('encrypted.pdf', 'rb'))

# Read-only boolean property showing whether this PDF file is encrypted
# If true, it will remain true even after the PdfFileReader.decrypt() function is called
pdfReader.isEncrypted

# Call the PdfFileReader.decrypt(password) function
# Returns 0 if failed, 1 if the password matched the user password, and 2 if the password matched the owner password
#  Raises NotImplementedError if document uses an unsupported encryption method
pdfReader.decrypt('rosebud')

# Calling getPage() on an encrypted PDF before calling decrypt() on it causes future getPage() calls to fail
# The error is 'IndexError: list index out of range'
# Close file
pdfReader.close()

# ---------------------------------------------------------------------------- #
#                                  Encrypting                                  #
# ---------------------------------------------------------------------------- #

# Open and copy
with open('./watermarkmeeting.pdf', 'rb') as pdfFile:
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfWriter = PyPDF2.PdfFileWriter()

    for page_num in range(pdfReader.numPages):
        page = pdfReader.getPage(page_num)
        pdfWriter.addPage(page)

    # Encrypt before writing
    pdfWriter.encrypt(user_pwd='1234user', owner_pwd='1234owner')
    with open('./encryptedmeeting.pdf', 'wb') as pdfoutput:
        pdfWriter.write(pdfoutput)


# ---------------------------------------------------------------------------- #
#                                    Copying                                   #
# ---------------------------------------------------------------------------- #

# Open files in read-binary mode
pdf1File = open('meetingminutes.pdf', 'rb')
pdf2File = open('meetingminutes2.pdf', 'rb')

# Instantiate reader objects
pdf1Reader, pdf2Reader = (PyPDF2.PdfFileReader(
    pdf1File), PyPDF2.PdfFileReader(pdf2File))

# Instantiate writer object
pdfWriter = PyPDF2.PdfFileWriter()

# The addPage() method will only add pages to the end and cannot insert
# Copy content from pdf1 and pdf2 to writer object
for page_num in range(pdf1Reader.numPages):
    # Get the Page object by calling getPage() on a PdfFileReader object
    page_obj1 = pdf1Reader.getPage(page_num)
    # Call addPage() function on writer object
    pdfWriter.addPage(page_obj1)

for page_num in range(pdf2Reader.numPages):
    # Get the Page object by calling getPage() on a PdfFileReader object
    page_obj2 = pdf2Reader.getPage(page_num)
    # Call addPage() function on writer object
    pdfWriter.addPage(page_obj2)

# Now the writer object should have pdf1Reader.numPages + pdf2Reader.numPages pages
pdfWriter.getNumPages() == pdf1Reader.numPages + pdf2Reader.numPages

# Open file in write-binary mode
pdfOutputFile = open('combinedminutes.pdf', 'wb')
# Call write() method to write the collection of pages as a PDF file
pdfWriter.write(pdfOutputFile)

# Close files
pdfOutputFile.close()
pdf1File.close()
pdf2File.close()

# ---------------------------------------------------------------------------- #
#                                Rotating pages                                #
# ---------------------------------------------------------------------------- #

# Open in read-binary
pdfFile = open('./meetingminutes.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile)

# Instantiate writer object
pdfWriter = PyPDF2.PdfFileWriter()
# Rotate all pages 90 degrees counter-clockwise
for num1 in range(pdfReader.numPages):
    page1 = pdfReader.getPage(num1)
    page1.rotateCounterClockwise(90)
    pdfWriter.addPage(page1)

# Open in write-binary
resultPdfFile = open('rotatedpdf.pdf', 'wb')
pdfWriter.write(resultPdfFile)

# Close files
pdfFile.close()
resultPdfFile.close()

# ---------------------------------------------------------------------------- #
#                                  Overlaying                                  #
# ---------------------------------------------------------------------------- #

# Open
pdfFile = open('./meetingminutes.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile)

# Watermark reader (only has one page)
watermarkFile = open('./watermark.pdf', 'rb')
watermarkpage = PyPDF2.PdfFileReader(watermarkFile).getPage(0)


# Writer object
pdfWriter = PyPDF2.PdfFileWriter()

# Merge watermark onto each page of pdfReader
for page_num in range(pdfReader.numPages):
    page = pdfReader.getPage(page_num)
    page.mergePage(watermarkpage)
    pdfWriter.addPage(page)

# Open in writing-binary mode
resultPdfFile = open('watermarkmeeting.pdf', 'wb')
pdfWriter.write(resultPdfFile)

# Close files
pdfFile.close()
watermarkFile.close()
resultPdfFile.close()

# ---------------------------------------------------------------------------- #
#                                     Merge                                    #
# ---------------------------------------------------------------------------- #

# Instantiate PdfFileMerger class
# The parameter deterines if users should be warned of all problems
pdfMerger = PyPDF2.PdfFileMerger(strict=True)

# Open pdf files in read-binary mode
# Opt to not use with for interactive purposes
pdf1 = open('./watermarkmeeting.pdf', 'rb')
pdfReader1 = PyPDF2.PdfFileReader(pdf1)

pdf2 = open('./meetingminutes.pdf', 'rb')
pdfReader2 = PyPDF2.PdfFileReader(pdf2)

pdf3 = open('./combinedminutes.pdf', 'rb')
pdfReader3 = PyPDF2.PdfFileReader(pdf3)

# Take the first 3 pages of pdf2 and merge it into the merger object as its first 3
pdfMerger.merge(
    position=0,
    fileobj=pdfReader2,
    bookmark='pdf2',
    # Using tuple
    pages=(0, 3)
)
# Take all pages from start to end, skipping 2 pages at at time, of pdf1
pdfMerger.append(
    fileobj=pdfReader1,
    bookmark='pdf1',
    # Use page range
    pages=PyPDF2.PageRange('::3')
)
# Rotate pages in pdf3 by 90 degrees and insert it to the 10th page of the merge object

# Rotate
rotatedwriter = PyPDF2.PdfFileWriter()
for page_num in range(pdfReader3.numPages):
    page = pdfReader3.getPage(page_num).rotateClockwise(90)
    rotatedwriter.addPage(page)

# Write rotated pdf to disk
with open('rotate_pdf3.pdf', 'wb') as output:
    rotatedwriter.write(output)

# Read in new rotated pdf
pdf3 = open('./rotate_pdf3.pdf', 'rb')
pdfReader3 = PyPDF2.PdfFileReader(pdf3)

pdfMerger.merge(
    position=10,
    fileobj=pdfReader3,
    bookmark='pdf3rotated',
    pages=PyPDF2.PageRange(':')
)

# Write merger object to disk
mergedpdf = open('mergedall.pdf', 'wb')
pdfMerger.write(mergedpdf)

# Close files
pdf1.close()
pdf2.close()
pdf3.close()
mergedpdf.close()
