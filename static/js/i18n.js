// Переводы
const translations = {
    ru: {
        title: 'Система учёта отчётов',
        systemTitle: 'Система учёта отчётов',
        systemSubtitle: 'Автоматизация Excel отчётов',
        uploadWeekly: 'Загрузка еженедельного отчёта',
        month: 'Месяц:',
        year: 'Год:',
        file: 'Файл:',
        selectMonth: 'Выберите',
        january: 'Январь',
        february: 'Февраль',
        march: 'Март',
        april: 'Апрель',
        may: 'Май',
        june: 'Июнь',
        july: 'Июль',
        august: 'Август',
        september: 'Сентябрь',
        october: 'Октябрь',
        november: 'Ноябрь',
        december: 'Декабрь',
        supportedFormats: 'Поддерживаются форматы: .xlsx, .xls',
        upload: 'Загрузить',
        monthlyReports: 'Месячные отчёты',
        refresh: 'Обновить',
        loading: 'Загрузка...',
        download: 'Скачать',
        delete: 'Удалить',
        confirmDelete: 'Подтверждение удаления',
        deleteConfirmText: 'Вы уверены, что хотите удалить этот отчёт?',
        cancel: 'Отмена',
        footerText: 'Система учёта отчётов',
        pleaseWait: 'Пожалуйста, подождите...',
        dataRows: 'Строк данных',
        updated: 'Обновлён',
        noReports: 'Нет созданных отчётов.',
        uploadFirst: 'Загрузите первый еженедельный файл.'
    },
    uz: {
        title: 'Hisobot tizimi',
        systemTitle: 'Hisobot tizimi',
        systemSubtitle: 'Excel hisobotlarini avtomatlashtirish',
        uploadWeekly: 'Haftalik hisobotni yuklash',
        month: 'Oy:',
        year: 'Yil:',
        file: 'Fayl:',
        selectMonth: 'Tanlang',
        january: 'Yanvar',
        february: 'Fevral',
        march: 'Mart',
        april: 'Aprel',
        may: 'May',
        june: 'Iyun',
        july: 'Iyul',
        august: 'Avgust',
        september: 'Sentabr',
        october: 'Oktabr',
        november: 'Noyabr',
        december: 'Dekabr',
        supportedFormats: 'Qo\'llab-quvvatlanadigan formatlar: .xlsx, .xls',
        upload: 'Yuklash',
        monthlyReports: 'Oylik hisobotlar',
        refresh: 'Yangilash',
        loading: 'Yuklanmoqda...',
        download: 'Yuklab olish',
        delete: 'O\'chirish',
        confirmDelete: 'O\'chirishni tasdiqlash',
        deleteConfirmText: 'Ushbu hisobotni o\'chirishga ishonchingiz komilmi?',
        cancel: 'Bekor qilish',
        footerText: 'Hisobot tizimi',
        pleaseWait: 'Iltimos, kuting...',
        dataRows: 'Ma\'lumot qatorlari',
        updated: 'Yangilangan',
        noReports: 'Hisobotlar mavjud emas.',
        uploadFirst: 'Birinchi haftalik faylni yuklang.'
    }
};

// Текущий язык
let currentLang = localStorage.getItem('lang') || 'ru';

// Функция смены языка
function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    document.documentElement.lang = lang;
    
    // Обновляем все элементы с data-i18n
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    
    // Обновляем активную кнопку языка
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
    
    // Обновляем title страницы
    document.title = translations[lang].title;
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Устанавливаем язык
    setLanguage(currentLang);
    
    // Обработчики кнопок языка
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setLanguage(this.getAttribute('data-lang'));
        });
    });
});

// Функция получения перевода
function t(key) {
    return translations[currentLang][key] || key;
}

