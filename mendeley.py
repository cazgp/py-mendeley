import sqlite3
import urllib2
import yaml


class Mendeley:

    def __init__(self, *args, **kwargs):
        y = None
        with open('config.yaml') as config:
            y = yaml.safe_load(config)
        self.conn = sqlite3.connect(y['conn_str'])
        self.cursor = self.conn.cursor()

    def get_documents_in_folder(self, name=None, folder_id=None):
        query = "select documentId from DocumentFoldersBase where folderId=%s"

        if name:
            d = "(select id from Folders where name='%s')" % (name,)
        else:
            d = str(folder_id)
        return self.get_singlet(query % d)

    def get_document_hash(self, dId):
        query = "select hash from DocumentFiles where documentId=%d"
        return self.get_singlet(query % dId)

    def get_highlights(self, dId):
        query = "select id from FileHighlights where documentId=%d"
        return self.get_singlet(query % dId)

    def get_file_path(self, dId):
        query = "select localUrl from Files where hash = (select hash from DocumentFiles where documentId=%d)"
        path = self.get_singlet(query % dId)[0].replace('file://', '')
        return urllib2.unquote(path)

    def get_highlight_rects(self, hs):
        # Need to get the highlights *in order* which they may not actually be
        query = "select * from FileHighlightRects Where highlightId in (%s) ORDER BY page, y1 DESC, x1" 
        return self.cursor.execute(query % ",".join(map(str, hs))).fetchall()

    def get_author_year_title(self, dId):
        query =  'select lastname, year, title from documentcontributors as dc join documents as d on dc.documentid = d.id where d.id = %d limit 1'
        return self.cursor.execute(query % dId).fetchall()[0]

    def get_document(self, author, year, title):
        if title:
            query = "select id from documents where title=%s" % (title,)
        else:
            query = "select d.id from DocumentContributors as dc join documents as d on d.id = dc.documentId where lastName = '%s' and year='%s'" % (author, year)
        return self.get_singlet(query)

    def get_document_tags(self, dId):
        query = "select group_concat(tag, ':') from documenttags where documentid=%d"
        return self.cursor.execute(query % dId).fetchall()[0][0]

    def get_highlight_pages(self, dId):
        query = "select group_concat(distinct page) from filehighlightrects as fhr join filehighlights as fh on fhr.highlightid = fh.id where documentid=%d"
        results = map(lambda x: int(x) - 1, self.get_singlet(query % dId)[0].split(','))
        results.sort()
        return results

    def get_singlet(self, query):
        return [item[0] for item in self.cursor.execute(query).fetchall()]
