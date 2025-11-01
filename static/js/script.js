// Показать анимацию загрузки
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

// Скрыть анимацию загрузки
function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function() {
    // Элементы
    const uploadForm = document.getElementById('uploadForm');
    const monthSelect = document.getElementById('month');
    const yearInput = document.getElementById('year');
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const message = document.getElementById('message');
    const reportsContainer = document.getElementById('reportsContainer');
    const refreshBtn = document.getElementById('refreshBtn');
    
    // Устанавливаем текущий год и месяц
    const now = new Date();
    yearInput.value = now.getFullYear();
    monthSelect.value = now.getMonth() + 1;
    
    // Загружаем список отчётов
    loadReports();
    
    // Обработчик загрузки
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        const month = monthSelect.value;
        const year = yearInput.value;
        
        if (!file || !month || !year) {
            showMessage('Заполните все поля', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('month', month);
        formData.append('year', year);
        
        // Блокируем форму и показываем анимацию
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        showLoading();
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                const msg = currentLang === 'uz' ? data.message_uz : data.message_ru;
                showMessage(msg || data.message, 'success');
                uploadForm.reset();
                yearInput.value = now.getFullYear();
                monthSelect.value = now.getMonth() + 1;
                loadReports();
            } else {
                const errorMsg = currentLang === 'uz' ? 'Yuklashda xatolik' : 'Ошибка загрузки';
                showMessage(data.error || errorMsg, 'error');
            }
        } catch (error) {
            showMessage('Ошибка соединения с сервером', 'error');
        } finally {
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            hideLoading();
        }
    });
    
    // Обновление списка
    refreshBtn.addEventListener('click', loadReports);
    
    // Функции
    async function loadReports() {
        reportsContainer.innerHTML = '<div class="loading">Загрузка...</div>';
        
        try {
            const response = await fetch('/monthly-reports');
            const data = await response.json();
            
            if (response.ok && data.files && data.files.length > 0) {
                const reportsHTML = data.files.map(file => `
                    <div class="report-item">
                        <div class="excel-icon">
                            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="40" height="40" rx="4" fill="#217346"/>
                                <path d="M24 10H12C11.4477 10 11 10.4477 11 11V29C11 29.5523 11.4477 30 12 30H28C28.5523 30 29 29.5523 29 29V15L24 10Z" fill="#185C37"/>
                                <path d="M24 10V14C24 14.5523 24.4477 15 25 15H29L24 10Z" fill="#21A366"/>
                                <path d="M17 18L20 22L17 26M23 18L20 22L23 26" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div class="report-info">
                            <div class="report-name">${file.display_name}</div>
                            <div class="report-meta">
                                <span data-i18n="dataRows">${t('dataRows')}</span>: ${file.total_rows} | 
                                <span data-i18n="updated">${t('updated')}</span>: ${formatDate(file.updated)}
                            </div>
                        </div>
                        <div class="report-actions">
                            <button class="btn btn-download btn-small" onclick="downloadFile(${file.month}, ${file.year})">
                                <span data-i18n="download">${t('download')}</span>
                            </button>
                            <button class="btn btn-danger btn-small" onclick="confirmDelete(${file.month}, ${file.year}, '${file.display_name}')">
                                <span data-i18n="delete">${t('delete')}</span>
                            </button>
                        </div>
                    </div>
                `).join('');
                
                reportsContainer.innerHTML = `<div class="reports-list">${reportsHTML}</div>`;
            } else {
                reportsContainer.innerHTML = `
                    <div class="empty-state">
                        <span data-i18n="noReports">${t('noReports')}</span><br>
                        <span data-i18n="uploadFirst">${t('uploadFirst')}</span>
                    </div>
                `;
            }
        } catch (error) {
            reportsContainer.innerHTML = `
                <div class="empty-state">
                    ${currentLang === 'uz' ? 'Xatolik' : 'Ошибка загрузки списка отчётов'}
                </div>
            `;
        }
    }
    
    function showMessage(text, type) {
        message.textContent = text;
        message.className = `message ${type}`;
        
        setTimeout(() => {
            message.className = 'message';
        }, 5000);
    }
    
    function formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    // Глобальные функции
    window.downloadFile = function(month, year) {
        window.location.href = `/download/${month}/${year}`;
    };
    
    let fileToDelete = null;
    
    window.confirmDelete = function(month, year, displayName) {
        fileToDelete = {month, year};
        document.getElementById('deleteFileName').textContent = displayName;
        document.getElementById('confirmModal').style.display = 'block';
    };
    
    window.closeConfirmModal = function() {
        document.getElementById('confirmModal').style.display = 'none';
        fileToDelete = null;
    };
    
    document.getElementById('confirmDeleteBtn').addEventListener('click', async function() {
        if (!fileToDelete) return;
        
        try {
            const response = await fetch(`/delete/${fileToDelete.month}/${fileToDelete.year}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showMessage(data.message, 'success');
                closeConfirmModal();
                loadReports();
            } else {
                showMessage(data.error || 'Ошибка удаления', 'error');
            }
        } catch (error) {
            showMessage('Ошибка соединения с сервером', 'error');
        }
    });
    
    // Закрытие модального окна по клику вне него
    window.onclick = function(event) {
        const confirmModal = document.getElementById('confirmModal');
        
        if (event.target === confirmModal) {
            closeConfirmModal();
        }
    };
});
