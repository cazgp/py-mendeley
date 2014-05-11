#!/usr/bin/python

from pdfquery import PDFQuery
from mendeley import Mendeley
from helpers import substring, extract, extract_unmerged

folder_id = 24
m = Mendeley()

# Get all documents we wish to extract in folder
dIds = m.get_documents_in_folder(folder_id)

highlights = []
for d in dIds:
    hs = m.get_highlights(d)
    if len(hs):
        highlights.append((d, hs))

for dId, hs in highlights:
    # Get the document and the Mendeley highlights
    path = m.get_file_path(dId)
    rects = m.get_highlight_rects(hs)

    # Get the author year title to call the saved txt file
    txt = m.get_author_year_title(dId)

    # Load the pdf files, one merged and one not
    pdf = PDFQuery(path)
    pdf_unmerged = PDFQuery(path, merge_tags=('LTAnno'))

    document_highlights = []
    current_highlight_id = -1
    current_highlight = []

    for _, hId, page, x1, y1, x2, y2 in rects:

        # If this highlight ID is different to previous ones, reset the text pieces
        if hId != current_highlight_id:
            if current_highlight_id != -1:
                document_highlights.append(" ".join(current_highlight))

            current_highlight_id = hId
            current_highlight = []

        m_page = page - 1
        pdf.load(m_page)

        # If the exact match is missing we need to extract text
        results = extract(pdf, m_page, x1, y1, x2, y2)
        section = results['section']

        if section:
            current_highlight.append(section.text())

        else:
            pdf_unmerged.load(m_page)
            results   = extract(pdf, m_page, x1, y1, x2, y2, False)
            results_u = extract_unmerged(pdf_unmerged, m_page, x1, y1, x2, y2)

            # Extract the highlighted substring
            substr = substring(results['section'].text(), results_u['chars'].text())
            current_highlight.append(substr)

        overlap = 'LTTextLineHorizontal:overlaps_bbox("%f, %f, %f, %f")' % (x1, y1, x2, y2)

    with open(txt, 'w') as f:
        output = "-- %s" % ("\n-- ".join(document_highlights), )
        f.write(output.replace('- ', '').encode('utf-8'))
