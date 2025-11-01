# 📊 AutomateExcelTasks - Excel Report Automation System

[English](#english) | [Русский](#russian)

---

## English

### 🎯 Project Purpose

This web application automates the consolidation of weekly Excel reports into monthly summaries with automatic data aggregation. Designed for organizations that need to:

- Collect weekly reports from multiple sources
- Automatically merge data into monthly reports
- Maintain exact template formatting (colors, borders, merged cells)
- Sum numerical values across weeks
- Track upload history in a database
- Support bilingual interface (Russian/Uzbek)

**Use Case:** Government agencies, corporate departments, or any organization requiring systematic weekly-to-monthly Excel report consolidation with data accumulation.

### ✨ Features

- 📤 **Upload weekly Excel files** via web interface
- ➕ **Automatic data summation** - numerical values are added together
- 🎨 **Perfect formatting preservation** - colors, borders, and table structures maintained
- 💾 **Database storage** - files stored in SQLite for easy backup
- 🌐 **Bilingual interface** - Russian and Uzbek (switchable)
- 🎭 **Company logo** display
- ⏳ **Loading animations** with "Please wait..." message
- 📥 **Download monthly reports** with all formatting intact
- 🗑️ **Delete reports** with confirmation
- 📊 **Statistics** showing row counts and upload history

### 🛠️ Technology Stack

- **Backend:** Python 3.8+, Flask 3.0.3
- **Excel Processing:** xlwings 0.32.1 (COM API for perfect formatting)
- **Database:** SQLite3
- **Frontend:** Vanilla JavaScript, CSS3
- **i18n:** Custom localization system

### 📋 Requirements

- Python 3.8 or higher
- Microsoft Excel (for xlwings COM integration)
- Windows OS (required for xlwings)

### 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AutomateExcelTasks.git
cd AutomateExcelTasks
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Place your template:**
   - Put your monthly report template in: `static/file/Шаблон.xlsx`
   - The template must have your desired formatting (colors, borders, merged cells)

4. **Run the application:**
```bash
python app.py
```
Or simply double-click `start.bat`

5. **Open in browser:**
```
http://localhost:5000
```

### 📖 How It Works

#### Template-Based Processing

1. **Monthly template** (`static/file/Шаблон.xlsx`) contains:
   - Rows 1-7: Headers with formatting (colors, borders, merged cells)
   - Rows 8+: Data area (empty in template)

2. **Weekly files** must have the same structure as the template

3. **Processing logic:**
   - First upload: Creates copy of template → fills data from weekly file
   - Subsequent uploads: Loads existing monthly file → **sums numerical values** → updates text values

#### Data Aggregation Example

```
Week 1 upload:
Region KR: 5 cameras

Week 2 upload:
Region KR: 3 cameras

Monthly result:
Region KR: 8 cameras (5 + 3) ✅
```

### 🗄️ Database Schema

**monthly_reports table:**
- `id` - Primary key
- `month`, `year` - Period identifier
- `file_name` - Generated filename
- `file_data` - BLOB (Excel file stored in database)
- `created_at`, `updated_at` - Timestamps
- `total_rows` - Data row count

**weekly_uploads table:**
- `id` - Primary key
- `monthly_report_id` - Foreign key
- `original_filename` - Uploaded filename
- `file_path` - Temporary path
- `uploaded_at` - Timestamp
- `rows_added` - Rows processed

### 🌐 Localization

Switch between languages using **RU / UZ** buttons in header.

Supported languages:
- 🇷🇺 Russian
- 🇺🇿 Uzbek

All interface elements, months, and messages are translated.

### 📁 Project Structure

```
AutomateExcelTasks/
├── app.py                    # Flask application
├── database.py               # SQLite database operations
├── excel_processor.py        # Excel processing with xlwings
├── requirements.txt          # Python dependencies
├── uploads.db               # SQLite database (auto-created)
├── templates/
│   └── index.html           # Main HTML template
├── static/
│   ├── images/
│   │   └── favicon.svg      # Company logo
│   ├── file/
│   │   └── Шаблон.xlsx      # Monthly report template
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       ├── i18n.js          # Localization
│       └── script.js        # Main JavaScript
└── uploads/                 # Temporary weekly files
```

### 🔒 Security

- File type validation (.xlsx, .xls only)
- Secure filename handling
- File size limits (50MB)
- SQL injection protection
- XSS prevention

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 👨‍💻 Author

Developed by AI Assistant with Claude Sonnet 4.5

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- Flask framework
- xlwings library for Excel automation
- openpyxl for Excel file handling

---

## Russian

### 🎯 Назначение проекта

Веб-приложение для автоматизации объединения еженедельных Excel отчётов в месячные сводки с автоматическим суммированием данных. Предназначено для организаций, которым необходимо:

- Собирать еженедельные отчёты из разных источников
- Автоматически объединять данные в месячные отчёты
- Сохранять точное форматирование шаблона (цвета, границы, объединённые ячейки)
- Суммировать числовые значения по неделям
- Отслеживать историю загрузок в базе данных
- Поддерживать двуязычный интерфейс (русский/узбекский)

**Применение:** Государственные органы, корпоративные отделы, любые организации, требующие систематического объединения еженедельных Excel отчётов в месячные с накоплением данных.

### ✨ Возможности

- 📤 **Загрузка еженедельных Excel файлов** через веб-интерфейс
- ➕ **Автоматическое суммирование данных** - числовые значения складываются
- 🎨 **Идеальное сохранение форматирования** - цвета, границы и структура таблиц
- 💾 **Хранение в базе данных** - файлы в SQLite для простого резервного копирования
- 🌐 **Двуязычный интерфейс** - русский и узбекский (переключаемый)
- 🎭 **Логотип компании** в интерфейсе
- ⏳ **Анимация загрузки** с сообщением "Пожалуйста, подождите..."
- 📥 **Скачивание месячных отчётов** с сохранением форматирования
- 🗑️ **Удаление отчётов** с подтверждением
- 📊 **Статистика** по количеству строк и истории загрузок

### 🛠️ Технологии

- **Backend:** Python 3.8+, Flask 3.0.3
- **Обработка Excel:** xlwings 0.32.1 (COM API для идеального форматирования)
- **База данных:** SQLite3
- **Frontend:** Vanilla JavaScript, CSS3
- **Локализация:** Собственная система i18n

### 📋 Требования

- Python 3.8 или выше
- Microsoft Excel (для интеграции xlwings COM)
- Windows (требуется для xlwings)

### 🚀 Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/AutomateExcelTasks.git
cd AutomateExcelTasks
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Разместите шаблон:**
   - Поместите шаблон месячного отчёта в: `static/file/Шаблон.xlsx`
   - Шаблон должен содержать желаемое форматирование (цвета, границы, объединённые ячейки)

4. **Запустите приложение:**
```bash
python app.py
```
Или просто дважды кликните `start.bat`

5. **Откройте в браузере:**
```
http://localhost:5000
```

### 📖 Как это работает

#### Обработка на основе шаблона

1. **Шаблон месячного отчёта** (`static/file/Шаблон.xlsx`) содержит:
   - Строки 1-7: Заголовки с форматированием (цвета, границы, объединённые ячейки)
   - Строки 8+: Область данных (пустая в шаблоне)

2. **Еженедельные файлы** должны иметь ту же структуру что и шаблон

3. **Логика обработки:**
   - Первая загрузка: Создаётся копия шаблона → заполняются данные из недельного файла
   - Последующие загрузки: Загружается существующий месячный файл → **суммируются числовые значения** → обновляются текстовые значения

#### Пример агрегации данных

```
Загрузка недели 1:
Регион КР: 5 камер

Загрузка недели 2:
Регион КР: 3 камеры

Результат в месячном отчёте:
Регион КР: 8 камер (5 + 3) ✅
```

### 🗄️ Схема базы данных

**Таблица monthly_reports:**
- `id` - Первичный ключ
- `month`, `year` - Идентификатор периода
- `file_name` - Сгенерированное имя файла
- `file_data` - BLOB (Excel файл хранится в БД)
- `created_at`, `updated_at` - Временные метки
- `total_rows` - Количество строк данных

**Таблица weekly_uploads:**
- `id` - Первичный ключ
- `monthly_report_id` - Внешний ключ
- `original_filename` - Имя загруженного файла
- `file_path` - Временный путь
- `uploaded_at` - Временная метка
- `rows_added` - Обработанные строки

### 🌐 Локализация

Переключайте язык кнопками **RU / UZ** в заголовке.

Поддерживаемые языки:
- 🇷🇺 Русский
- 🇺🇿 Узбекский

Переводятся все элементы интерфейса, месяцы и сообщения.

### 🤝 Вклад в проект

Приветствуются любые предложения! Создавайте Pull Request.

### 👨‍💻 Автор

Разработано AI Assistant с использованием Claude Sonnet 4.5

### 📄 Лицензия

Проект распространяется под лицензией MIT - подробности в файле [LICENSE](LICENSE).

### 🙏 Благодарности

- Flask framework
- xlwings библиотека для автоматизации Excel
- openpyxl для работы с Excel файлами

---

## 📸 Screenshots

### Main Interface
![Main Interface](docs/screenshot-main.png)

### File Upload
![Upload](docs/screenshot-upload.png)

### Monthly Reports List
![Reports](docs/screenshot-reports.png)

---

## 🔧 Configuration

### Change template path

Edit `app.py` line 11:
```python
app.config['TEMPLATE_FILE'] = r'static\file\Шаблон.xlsx'
```

### Change port

Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Maximum file size

Edit `app.py` line 12:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 📞 Support

For issues or questions:
1. Check the documentation
2. Ensure template structure matches weekly files
3. Verify Excel is installed (required for xlwings)

---

**Version:** 4.0  
**Date:** November 2025  
**Status:** Production Ready ✅
