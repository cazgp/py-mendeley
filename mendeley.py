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

    def get_documents_in_folder(self, folder_id, recursive=False):
        query = "select documentId from DocumentFoldersBase where folderId=%d"
        return self.get_singlet(query % folder_id)

    def get_document_hash(self, dId):
        query = "select hash from DocumentFiles where documentId=%d"
        return self.get_singlet(query % dId)

    def get_highlights(self, dId):
        query = "select id from FileHighlights where documentId=%d"
        return self.get_singlet(query % dId)

    def get_singlet(self, query):
        return [item[0] for item in self.cursor.execute(query).fetchall()]

    def get_file_path(self, dId):
        query = "select localUrl from Files where hash = (select hash from DocumentFiles where documentId=%d)"
        path = self.get_singlet(query % dId)[0].replace('file://', '')
        return urllib2.unquote(path)

    def get_highlight_rects(self, hs):
        # Need to get the highlights *in order* which they may not actually be
        query = "select * from FileHighlightRects Where highlightId in (%s) ORDER BY page, y1 DESC, x1" 
        return self.cursor.execute(query % ",".join(map(str, hs))).fetchall()

    def get_author_year_title(self, dId):
        query =  'select lastname, year, substr(replace(title, " ", ""),0,10) from documentcontributors as dc join documents as d on dc.documentid = d.id where d.id = %d limit 1'
        res = self.cursor.execute(query % dId).fetchall()
        return "%s-%s-%s.txt" % res[0]