def extract_unmerged(pdf, page, x1, y1, x2, y2):
    # Extract LTChar
    query  = ':in_bbox("%f, %f, %f, %f")' % (x1-1, y1-1, x2+5, y2+5)
    return pdf.extract([
        ('with_parent', 'LTPage[page_index="%d"]' % page),
        ('chars', 'LTChar' + query),
    ])

def extract(pdf, page, x1, y1, x2, y2, exact=True):
    if exact:
        query  = ':%s_bbox("%f, %f, %f, %f")' % ("in", x1-1, y1-1, x2+5, y2+5)
    else:
        query  = ':%s_bbox("%f, %f, %f, %f")' % ("overlaps", x1, y1, x2, y2)

    return pdf.extract([
        ('with_parent', 'LTPage[page_index="%d"]' % page),
        ('section', 'LTTextLineHorizontal' + query),
    ])


def substring(str1, str2):

    rep1 = str1.replace(" ", "")
    rep2 = str2.replace(" ", "")

    # Loop through first string array until index is found, then we know what the substring is and can extract
    arr = str1.split(" ")

    ind = rep1.index(rep2)

    curr_len = 0
    first_ind = 0

    for i, a in enumerate(arr):
        curr_len += len(a)
        if curr_len > ind:
            first_ind = i
            break

    ind += len(rep2)
    curr_len = 0
    last_ind = 0
    for i, a in enumerate(arr):
        curr_len += len(a)
        if curr_len > ind:
            last_ind = i
            break

    if last_ind == 0:
        last_ind = len(rep1) - 1

    return " ".join(arr[first_ind:last_ind])
