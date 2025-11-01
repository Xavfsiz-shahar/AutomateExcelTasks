import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='uploads.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица для месячных отчетов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_data BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_rows INTEGER DEFAULT 0,
                UNIQUE(month, year)
            )
        ''')
        
        # Таблица для еженедельных загрузок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monthly_report_id INTEGER NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rows_added INTEGER DEFAULT 0,
                status TEXT DEFAULT 'success',
                FOREIGN KEY (monthly_report_id) REFERENCES monthly_reports(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_monthly_report(self, month, year, file_name, file_data):
        """Получить или создать месячный отчет"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM monthly_reports WHERE month = ? AND year = ?
        ''', (month, year))
        
        result = cursor.fetchone()
        
        if result:
            report_id = result[0]
            # Обновляем файл и время последнего изменения
            cursor.execute('''
                UPDATE monthly_reports 
                SET file_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (file_data, report_id))
        else:
            # Создаем новый отчет
            cursor.execute('''
                INSERT INTO monthly_reports (month, year, file_name, file_data)
                VALUES (?, ?, ?, ?)
            ''', (month, year, file_name, file_data))
            report_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return report_id
    
    def add_weekly_upload(self, monthly_report_id, original_filename, file_path, rows_added):
        """Добавить запись о еженедельной загрузке"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weekly_uploads (monthly_report_id, original_filename, file_path, rows_added)
            VALUES (?, ?, ?, ?)
        ''', (monthly_report_id, original_filename, file_path, rows_added))
        
        conn.commit()
        conn.close()
    
    def update_monthly_report_rows(self, report_id, total_rows):
        """Обновить количество строк в месячном отчете"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE monthly_reports SET total_rows = ? WHERE id = ?
        ''', (total_rows, report_id))
        
        conn.commit()
        conn.close()
    
    def get_weekly_uploads(self, month, year):
        """Получить все еженедельные загрузки для месяца"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT wu.id, wu.original_filename, wu.uploaded_at, wu.rows_added, wu.status
            FROM weekly_uploads wu
            JOIN monthly_reports mr ON wu.monthly_report_id = mr.id
            WHERE mr.month = ? AND mr.year = ?
            ORDER BY wu.uploaded_at DESC
        ''', (month, year))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'id': r[0], 'filename': r[1], 'uploaded_at': r[2], 
                 'rows_added': r[3], 'status': r[4]} for r in results]
    
    def get_all_monthly_reports(self):
        """Получить все месячные отчеты"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, month, year, file_name, created_at, updated_at, total_rows, length(file_data) as file_size
            FROM monthly_reports
            ORDER BY year DESC, month DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'id': r[0], 'month': r[1], 'year': r[2], 'file_name': r[3],
                 'created_at': r[4], 'updated_at': r[5], 'total_rows': r[6], 'file_size': r[7]} for r in results]
    
    def get_monthly_report_file(self, month, year):
        """Получить файл месячного отчета"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_name, file_data FROM monthly_reports WHERE month = ? AND year = ?
        ''', (month, year))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'file_name': result[0], 'file_data': result[1]}
        return None
    
    def delete_monthly_report(self, month, year):
        """Удалить месячный отчет"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM monthly_reports WHERE month = ? AND year = ?
        ''', (month, year))
        
        conn.commit()
        conn.close()
    
    def get_monthly_report_stats(self, month, year):
        """Получить статистику по месячному отчету"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                mr.total_rows,
                COUNT(wu.id) as uploads_count,
                mr.created_at,
                mr.updated_at
            FROM monthly_reports mr
            LEFT JOIN weekly_uploads wu ON mr.id = wu.monthly_report_id
            WHERE mr.month = ? AND mr.year = ?
            GROUP BY mr.id
        ''', (month, year))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_rows': result[0],
                'uploads_count': result[1],
                'created_at': result[2],
                'updated_at': result[3]
            }
        return None

