"""
Оптимизированная версия приложения для production
"""

import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import datetime

# Определяем какой процессор использовать
USE_DOCKER = os.getenv('USE_DOCKER', 'false').lower() == 'true'

if USE_DOCKER:
    from excel_processor_docker import ExcelProcessor
else:
    from excel_processor import ExcelProcessor

from database import Database

app = Flask(__name__)

# Конфигурация
app.config.update(
    UPLOAD_FOLDER='uploads',
    TEMPLATE_FILE=os.getenv('TEMPLATE_FILE', r'static\file\Шаблон.xlsx'),
    MAX_CONTENT_LENGTH=50 * 1024 * 1024,
    ALLOWED_EXTENSIONS={'xlsx', 'xls'},
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production'),
    JSON_AS_ASCII=False  # Для корректной работы с кириллицей
)

# Создание папок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# БД
db_path = os.getenv('DATABASE_PATH', 'uploads.db')
db = Database(db_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Валидация
        if 'file' not in request.files:
            return jsonify({'error': 'Файл не выбран'}), 400
        
        file = request.files['file']
        month = request.form.get('month')
        year = request.form.get('year')
        
        if not file or file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Разрешены только .xlsx, .xls'}), 400
        
        if not month or not year:
            return jsonify({'error': 'Укажите месяц и год'}), 400
        
        if not os.path.exists(app.config['TEMPLATE_FILE']):
            return jsonify({'error': 'Шаблон не найден'}), 400
        
        # Сохранение временного файла
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        weekly_file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], 
            f'{timestamp}_{filename}'
        )
        file.save(weekly_file_path)
        
        # Получение существующего отчёта
        existing_report = db.get_monthly_report_file(int(month), int(year))
        existing_data = existing_report['file_data'] if existing_report else None
        
        # Обработка
        processor = ExcelProcessor(template_path=app.config['TEMPLATE_FILE'])
        monthly_filename, file_data, rows_updated = processor.process_weekly_file(
            weekly_file_path, month, year, existing_data
        )
        
        # Сохранение в БД
        monthly_report_id = db.get_or_create_monthly_report(
            int(month), int(year), monthly_filename, file_data
        )
        db.add_weekly_upload(monthly_report_id, filename, weekly_file_path, rows_updated)
        
        # Статистика
        stats = processor.get_monthly_stats(file_data)
        db.update_monthly_report_rows(monthly_report_id, stats['total_rows'])
        
        db_stats = db.get_monthly_report_stats(int(month), int(year))
        
        # Очистка временного файла
        if os.path.exists(weekly_file_path):
            os.remove(weekly_file_path)
        
        return jsonify({
            'success': True,
            'message_ru': f'Файл успешно обработан. Обновлено {rows_updated} строк.',
            'message_uz': f'Fayl muvaffaqiyatli qayta ishlandi. {rows_updated} ta qator yangilandi.',
            'monthly_file': monthly_filename,
            'stats': {
                'rows_updated': rows_updated,
                'total_rows': stats['total_rows'],
                'uploads_count': db_stats['uploads_count'] if db_stats else 1
            }
        })
    
    except Exception as e:
        if 'weekly_file_path' in locals() and os.path.exists(weekly_file_path):
            os.remove(weekly_file_path)
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@app.route('/download/<int:month>/<int:year>')
def download_file(month, year):
    try:
        report = db.get_monthly_report_file(month, year)
        
        if not report:
            return jsonify({'error': 'Файл не найден'}), 404
        
        file_stream = io.BytesIO(report['file_data'])
        file_stream.seek(0)
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=report['file_name'],
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@app.route('/monthly-reports')
def get_monthly_reports():
    try:
        reports = db.get_all_monthly_reports()
        
        month_names = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        
        files = []
        for report in reports:
            files.append({
                'month': report['month'],
                'year': report['year'],
                'display_name': f"{month_names.get(report['month'], report['month'])} {report['year']}",
                'size': report['file_size'],
                'created': report['created_at'],
                'updated': report['updated_at'],
                'total_rows': report['total_rows']
            })
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@app.route('/delete/<int:month>/<int:year>', methods=['DELETE'])
def delete_report(month, year):
    try:
        report = db.get_monthly_report_file(month, year)
        if not report:
            return jsonify({'error': 'Файл не найден'}), 404
        
        db.delete_monthly_report(month, year)
        return jsonify({'success': True, 'message': 'Файл успешно удалён'})
    except Exception as e:
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    # Production mode
    if os.getenv('FLASK_ENV') == 'production':
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        
    app.run(
        debug=os.getenv('FLASK_ENV') != 'production',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )

