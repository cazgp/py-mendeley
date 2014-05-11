#!/usr/bin/python

from parser import get_args
from pdfquery import PDFQuery
from mendeley import Mendeley
from helpers import *

def main(m, dIds):
    highlights = []
    for d in dIds:
        hs = m.get_highlights(d)
        if len(hs):
            highlights.append((d, hs))

    for dId, hs in highlights:
        # Get the document and the Mendeley highlights
        path = m.get_file_path(dId)
        rects = m.get_highlight_rects(hs)

        # Load the pdf files, one merged and one not
        pdf = PDFQuery(path)
        pdf_unmerged = PDFQuery(path, merge_tags=('LTAnno'))

        # Get the author year title to call the saved txt file
        author, year, title = m.get_author_year_title(dId)

        # Append that info right at the start of the file
        document_highlights = ["* %s, %s - %s" % (author, year, title)]
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
                current_highlight.append(sanitize(section.text()))

            else:
                pdf_unmerged.load(m_page)
                results   = extract(pdf, m_page, x1, y1, x2, y2, False)
                results_u = extract_unmerged(pdf_unmerged, m_page, x1, y1, x2, y2)

                # Extract the highlighted substring
                substr = substring(results['section'].text(), results_u['chars'].text())
                current_highlight.append(sanitize(substr))

            overlap = 'LTTextLineHorizontal:overlaps_bbox("%f, %f, %f, %f")' % (x1, y1, x2, y2)

        org_name = "%s-%s-%s.org" % (author, year, title.replace(" ", "")[:10])
        with open(org_name, 'w') as f:
            output = "\n - ".join(document_highlights)
            f.write(output.encode('utf-8'))

if __name__ == "__main__":
    args = get_args()
    mendeley = Mendeley()

    if args.namespace == "document":
        dIds = mendeley.get_document(args.author, args.year, args.title)

    elif args.namespace == "folder":
        # Get all documents we wish to extract in folder
        dIds = mendeley.get_documents_in_folder(args.name, args.id)

    main(mendeley, dIds)
