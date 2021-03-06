import sqlite3
import logging as log

# logger = log.getLogger(__name__)

class Sqlite3():
    def __init__(self):
        self.dbfile = self.maxfetchlen = None
        self.conn = self.cur = self.queries = None


    def init(self, dbfile=":memory:", maxfetchlen=0, queries=None):
        self.dbfile = dbfile 
        # max number of rows returned from select statement
        # zero means all
        self.maxfetchlen = maxfetchlen
        self.queries = queries

    def connect(self):
        err = None
        try:
            self.conn = sqlite3.connect(self.dbfile)
            log.info("Database %s opened.", self.dbfile)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            log.error(e)
            err = str(e)

        return err



    """
    returns the result, error.
    """
    def select (self, queryid, data=None, maxfetchlen=None): 
        log.info("queryid = %s", queryid)

        if not queryid in self.queries:
            return None, "sqlite_driver: Wrong queryid {}.".format(queryid)

        if maxfetchlen == None:
            maxfetchlen = self.maxfetchlen

        log.info("queryid=%s, query = [%s], data = [%s], maxfetchlen = [%s]", 
                queryid, self.queries[queryid], data, maxfetchlen)

        if data == None:
            self.cur.execute (self.queries[queryid]) 
        else:
            self.cur.execute (self.queries[queryid], data)

        if maxfetchlen == 0:
            return self.cur.fetchall(), None
        else:
            return self.cur.fetchmany(size=maxfetchlen), None


    """
    returns the rowcount, error
    """
    def modify (self, queryid, data=None):
        log.info("queryid = %s", queryid)

        if not queryid in self.queries:
            return None, "sqlite_driver: Wrong queryid {}.".format(queryid)

        log.info("queryid=%s, query = [%s], data = [%s]",
                queryid, self.queries[queryid], data)

        if data == None:
            self.cur.execute (self.queries[queryid]) 
        else:
            self.cur.execute (self.queries[queryid], data)

        self.conn.commit()

        return self.cur.rowcount, None


    def close (self):
        if self.conn != None:
            try:
                self.conn.close()
                log.info("Database %s closed.", self.dbfile)
                return None
            except sqlite3.Error as e:
                return str(e)


