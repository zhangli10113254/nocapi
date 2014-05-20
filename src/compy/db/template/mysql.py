# -*-  coding:UTF-8   -*-

'''
Created on 2014年4月11日

@author: zhangli
'''
from compy.db.template import DataAccessTemplate
from compy.db.errors import DataAccessError
import MySQLdb.cursors

class MySQLTemplate(DataAccessTemplate):
    def execute(self, sql, params = None):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            self.connection_commit(conn)
            return result
        except MySQLdb.Error as e:
            raise DataAccessError(*e.args)
        except Exception as e:
            info = dict(type = type(e), message = str(e.args))
            args = (-1, str(info))
            raise DataAccessError(*args)
        finally:
            if conn:
                self.release_connection(conn)
                
    def query(self, sql, params = None, cursor_call_back = None, cursor_class = None):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_class)
            cursor.execute(sql, params)
            self.connection_commit(conn)
            if not cursor_call_back:
                return cursor.fetchall()
            else:
                return cursor_call_back(cursor)
        except MySQLdb.Error as e:
            raise DataAccessError(*e.args)
        except Exception as e:
            info = dict(type = type(e), message = str(e.args))
            args = (-1, str(info))
            raise DataAccessError(*args)
        finally:
            if conn:
                self.release_connection(conn)
        
    def query_for_single_column(self, sql, params = None):
        def cursor_call_back(cursor):
            result = cursor.fetchone()
            if result and len(result) > 0:
                return result[0]
            return None
            
        return self.query(sql, params, cursor_call_back)
    
    def queryone_for_dict(self, sql, params = None):
        def cursor_call_back(cursor):
            result = cursor.fetchone()
            if result:
                return result
            return None
            
        return self.query(sql, params, cursor_call_back, cursor_class = MySQLdb.cursors.DictCursor)
    
    def query_for_dict(self, sql, params = None):
        def cursor_call_back(cursor):
            return cursor.fetchall()
            
        return self.query(sql, params, cursor_call_back, cursor_class = MySQLdb.cursors.DictCursor)
    
    def queryone_for_obj(self, sql, params = None, obj_class = dict, convertor = None):
        def cursor_call_back(cursor):
            result = cursor.fetchone()
            if result:
                if convertor:
                    return convertor(result)
                else:
                    return self._reflect_convert(result, obj_class)
            return None
            
        return self.query(sql, params, cursor_call_back, cursor_class = MySQLdb.cursors.DictCursor)
    
    def query_for_obj(self, sql, params = None, obj_class = dict, convertor = None):
        def cursor_call_back(cursor):
            results = cursor.fetchall()
            if results:
                obj_array = list()
                for result in results:
                    if convertor:
                        obj_array.append(convertor(result))
                    else:
                        obj_array.append(self._reflect_convert(result, obj_class))
                return obj_array
            return None
            
        return self.query(sql, params, cursor_call_back, cursor_class = MySQLdb.cursors.DictCursor)
    
    def update(self, sql, params = None):
        return self.execute(sql, params)
    
    def insert(self, sql, params = None):
        return self.execute(sql, params)
    
    def _reflect_convert(self, _d, _o_cls):
        _o = _o_cls()
        
        if isinstance(_o, dict):
            return _d
        
        if _d:
            for key in _d:
                if hasattr(_o, key):
                    setattr(_o, key, _d.get(key))
                    
        return _o