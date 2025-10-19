/**
 * SQL Agent Frontend Application
 * Clean Code Architecture - Frontend JavaScript
 */

class SQLAgentApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.elements = this.initializeElements();
        this.state = this.initializeState();
        this.bindEvents();
        this.initializeApp();
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        const elements = {
            // Database connection elements
            dbConnInput: document.getElementById('db_conn'),
            dbDriverInput: document.getElementById('db_driver'),
            dbServerInput: document.getElementById('db_server'),
            dbDatabaseInput: document.getElementById('db_database'),
            dbUsernameInput: document.getElementById('db_username'),
            dbPasswordInput: document.getElementById('db_password'),
            setDbBtn: document.getElementById('set-db-btn'),
            clearDbBtn: document.getElementById('clear-db-btn'),
            dbStatus: document.getElementById('db-status'),
            
            // Table selection elements
            tableSelect: document.getElementById('table_name'),
            
            // Schema elements
            columnsDiv: document.getElementById('columns'),
            
            // Query elements
            questionTextarea: document.getElementById('question'),
            sendQueryBtn: document.getElementById('send-query-btn'),
            clearBtn: document.getElementById('clear-btn'),
            
            // Results elements
            resultsDiv: document.getElementById('results'),
            
            // Navigation elements
            navBtns: document.querySelectorAll('.nav-btn'),
            pageContents: document.querySelectorAll('.page-content'),
            
            // Saved queries elements
            refreshQueriesBtn: document.getElementById('refresh-queries-btn'),
            exportQueriesBtn: document.getElementById('export-queries-btn'),
            clearAllQueriesBtn: document.getElementById('clear-all-queries-btn'),
            savedQueriesList: document.getElementById('saved-queries-list'),
            
            // Dashboard elements
            querySelector: document.getElementById('query-selector'),
            chartTypeBtns: document.querySelectorAll('.chart-type-btn'),
            createChartBtn: document.getElementById('create-chart-btn'),
            dashboardChart: document.getElementById('dashboard-chart'),
            chartContainer: document.getElementById('chart-container'),
            chartInfo: document.getElementById('chart-info'),
            chartDetails: document.getElementById('chart-details'),
            
            // Reports elements
            reportQuestion: document.getElementById('report-question'),
            reportTables: document.getElementById('report-tables'),
            reportChartType: document.getElementById('report-chart-type'),
            generateReportBtn: document.getElementById('generate-report-btn'),
            reportResultsDiv: document.getElementById('report-results'),
            reportChart: document.getElementById('report-chart'),

            // Scheduled queries elements
            scheduledQuestion: document.getElementById('scheduled-question'),
            scheduledTables: document.getElementById('scheduled-tables'),
            scheduleType: document.getElementById('schedule-type'),
            scheduleTime: document.getElementById('schedule-time'),
            scheduleDay: document.getElementById('schedule-day'),
            scheduleMonthDay: document.getElementById('schedule-month-day'),
            timeInputGroup: document.getElementById('time-input-group'),
            dayInputGroup: document.getElementById('day-input-group'),
            monthDayInputGroup: document.getElementById('month-day-input-group'),
            createScheduledBtn: document.getElementById('create-scheduled-btn'),
            refreshScheduledBtn: document.getElementById('refresh-scheduled-btn'),
            scheduledQueriesList: document.getElementById('scheduled-queries-list')
        };

        // Debug: Check for missing elements (only log if element is actually missing)
        for (const [name, element] of Object.entries(elements)) {
            if (!element) {
                console.warn(`Element not found: ${name} - Bu element opsiyonel olabilir`);
            }
        }

        return elements;
    }

    /**
     * Initialize application state
     */
    initializeState() {
        return {
            isConnected: false,
            selectedTables: [],
            isLoading: false,
            currentChart: null,
            selectedChartType: null,
            selectedQueryId: null
        };
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Core elements
        if (this.elements.setDbBtn) {
            this.elements.setDbBtn.addEventListener('click', () => this.setDatabaseConnection());
        }
        if (this.elements.tableSelect) {
            this.elements.tableSelect.addEventListener('change', () => this.loadColumns());
        }
        if (this.elements.clearDbBtn) {
            this.elements.clearDbBtn.addEventListener('click', () => this.clearDatabaseCredentials());
        }
        if (this.elements.sendQueryBtn) {
            this.elements.sendQueryBtn.addEventListener('click', () => this.sendQuery());
        }
        if (this.elements.clearBtn) {
            this.elements.clearBtn.addEventListener('click', () => this.clearResults());
        }
        
        // Page navigation
        this.elements.navBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchPage(e.target.dataset.page));
        });
        
        // Saved queries (opsiyonel elementler)
        if (this.elements.refreshQueriesBtn) {
            this.elements.refreshQueriesBtn.addEventListener('click', () => this.loadSavedQueries());
        }
        if (this.elements.exportQueriesBtn) {
            this.elements.exportQueriesBtn.addEventListener('click', () => this.exportQueriesToFile());
        }
        if (this.elements.clearAllQueriesBtn) {
            this.elements.clearAllQueriesBtn.addEventListener('click', () => this.clearAllQueries());
        }
        
        // Enable/disable query button based on state
        if (this.elements.questionTextarea) {
            this.elements.questionTextarea.addEventListener('input', () => this.updateQueryButtonState());
        }
        if (this.elements.tableSelect) {
            this.elements.tableSelect.addEventListener('change', () => this.updateQueryButtonState());
        }
        
        // Dashboard events
        if (this.elements.querySelector) {
            this.elements.querySelector.addEventListener('change', async (e) => {
                this.state.selectedQueryId = e.target.value;
                // Reset chart type selection; user must pick
                this.state.selectedChartType = null;
                this.updateCreateChartButtonState();
                // Compute and show recommended chart without creating it
                if (this.state.selectedQueryId) {
                    await this.showRecommendedChartForSelectedQuery();
                } else {
                    this.highlightRecommendedChart(null);
                }
            });
        }
        
        if (this.elements.chartTypeBtns) {
            this.elements.chartTypeBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    this.selectChartType(e.target.dataset.chartType);
                });
            });
        }
        
        if (this.elements.createChartBtn) {
            this.elements.createChartBtn.addEventListener('click', () => this.createChart());
        }

        // Reports events
        if (this.elements.reportQuestion) {
            this.elements.reportQuestion.addEventListener('input', () => this.updateGenerateReportButtonState());
        }
        if (this.elements.reportTables) {
            this.elements.reportTables.addEventListener('change', () => this.updateGenerateReportButtonState());
        }
        if (this.elements.generateReportBtn) {
            this.elements.generateReportBtn.addEventListener('click', () => this.generateReport());
        }
        
        // Scheduled queries events
        if (this.elements.scheduleType) {
            this.elements.scheduleType.addEventListener('change', () => this.updateScheduleInputs());
        }
        
        if (this.elements.scheduledQuestion) {
            this.elements.scheduledQuestion.addEventListener('input', () => this.updateCreateScheduledButtonState());
        }
        
        if (this.elements.scheduledTables) {
            this.elements.scheduledTables.addEventListener('change', () => this.updateCreateScheduledButtonState());
        }
        
        if (this.elements.createScheduledBtn) {
            this.elements.createScheduledBtn.addEventListener('click', () => this.createScheduledQuery());
        }
        
        if (this.elements.refreshScheduledBtn) {
            this.elements.refreshScheduledBtn.addEventListener('click', () => this.loadScheduledQueries());
        }
    }

    async clearDatabaseCredentials() {
        this.setLoading(true);
        this.showStatus('Bağlantı bilgileri temizleniyor...', 'info');
        try {
            const response = await this.apiCall('/clear_db', 'POST', {});
            if (response.success) {
                // Reset state and UI
                this.state.isConnected = false;
                if (this.elements.dbPasswordInput) this.elements.dbPasswordInput.value = '';
                if (this.elements.dbConnInput) this.elements.dbConnInput.value = '';
                if (this.elements.dbServerInput) this.elements.dbServerInput.value = '';
                if (this.elements.dbDatabaseInput) this.elements.dbDatabaseInput.value = '';
                if (this.elements.dbUsernameInput) this.elements.dbUsernameInput.value = '';
                // Disable dependent UI
                if (this.elements.tableSelect) {
                    this.elements.tableSelect.innerHTML = '<option value="">Önce veritabanı bağlantısını kurun</option>';
                    this.elements.tableSelect.disabled = true;
                }
                if (this.elements.reportTables) {
                    this.elements.reportTables.innerHTML = '<option value="">Önce veritabanı bağlantısını kurun</option>';
                    this.elements.reportTables.disabled = true;
                }
                // Clear results and pages that depend on connection
                if (this.elements.resultsDiv) {
                    this.elements.resultsDiv.innerHTML = '<p class="placeholder">Sorgu sonuçları burada görünecek</p>';
                }
                if (this.elements.savedQueriesList) {
                    this.elements.savedQueriesList.innerHTML = `
                        <div class="no-saved-queries">
                            <div class="no-saved-queries-icon">🔌</div>
                            <p>Önce veritabanı bağlantısını kurun</p>
                        </div>`;
                }
                if (this.elements.reportResultsDiv) {
                    this.elements.reportResultsDiv.innerHTML = '<p class="placeholder">Rapor sonucu burada görünecek</p>';
                }
                if (this.elements.generateReportBtn) {
                    this.elements.generateReportBtn.disabled = true;
                }
                if (this.elements.querySelector) {
                    this.elements.querySelector.innerHTML = '<option value="">Önce sorgu seçin...</option>';
                }
                if (this.elements.createChartBtn) {
                    this.elements.createChartBtn.disabled = true;
                }
                if (this.elements.scheduledQueriesList) {
                    this.elements.scheduledQueriesList.innerHTML = `
                        <p class="placeholder">Önce veritabanı bağlantısını kurun</p>`;
                }
                if (this.elements.dashboardChart) {
                    this.elements.dashboardChart.style.display = 'none';
                }
                this.showStatus('Bağlantı bilgileri temizlendi', 'success');
            } else {
                this.showStatus(`Temizleme hatası: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Temizleme hatası: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Initialize application
     */
    async initializeApp() {
        this.showStatus('Uygulama başlatılıyor...', 'info');
        // App is ready, no initial database connection needed
        this.showStatus('Veritabanı bağlantısı kurulmasını bekliyor...', 'info');
        
        // Load saved queries if database is connected and element exists
        if (this.state.isConnected && this.elements.savedQueriesList) {
            await this.loadSavedQueries();
        }

        // If reports tables select exists and we are connected later, it will be enabled in setDatabaseConnection
    }

    /**
     * Set database connection
     */
    async setDatabaseConnection() {
        const driver = (this.elements.dbDriverInput && this.elements.dbDriverInput.value.trim()) || '';
        const server = (this.elements.dbServerInput && this.elements.dbServerInput.value.trim()) || '';
        const database = (this.elements.dbDatabaseInput && this.elements.dbDatabaseInput.value.trim()) || '';
        const username = (this.elements.dbUsernameInput && this.elements.dbUsernameInput.value.trim()) || '';
        const password = (this.elements.dbPasswordInput && this.elements.dbPasswordInput.value) || '';
        const connectionString = this.elements.dbConnInput ? this.elements.dbConnInput.value.trim() : '';

        // Prefer field-based secure submission; fallback to full DSN if fields are empty
        let payload = null;
        if (server && database && username && password) {
            payload = {
                driver: driver || 'ODBC Driver 17 for SQL Server',
                server,
                database,
                uid: username,
                pwd: password
            };
        } else if (connectionString) {
            payload = { db_conn_str: connectionString };
        } else {
            this.showStatus('Lütfen server, database, username ve password girin veya DSN sağlayın', 'error');
            return;
        }

        this.setLoading(true);
        this.showStatus('Veritabanı bağlantısı kuruluyor...', 'info');

        try {
            const response = await this.apiCall('/set_db', 'POST', payload);

            if (response.success) {
                this.state.isConnected = true;
                this.showStatus('Veritabanı bağlantısı başarılı!', 'success');
                // Clear password input in UI memory for safety
                if (this.elements.dbPasswordInput) this.elements.dbPasswordInput.value = '';
                this.elements.tableSelect.disabled = false;
                if (this.elements.reportTables) {
                    this.elements.reportTables.disabled = false;
                }
                await this.loadTables();
                await this.populateReportTables();
                // Load saved queries after connection if element exists
                if (this.elements.savedQueriesList) {
                    await this.loadSavedQueries();
                }
            } else {
                this.showStatus(`Bağlantı hatası: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Bağlantı hatası: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Load tables from database
     */
    async loadTables() {
        if (!this.state.isConnected) {
            this.showStatus('Önce veritabanı bağlantısını kurun', 'error');
            return;
        }

        try {
            const response = await this.apiCall('/tables', 'GET');
            
            if (response.success) {
                this.populateTableSelect(response.data);
                this.showStatus(`${response.data.length} tablo yüklendi`, 'success');
            } else {
                this.showStatus(`Tablo yükleme hatası: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Tablo yükleme hatası: ${error.message}`, 'error');
        }
    }

    /**
     * Populate report tables select
     */
    async populateReportTables() {
        if (!this.elements.reportTables || !this.state.isConnected) return;
        try {
            const response = await this.apiCall('/tables', 'GET');
            if (response.success) {
                this.elements.reportTables.innerHTML = '';
                response.data.forEach(table => {
                    const option = document.createElement('option');
                    option.value = table;
                    option.textContent = table;
                    this.elements.reportTables.appendChild(option);
                });
            }
        } catch (e) {
            // ignore
        }
    }

    /**
     * Populate table select element
     */
    populateTableSelect(tables) {
        this.elements.tableSelect.innerHTML = '';
        
        if (tables.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Veritabanında tablo bulunamadı';
            this.elements.tableSelect.appendChild(option);
            return;
        }

        tables.forEach(table => {
            const option = document.createElement('option');
            option.value = table;
            option.textContent = table;
            this.elements.tableSelect.appendChild(option);
        });
    }

    /**
     * Load columns for selected tables
     */
    async loadColumns() {
        const selectedOptions = Array.from(this.elements.tableSelect.selectedOptions);
        const selectedTables = selectedOptions.map(option => option.value);
        
        this.state.selectedTables = selectedTables;

        if (selectedTables.length === 0) {
            this.elements.columnsDiv.innerHTML = '<p class="placeholder">Tablolar seçildiğinde kolonlar burada görünecek</p>';
            return;
        }

        try {
            const response = await this.apiCall('/columns', 'POST', {
                tables: selectedTables
            });

            if (response.success) {
                this.displayColumns(response.data);
            } else {
                this.showStatus(`Kolon yükleme hatası: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Kolon yükleme hatası: ${error.message}`, 'error');
        }
    }

    /**
     * Display columns information
     */
    displayColumns(columnsData) {
        let html = '';
        
        for (const [tableName, columns] of Object.entries(columnsData)) {
            html += `
                <div class="table-schema">
                    <h4>📋 ${tableName}</h4>
                    <div class="columns-list">
                        ${columns.map(col => `<span class="column-tag">${col}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        this.elements.columnsDiv.innerHTML = html;
    }

    /**
     * Reports: enable/disable button
     */
    updateGenerateReportButtonState() {
        if (!this.elements.generateReportBtn) return;
        const hasQuestion = this.elements.reportQuestion && this.elements.reportQuestion.value.trim().length > 0;
        const hasTables = this.elements.reportTables && this.elements.reportTables.selectedOptions.length > 0;
        const isConnected = this.state.isConnected;
        this.elements.generateReportBtn.disabled = !(hasQuestion && hasTables && isConnected);
    }

    /**
     * Generate report via backend
     */
    async generateReport() {
        const question = this.elements.reportQuestion.value.trim();
        const tables = Array.from(this.elements.reportTables.selectedOptions).map(o => o.value);
        const preferredChart = this.elements.reportChartType.value;
        const explainOnly = preferredChart === 'auto' && tables.length > 0 && question.length > 0 && (question.toLowerCase().includes('özet') || question.toLowerCase().includes('açıkla') || question.toLowerCase().includes('rapor öner'));

        if (!question || tables.length === 0) return;

        this.setLoading(true);
        this.showStatus('Rapor oluşturuluyor...', 'info');
        try {
            const response = await this.apiCall('/report', 'POST', {
                question,
                tables,
                preferred_chart: preferredChart,
                explain_only: explainOnly
            });

            if (response.success) {
                // If explanation-only
                if (response.data && response.data.summary) {
                    this.elements.reportResultsDiv.innerHTML = `
                        <div class="result-section">
                            <div class="sql-query"><strong>SQL:</strong><pre>${response.data.sql}</pre></div>
                            <div class="message-result">
                                <p><strong>Kısa Açıklama:</strong> ${this.escapeHtml(response.data.summary)}</p>
                                ${response.data.analysis ? `<p style="margin-top:8px;"><strong>Analiz:</strong> ${this.escapeHtml(response.data.analysis)}</p>` : ''}
                            </div>
                        </div>`;
                    // Hide chart
                    if (this.elements.reportChart) this.elements.reportChart.style.display = 'none';
                } else if (response.data && (response.data.results || response.data.sql)) {
                    // Show results if available, otherwise show SQL and analysis
                    if (response.data.results && response.data.results.length > 0) {
                        this.displayReportResults(response.data.results, response.data.sql, response.data.summary, response.data.analysis);
                    } else {
                        // No results but we have SQL - show SQL and analysis
                        this.displayReportResults([], response.data.sql, response.data.summary, response.data.analysis);
                    }
                    
                    // Render chart if chartData provided
                    if (response.data.chartData) {
                        this.renderReportChart(response.data.chartData, response.data.chartType || 'bar');
                    }
                } else {
                    this.elements.reportResultsDiv.innerHTML = `
                        <div class="result-section">
                            <div class="no-results">
                                <p>📊 Rapor oluşturuldu ancak sonuç bulunamadı.</p>
                                <p>Bu durum normal olabilir - sorgunuzun kriterlerine uygun veri bulunmuyor olabilir.</p>
                            </div>
                        </div>`;
                }
                this.showStatus('Rapor oluşturuldu', 'success');
            } else {
                this.elements.reportResultsDiv.innerHTML = `
                    <div class="result-section">
                        <div class="error-result">
                            <h3>❌ Rapor Oluşturulamadı</h3>
                            <p><strong>Hata:</strong> ${this.escapeHtml(response.error)}</p>
                            <p>Lütfen sorunuzu kontrol edin ve tekrar deneyin.</p>
                        </div>
                    </div>`;
                this.showStatus('Rapor oluşturulamadı', 'error');
            }
        } catch (error) {
            this.elements.reportResultsDiv.innerHTML = `
                <div class="result-section">
                    <div class="error-result">
                        <h3>❌ Bağlantı Hatası</h3>
                        <p><strong>Hata:</strong> ${this.escapeHtml(error.message)}</p>
                        <p>Veritabanı bağlantısını kontrol edin ve tekrar deneyin.</p>
                    </div>
                </div>`;
            this.showStatus('Bağlantı hatası', 'error');
        } finally {
            this.setLoading(false);
            this.updateGenerateReportButtonState();
        }
    }

    displayReportResults(results, sql, summary = null, analysis = null) {
        // Reuse displayTableResults layout
        if (!results || results.length === 0) {
            this.elements.reportResultsDiv.innerHTML = `
                <div class="result-section">
                    <div class="sql-query">
                        <strong>SQL:</strong>
                        <pre>${sql}</pre>
                    </div>
                    <div class="no-results">
                        <p>📊 Sorgu başarıyla çalıştırıldı ancak sonuç bulunamadı.</p>
                        <p>Bu durum normal olabilir - sorgunuzun kriterlerine uygun veri bulunmuyor olabilir.</p>
                    </div>
                    <div class="message-result" style="margin-top:12px; background-color: #f0f8ff; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff;">
                        ${summary && summary.trim() ? `<p><strong>Kısa Özet:</strong> ${this.escapeHtml(summary)}</p>` : '<p><strong>Kısa Özet:</strong> Sorgu başarıyla çalıştırıldı ancak sonuç bulunamadı. Bu durum normal olabilir.</p>'}
                        ${analysis && analysis.trim() ? `<p style="margin-top:8px;"><strong>Analiz:</strong> ${this.escapeHtml(analysis)}</p>` : '<p style="margin-top:8px;"><strong>Analiz:</strong> Sorgunuzun kriterlerine uygun veri bulunmuyor olabilir. Farklı kriterler deneyebilirsiniz.</p>'}
                    </div>
                </div>`;
            return;
        }
        const headers = Object.keys(results[0]);
        const tableRows = results.map(row => 
            `<tr>${headers.map(header => `<td>${this.escapeHtml(String(row[header] ?? ''))}</td>`).join('')}</tr>`
        ).join('');
        this.elements.reportResultsDiv.innerHTML = `
            <div class="result-section">
                <div class="sql-query">
                    <strong>SQL:</strong>
                    <pre>${sql}</pre>
                </div>
                <div class="table-container">
                    <table class="results-table">
                        <thead>
                            <tr>${headers.map(h => `<th>${this.escapeHtml(h)}</th>`).join('')}</tr>
                        </thead>
                        <tbody>
                            ${tableRows}
                        </tbody>
                    </table>
                </div>
                <div class="message-result" style="margin-top:12px; background-color: #f0f8ff; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff;">
                    ${summary && summary.trim() ? `<p><strong>Kısa Özet:</strong> ${this.escapeHtml(summary)}</p>` : '<p><strong>Kısa Özet:</strong> Bu sorgu sonuçları tabloda gösteriliyor. Verilerinizi analiz ederek önemli trendleri görebilirsiniz.</p>'}
                    ${analysis && analysis.trim() ? `<p style="margin-top:8px;"><strong>Analiz:</strong> ${this.escapeHtml(analysis)}</p>` : '<p style="margin-top:8px;"><strong>Analiz:</strong> Sorgu sonuçlarına göre verilerinizde önemli bilgiler bulunuyor. Grafik görselleştirmesi de mevcut sonuçları daha iyi anlamanıza yardımcı olacaktır.</p>'}
                </div>
            </div>
        `;
    }

    renderReportChart(chartData, chartType) {
        const canvas = this.elements.reportChart;
        if (!canvas) return;
        canvas.style.display = 'block';
        const ctx = canvas.getContext('2d');
        if (this.reportChartInstance) {
            this.reportChartInstance.destroy();
        }
        const config = this.getChartConfig(chartData, chartType);
        this.reportChartInstance = new Chart(ctx, config);
    }
    /**
     * Send query to backend
     */
    async sendQuery() {
        const question = this.elements.questionTextarea.value.trim();
        const selectedTables = this.state.selectedTables;

        if (!question) {
            this.showStatus('Lütfen bir soru girin', 'error');
            return;
        }

        if (selectedTables.length === 0) {
            this.showStatus('Lütfen en az bir tablo seçin', 'error');
            return;
        }

        this.setLoading(true);
        this.showStatus('Sorgu işleniyor...', 'info');

        try {
            const response = await this.apiCall('/query', 'POST', {
                question: question,
                tables: selectedTables
            });

            this.displayResults(response);
            
            if (response.success) {
                this.showStatus('Sorgu başarıyla çalıştırıldı', 'success');
            } else {
                this.showStatus(`Sorgu hatası: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Sorgu hatası: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    /**
     * Display query results
     */
    displayResults(response) {
        if (response.success) {
            if (response.results) {
                // SELECT query results
                this.displayTableResults(response.results, response.sql);
            } else if (response.message) {
                // Non-SELECT query results
                this.displayMessageResult(response.message, response.sql);
            }
        } else {
            // Error results
            this.displayErrorResult(response.error, response.sql);
        }
    }

    /**
     * Display table results
     */
    displayTableResults(results, sql) {
        if (results.length === 0) {
            this.elements.resultsDiv.innerHTML = `
                <div class="result-section">
                    <h3>📊 Sorgu Sonuçları</h3>
                    <div class="sql-query">
                        <strong>SQL:</strong>
                        <pre>${sql}</pre>
                    </div>
                    <div class="no-results">
                        <p>❌ Sorgu sonucu bulunamadı</p>
                    </div>
                </div>
            `;
            return;
        }

        const headers = Object.keys(results[0]);
        const tableRows = results.map(row => 
            `<tr>${headers.map(header => `<td>${this.escapeHtml(row[header])}</td>`).join('')}</tr>`
        ).join('');

        this.elements.resultsDiv.innerHTML = `
            <div class="result-section">
                <h3>📊 Sorgu Sonuçları (${results.length} satır)</h3>
                <div class="sql-query">
                    <strong>SQL:</strong>
                    <pre>${sql}</pre>
                </div>
                <div class="table-container">
                    <table class="results-table">
                        <thead>
                            <tr>${headers.map(header => `<th>${this.escapeHtml(header)}</th>`).join('')}</tr>
                        </thead>
                        <tbody>
                            ${tableRows}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    /**
     * Display message result
     */
    displayMessageResult(message, sql) {
        this.elements.resultsDiv.innerHTML = `
            <div class="result-section">
                <h3>✅ Sorgu Tamamlandı</h3>
                <div class="sql-query">
                    <strong>SQL:</strong>
                    <pre>${sql}</pre>
                </div>
                <div class="message-result">
                    <p>${message}</p>
                </div>
            </div>
        `;
    }

    /**
     * Display error result
     */
    displayErrorResult(error, sql) {
        this.elements.resultsDiv.innerHTML = `
            <div class="result-section">
                <h3>❌ Sorgu Hatası</h3>
                <div class="sql-query">
                    <strong>SQL:</strong>
                    <pre>${sql || 'SQL oluşturulamadı'}</pre>
                </div>
                <div class="error-result">
                    <p><strong>Hata:</strong> ${this.escapeHtml(error)}</p>
                </div>
            </div>
        `;
    }

    /**
     * Clear results and form
     */
    clearResults() {
        this.elements.resultsDiv.innerHTML = '<p class="placeholder">Sorgu sonuçları burada görünecek</p>';
        this.elements.questionTextarea.value = '';
        this.showStatus('Sonuçlar temizlendi', 'info');
    }

    /**
     * Update query button state based on form validity
     */
    updateQueryButtonState() {
        const hasQuestion = this.elements.questionTextarea.value.trim().length > 0;
        const hasTables = this.state.selectedTables.length > 0;
        const isConnected = this.state.isConnected;
        
        this.elements.sendQueryBtn.disabled = !(hasQuestion && hasTables && isConnected);
    }

    /**
     * Set loading state
     */
    setLoading(isLoading) {
        this.state.isLoading = isLoading;
        this.elements.setDbBtn.disabled = isLoading;
        this.elements.sendQueryBtn.disabled = isLoading || !this.canSendQuery();
    }

    /**
     * Check if query can be sent
     */
    canSendQuery() {
        const hasQuestion = this.elements.questionTextarea.value.trim().length > 0;
        const hasTables = this.state.selectedTables.length > 0;
        const isConnected = this.state.isConnected;
        
        return hasQuestion && hasTables && isConnected;
    }

    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        this.elements.dbStatus.textContent = message;
        this.elements.dbStatus.className = `status-message status-${type}`;
        
        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => {
                this.elements.dbStatus.textContent = '';
                this.elements.dbStatus.className = 'status-message';
            }, 3000);
        }
    }

    /**
     * Make API call
     */
    async apiCall(endpoint, method = 'GET', data = null) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API call failed');
        }

        return result;
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Format SQL query for better readability
     */
    formatSQL(sql) {
        if (!sql) return '';
        
        // Basic SQL formatting
        return sql
            .replace(/\bSELECT\b/gi, '\nSELECT')
            .replace(/\bFROM\b/gi, '\nFROM')
            .replace(/\bWHERE\b/gi, '\nWHERE')
            .replace(/\bJOIN\b/gi, '\nJOIN')
            .replace(/\bLEFT JOIN\b/gi, '\nLEFT JOIN')
            .replace(/\bRIGHT JOIN\b/gi, '\nRIGHT JOIN')
            .replace(/\bINNER JOIN\b/gi, '\nINNER JOIN')
            .replace(/\bGROUP BY\b/gi, '\nGROUP BY')
            .replace(/\bORDER BY\b/gi, '\nORDER BY')
            .replace(/\bHAVING\b/gi, '\nHAVING')
            .replace(/\bUNION\b/gi, '\nUNION')
            .replace(/\bINSERT INTO\b/gi, '\nINSERT INTO')
            .replace(/\bUPDATE\b/gi, '\nUPDATE')
            .replace(/\bDELETE FROM\b/gi, '\nDELETE FROM')
            .trim();
    }

    /**
     * Re-run a saved query
     */
    async reRunQuery(queryId) {
        try {
            const response = await this.apiCall(`/queries/${queryId}`, 'GET');
            
            if (response.success) {
                const query = response.data;
                
                // Switch to query page
                this.switchPage('query-page');
                
                // Fill the form with the saved query data
                this.elements.questionTextarea.value = query.question;
                
                // Select the tables that were used
                if (this.elements.tableSelect && query.tables_used) {
                    Array.from(this.elements.tableSelect.options).forEach(option => {
                        option.selected = query.tables_used.includes(option.value);
                    });
                    
                    // Trigger change event to load columns
                    this.elements.tableSelect.dispatchEvent(new Event('change'));
                }
                
                this.showStatus('Sorgu bilgileri forma yüklendi. Göndermek için "Sorguyu Gönder" butonuna tıklayın.', 'info');
            } else {
                this.showStatus(`Sorgu alınırken hata: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Sorgu alınırken hata: ${error.message}`, 'error');
        }
    }

    /**
     * Switch between pages
     */
    switchPage(pageName) {
        // Update navigation buttons
        this.elements.navBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.page === pageName);
        });

        // Update page content
        this.elements.pageContents.forEach(content => {
            content.classList.toggle('active', content.id === pageName);
        });

        // Load saved queries when switching to history page
        if (pageName === 'history-page' && this.state.isConnected && this.elements.savedQueriesList) {
            this.loadSavedQueries();
        }
        
        // Load dashboard data when switching to dashboard page
        if (pageName === 'dashboard-page' && this.state.isConnected) {
            this.loadDashboard();
        }
        
        // Load scheduled queries when switching to scheduled page
        if (pageName === 'scheduled-page') {
            console.log('Switching to scheduled page, isConnected:', this.state.isConnected);
            if (this.state.isConnected) {
                console.log('Loading scheduled tables and queries...');
                this.populateScheduledTables();
                this.loadScheduledQueries();
            } else {
                console.warn('Not connected - cannot load scheduled data');
            }
        }
    }

    /**
     * Load saved queries from the database
     */
    async loadSavedQueries() {
        if (!this.elements.savedQueriesList) {
            console.warn('savedQueriesList element not found - Saved queries tab may not be available');
            return;
        }

        if (!this.state.isConnected) {
            this.elements.savedQueriesList.innerHTML = `
                <div class="no-saved-queries">
                    <div class="no-saved-queries-icon">🔌</div>
                    <p>Önce veritabanı bağlantısını kurun</p>
                </div>
            `;
            return;
        }

        try {
            this.elements.savedQueriesList.innerHTML = '<p class="placeholder">Kayıtlı sorgular yükleniyor...</p>';
            
            const response = await this.apiCall('/queries', 'GET');
            
            if (response.success) {
                this.displaySavedQueries(response.data);
            } else {
                this.elements.savedQueriesList.innerHTML = `
                    <div class="no-saved-queries">
                        <div class="no-saved-queries-icon">❌</div>
                        <p>Sorgular yüklenirken hata oluştu: ${response.error}</p>
                    </div>
                `;
            }
        } catch (error) {
            this.elements.savedQueriesList.innerHTML = `
                <div class="no-saved-queries">
                    <div class="no-saved-queries-icon">❌</div>
                    <p>Sorgular yüklenirken hata oluştu: ${error.message}</p>
                </div>
            `;
        }
    }

    /**
     * Display saved queries
     */
    displaySavedQueries(queries) {
        if (!this.elements.savedQueriesList) {
            console.warn('savedQueriesList element not found - Saved queries tab may not be available');
            return;
        }

        if (queries.length === 0) {
            this.elements.savedQueriesList.innerHTML = `
                <div class="no-saved-queries">
                    <div class="no-saved-queries-icon">📝</div>
                    <p>Henüz kayıtlı sorgu bulunmuyor</p>
                    <p>İlk sorgunuzu oluşturun ve otomatik olarak kaydedilecek</p>
                </div>
            `;
            return;
        }

        const queriesHtml = queries.map(query => this.createSavedQueryHTML(query)).join('');
        this.elements.savedQueriesList.innerHTML = queriesHtml;
    }

    /**
     * Create HTML for a saved query
     */
    createSavedQueryHTML(query) {
        const createdDate = new Date(query.created_at).toLocaleString('tr-TR');
        const statusClass = query.is_successful ? 'success' : 'error';
        const statusText = query.is_successful ? '✅ Başarılı' : '❌ Hatalı';
        
        const tablesHtml = query.tables_used.map(table => 
            `<span class="saved-query-table-tag">${this.escapeHtml(table)}</span>`
        ).join('');

        // Format the SQL query for better readability
        const formattedSql = this.formatSQL(query.sql_query);

        // Generate results HTML
        let resultsHtml = '';
        if (query.is_successful && query.query_results && query.query_results.length > 0) {
            // SELECT query with results
            const headers = Object.keys(query.query_results[0]);
            const tableRows = query.query_results.slice(0, 10).map(row => 
                `<tr>${headers.map(header => `<td>${this.escapeHtml(String(row[header] || ''))}</td>`).join('')}</tr>`
            ).join('');
            
            const moreRowsText = query.query_results.length > 10 
                ? `<p class="more-results-info">... ve ${query.query_results.length - 10} satır daha (Toplam: ${query.query_results.length} satır)</p>` 
                : '';

            resultsHtml = `
                <div class="saved-query-results">
                    <h4>📊 Sorgu Sonuçları (${query.query_results.length} satır):</h4>
                    <div class="table-container">
                        <table class="results-table">
                            <thead>
                                <tr>${headers.map(header => `<th>${this.escapeHtml(header)}</th>`).join('')}</tr>
                            </thead>
                            <tbody>
                                ${tableRows}
                            </tbody>
                        </table>
                    </div>
                    ${moreRowsText}
                </div>
            `;
        } else if (query.is_successful && query.result_message) {
            // Non-SELECT query with message
            resultsHtml = `
                <div class="saved-query-success">
                    <h4>✅ Sorgu Başarıyla Çalıştırıldı</h4>
                    <p>${this.escapeHtml(query.result_message)}</p>
                </div>
            `;
        } else if (query.is_successful && query.query_results && query.query_results.length === 0) {
            // SELECT query with no results
            resultsHtml = `
                <div class="saved-query-no-results">
                    <h4>📊 Sorgu Sonuçları:</h4>
                    <p>Sorgu başarılı ancak sonuç bulunamadı.</p>
                </div>
            `;
        } else if (!query.is_successful && query.error_message) {
            // Error
            resultsHtml = `
                <div class="saved-query-error">
                    <h4>❌ Hata Mesajı:</h4>
                    <p>${this.escapeHtml(query.error_message)}</p>
                </div>
            `;
        }

        return `
            <div class="saved-query-item">
                <div class="saved-query-header">
                    <div class="saved-query-info">
                        <div class="saved-query-id">Sorgu #${query.id}</div>
                        <div class="saved-query-question">
                            <strong>💬 Soru:</strong> ${this.escapeHtml(query.question)}
                        </div>
                        <div class="saved-query-meta">
                            <span>📅 ${createdDate}</span>
                            <span class="saved-query-status ${statusClass}">${statusText}</span>
                        </div>
                        <div class="saved-query-tables">
                            <strong>📋 Kullanılan Tablolar:</strong> ${tablesHtml}
                        </div>
                    </div>
                </div>
                
                <div class="saved-query-sql-section">
                    <h4>🔍 SQL Sorgusu:</h4>
                    <div class="sql-code-block">
                        <pre><code>${formattedSql}</code></pre>
                    </div>
                </div>
                
                ${resultsHtml}
                
                <div class="saved-query-actions">
                    <button class="btn btn-sm btn-secondary" onclick="app.copyQuery(${query.id})">
                        📋 SQL'i Kopyala
                    </button>
                    <button class="btn btn-sm btn-primary" onclick="app.reRunQuery(${query.id})">
                        🔄 Tekrar Çalıştır
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="app.deleteQuery(${query.id})">
                        🗑️ Sil
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Delete a saved query
     */
    async deleteQuery(queryId) {
        if (!confirm('Bu sorguyu silmek istediğinizden emin misiniz?')) {
            return;
        }

        try {
            const response = await this.apiCall(`/queries/${queryId}`, 'DELETE');
            
            if (response.success) {
                this.showStatus('Sorgu başarıyla silindi', 'success');
                await this.loadSavedQueries(); // Refresh the list
            } else {
                this.showStatus(`Sorgu silinirken hata: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Sorgu silinirken hata: ${error.message}`, 'error');
        }
    }

    /**
     * Copy query to clipboard
     */
    async copyQuery(queryId) {
        try {
            const response = await this.apiCall(`/queries/${queryId}`, 'GET');
            
            if (response.success) {
                await navigator.clipboard.writeText(response.data.sql_query);
                this.showStatus('SQL sorgusu panoya kopyalandı', 'success');
            } else {
                this.showStatus(`Sorgu alınırken hata: ${response.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Kopyalama hatası: ${error.message}`, 'error');
        }
    }

    /**
     * Export queries to file
     */
    async exportQueriesToFile() {
        if (!this.state.isConnected) {
            this.showStatus('Önce veritabanı bağlantısını kurun', 'error');
            return;
        }

        try {
            const response = await this.apiCall('/queries', 'GET');
            
            if (response.success && response.data.length > 0) {
                // Create file content
                let fileContent = `# SQL Agent - Kayıtlı Sorgular\n`;
                fileContent += `# Oluşturulma Tarihi: ${new Date().toLocaleString('tr-TR')}\n`;
                fileContent += `# Toplam Sorgu Sayısı: ${response.data.length}\n\n`;
                
                response.data.forEach((query, index) => {
                    const createdDate = new Date(query.created_at).toLocaleString('tr-TR');
                    const status = query.is_successful ? 'BAŞARILI' : 'HATALI';
                    
                    fileContent += `## Sorgu #${query.id} - ${status}\n`;
                    fileContent += `**Tarih:** ${createdDate}\n`;
                    fileContent += `**Soru:** ${query.question}\n`;
                    fileContent += `**Tablolar:** ${query.tables_used.join(', ')}\n`;
                    
                    if (query.error_message) {
                        fileContent += `**Hata:** ${query.error_message}\n`;
                    }
                    
                    fileContent += `\n**SQL Sorgusu:**\n\`\`\`sql\n${query.sql_query}\n\`\`\`\n\n`;
                    fileContent += `---\n\n`;
                });
                
                // Create and download file
                const blob = new Blob([fileContent], { type: 'text/markdown' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `sorgular_${new Date().toISOString().split('T')[0]}.md`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showStatus('Sorgular başarıyla dosyaya kaydedildi', 'success');
            } else {
                this.showStatus('Kaydedilecek sorgu bulunamadı', 'info');
            }
        } catch (error) {
            this.showStatus(`Dosya kaydetme hatası: ${error.message}`, 'error');
        }
    }

    /**
     * Clear all saved queries
     */
    async clearAllQueries() {
        if (!confirm('Tüm kayıtlı sorguları silmek istediğinizden emin misiniz? Bu işlem geri alınamaz!')) {
            return;
        }

        try {
            // Get all queries first
            const response = await this.apiCall('/queries', 'GET');
            
            if (response.success && response.data.length > 0) {
                // Delete each query
                for (const query of response.data) {
                    await this.apiCall(`/queries/${query.id}`, 'DELETE');
                }
                
                this.showStatus('Tüm sorgular başarıyla silindi', 'success');
                await this.loadSavedQueries(); // Refresh the list
            } else {
                this.showStatus('Silinecek sorgu bulunamadı', 'info');
            }
        } catch (error) {
            this.showStatus(`Sorgular silinirken hata: ${error.message}`, 'error');
        }
    }

    /* ==========================================================================
       DASHBOARD METHODS
       ========================================================================== */

    /**
     * Load dashboard data
     */
    async loadDashboard() {
        if (!this.state.isConnected) {
            return;
        }

        try {
            const response = await this.apiCall('/queries', 'GET');
            
            if (response.success) {
                this.populateQuerySelector(response.data);
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    /**
     * Populate query selector dropdown
     */
    populateQuerySelector(queries) {
        if (!this.elements.querySelector) return;
        
        this.elements.querySelector.innerHTML = '<option value="">Sorgu seçin...</option>';
        
        // Only show queries with results
        const queriesWithResults = queries.filter(q => q.query_results && q.query_results.length > 0);
        
        if (queriesWithResults.length === 0) {
            this.elements.querySelector.innerHTML = '<option value="">Grafik oluşturulabilecek sorgu yok</option>';
            return;
        }
        
        queriesWithResults.forEach(query => {
            const option = document.createElement('option');
            option.value = query.id;
            option.textContent = `#${query.id} - ${query.question.substring(0, 60)}${query.question.length > 60 ? '...' : ''}`;
            this.elements.querySelector.appendChild(option);
        });
    }

    /**
     * Select chart type
     */
    selectChartType(chartType) {
        this.state.selectedChartType = chartType;
        
        // Update button states
        this.elements.chartTypeBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.chartType === chartType);
        });
        this.updateCreateChartButtonState();
    }

    /**
     * Update create chart button state
     */
    updateCreateChartButtonState() {
        if (this.elements.createChartBtn) {
            const enabled = !!(this.state.selectedQueryId && this.state.selectedChartType);
            this.elements.createChartBtn.disabled = !enabled;
        }
    }

    /**
     * Create chart from selected query
     */
    async createChart() {
        if (!this.state.selectedQueryId) return;
        if (!this.state.selectedChartType) {
            this.showStatus('Önce bir grafik tipi seçin', 'error');
            return;
        }

        try {
            const response = await this.apiCall(`/queries/${this.state.selectedQueryId}`, 'GET');
            
            if (response.success && response.data.query_results) {
                const query = response.data;
                this.renderChart(query);
            } else {
                this.showStatus('Sorgu verileri alınamadı', 'error');
            }
        } catch (error) {
            this.showStatus(`Grafik oluşturma hatası: ${error.message}`, 'error');
        }
    }

    /**
     * Render chart with query data
     */
    renderChart(query) {
        const results = query.query_results;
        
        if (!results || results.length === 0) {
            this.showStatus('Sorgu sonucu boş', 'error');
            return;
        }

        // Analyze data
        const chartData = this.analyzeDataForChart(results);
        
        if (!chartData) {
            this.showStatus('Bu sorgu verisi grafik oluşturmak için uygun değil', 'error');
            return;
        }

        // Hide placeholder, show canvas
        const placeholder = this.elements.chartContainer.querySelector('.no-chart-placeholder');
        if (placeholder) placeholder.style.display = 'none';
        this.elements.dashboardChart.style.display = 'block';

        // Destroy existing chart
        if (this.state.currentChart) {
            this.state.currentChart.destroy();
        }

        // Create new chart
        const ctx = this.elements.dashboardChart.getContext('2d');
        // Fix hover-induced layout shifts by enforcing height and disabling aspect ratio
        this.elements.dashboardChart.height = 420;

        // Use user-selected type only
        const typeToUse = this.state.selectedChartType;
        const chartConfig = this.getChartConfig(chartData, typeToUse);
        
        this.state.currentChart = new Chart(ctx, chartConfig);

        // Show chart info
        this.displayChartInfo(query, chartData);
        this.highlightRecommendedChart(chartData.recommendedChart);
        
        this.showStatus('Grafik başarıyla oluşturuldu!', 'success');
    }

    highlightRecommendedChart(recommended) {
        if (!this.elements.chartTypeBtns) return;
        this.elements.chartTypeBtns.forEach(btn => {
            const type = btn.dataset.chartType;
            // Add star to the recommended button label and a badge
            if (recommended && type === recommended) {
                btn.classList.add('recommended');
                if (!btn.dataset.originalText) btn.dataset.originalText = btn.textContent;
                btn.textContent = `🏅 ${btn.dataset.originalText} · Önerilen`;
                btn.style.backgroundColor = '#fde7c6'; // light orange background
                btn.style.borderColor = '#f59e0b';
            } else {
                btn.classList.remove('recommended');
                if (btn.dataset.originalText) btn.textContent = btn.dataset.originalText;
                btn.style.backgroundColor = '';
                btn.style.borderColor = '';
            }
        });
    }

    async showRecommendedChartForSelectedQuery() {
        try {
            const response = await this.apiCall(`/queries/${this.state.selectedQueryId}`, 'GET');
            if (!response.success || !response.data || !response.data.query_results) {
                this.highlightRecommendedChart(null);
                return;
            }
            const results = response.data.query_results;
            const chartData = this.analyzeDataForChart(results);
            if (!chartData) {
                this.highlightRecommendedChart(null);
                return;
            }
            // Mark recommended in UI but DO NOT set selected type
            this.highlightRecommendedChart(chartData.recommendedChart);
        } catch (e) {
            this.highlightRecommendedChart(null);
        }
    }

    /**
     * Analyze data to determine best chart representation
     */
    analyzeDataForChart(results) {
        if (results.length === 0) return null;

        const keys = Object.keys(results[0]);
        
        if (keys.length < 2) return null;

        // Try to find label and value columns
        let labelKey = null;
        let valueKey = null;

        // Look for numeric columns
        const numericKeys = keys.filter(key => {
            const value = results[0][key];
            return typeof value === 'number' || !isNaN(parseFloat(value));
        });

        // Look for string/text columns for labels
        const textKeys = keys.filter(key => !numericKeys.includes(key));

        if (numericKeys.length === 0) {
            // No numeric data, try to count occurrences
            labelKey = keys[0];
            const counts = {};
            results.forEach(row => {
                const label = String(row[labelKey]);
                counts[label] = (counts[label] || 0) + 1;
            });
            
            return {
                labels: Object.keys(counts),
                datasets: [{
                    label: 'Count',
                    data: Object.values(counts)
                }]
            };
        }

        // Use first text column as label, first numeric as value
        labelKey = textKeys.length > 0 ? textKeys[0] : keys[0];
        valueKey = numericKeys[0];

        const labels = results.map(row => String(row[labelKey]));
        const data = results.map(row => parseFloat(row[valueKey]) || 0);

        // Heuristic recommendation
        const distinctLabelCount = new Set(labels).size;
        let recommended = 'bar';
        if (distinctLabelCount <= 5 && distinctLabelCount > 0) {
            recommended = 'pie';
        } else if (distinctLabelCount > 15) {
            recommended = 'line';
        }

        return {
            labels: labels,
            datasets: [{
                label: valueKey,
                data: data
            }],
            originalKeys: { labelKey, valueKey },
            recommendedChart: recommended
        };
    }

    /**
     * Get chart configuration
     */
    getChartConfig(chartData, chartType) {
        const colors = [
            'rgba(37, 99, 235, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(236, 72, 153, 0.8)',
            'rgba(14, 165, 233, 0.8)',
        ];

        const backgroundColors = chartType === 'pie' || chartType === 'doughnut' 
            ? colors 
            : colors[0];

        const config = {
            type: chartType === 'area' ? 'line' : chartType,
            data: {
                labels: chartData.labels,
                datasets: chartData.datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    backgroundColor: Array.isArray(backgroundColors) ? backgroundColors : backgroundColors,
                    borderColor: Array.isArray(backgroundColors) ? backgroundColors.map(c => c.replace('0.8', '1')) : backgroundColors.replace('0.8', '1'),
                    borderWidth: 2,
                    fill: chartType === 'area'
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 400 },
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: chartType !== 'pie' && chartType !== 'doughnut' ? {
                    y: {
                        beginAtZero: true
                    }
                } : {}
            }
        };

        return config;
    }

    /**
     * Update schedule input visibility based on schedule type
     */
    updateScheduleInputs() {
        const scheduleType = this.elements.scheduleType.value;
        
        // Hide all optional inputs first
        this.elements.timeInputGroup.style.display = 'none';
        this.elements.dayInputGroup.style.display = 'none';
        this.elements.monthDayInputGroup.style.display = 'none';
        
        // Show relevant inputs based on schedule type
        switch(scheduleType) {
            case 'hourly':
                // No additional inputs needed
                break;
            case 'daily':
                this.elements.timeInputGroup.style.display = 'block';
                break;
            case 'weekly':
                this.elements.timeInputGroup.style.display = 'block';
                this.elements.dayInputGroup.style.display = 'block';
                break;
            case 'monthly':
                this.elements.timeInputGroup.style.display = 'block';
                this.elements.monthDayInputGroup.style.display = 'block';
                break;
        }
        
        this.updateCreateScheduledButtonState();
    }
    
    /**
     * Update create scheduled query button state
     */
    updateCreateScheduledButtonState() {
        if (!this.elements.createScheduledBtn) return;
        
        const hasQuestion = this.elements.scheduledQuestion.value.trim().length > 0;
        const hasTables = this.elements.scheduledTables.selectedOptions.length > 0;
        const isConnected = this.state.isConnected;
        
        this.elements.createScheduledBtn.disabled = !(hasQuestion && hasTables && isConnected);
    }
    
    /**
     * Populate scheduled tables dropdown
     */
    async populateScheduledTables() {
        if (!this.elements.scheduledTables) {
            console.warn('scheduledTables element not found');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/tables`);
            const data = await response.json();
            
            console.log('Tables response:', data); // Debug log
            
            if (data.success && data.data) {
                this.elements.scheduledTables.innerHTML = '';
                
                // Add a default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Tablo seçin...';
                defaultOption.disabled = true;
                this.elements.scheduledTables.appendChild(defaultOption);
                
                // Add table options
                data.data.forEach(table => {
                    const option = document.createElement('option');
                    option.value = table;
                    option.textContent = table;
                    this.elements.scheduledTables.appendChild(option);
                });
                
                console.log(`Loaded ${data.data.length} tables into scheduled tables dropdown`);
            } else {
                console.warn('No tables data found in response:', data);
            }
        } catch (error) {
            console.error('Error loading tables for scheduled queries:', error);
        }
    }
    
    /**
     * Create new scheduled query
     */
    async createScheduledQuery() {
        const question = this.elements.scheduledQuestion.value.trim();
        const selectedTables = Array.from(this.elements.scheduledTables.selectedOptions).map(opt => opt.value);
        const scheduleType = this.elements.scheduleType.value;
        
        if (!question || selectedTables.length === 0) {
            this.showStatus('Lütfen sorgu ve tablo seçin', 'error');
            return;
        }
        
        // Prepare schedule data based on type
        const scheduleData = {
            question: question,
            tables: selectedTables,
            schedule_type: scheduleType
        };
        
        if (scheduleType === 'daily' || scheduleType === 'weekly' || scheduleType === 'monthly') {
            scheduleData.schedule_time = this.elements.scheduleTime.value;
        }
        
        if (scheduleType === 'weekly') {
            scheduleData.schedule_day = parseInt(this.elements.scheduleDay.value);
        }
        
        if (scheduleType === 'monthly') {
            scheduleData.schedule_day = parseInt(this.elements.scheduleMonthDay.value);
        }
        
        try {
            this.showStatus('Zamanlanmış sorgu oluşturuluyor...', 'info');
            
            const response = await fetch(`${this.apiBaseUrl}/scheduled-queries`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(scheduleData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showStatus('✅ Zamanlanmış sorgu başarıyla oluşturuldu!', 'success');
                
                // Clear form
                this.elements.scheduledQuestion.value = '';
                this.elements.scheduledTables.selectedIndex = -1;
                this.elements.scheduleType.value = 'daily';
                this.elements.scheduleTime.value = '09:00';
                this.updateScheduleInputs();
                
                // Reload scheduled queries list
                await this.loadScheduledQueries();
            } else {
                this.showStatus(`❌ Hata: ${data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error creating scheduled query:', error);
            this.showStatus('❌ Zamanlanmış sorgu oluşturulurken bir hata oluştu', 'error');
        }
    }
    
    /**
     * Load scheduled queries
     */
    async loadScheduledQueries() {
        if (!this.elements.scheduledQueriesList) return;
        
        try {
            this.elements.scheduledQueriesList.innerHTML = '<p class="placeholder">Zamanlanmış sorgular yükleniyor...</p>';
            
            const response = await fetch(`${this.apiBaseUrl}/scheduled-queries`);
            const data = await response.json();
            
            if (data.success && data.data && data.data.length > 0) {
                this.renderScheduledQueries(data.data);
            } else {
                this.elements.scheduledQueriesList.innerHTML = `
                    <div class="no-scheduled-queries">
                        <div class="no-scheduled-queries-icon">⏰</div>
                        <h3>Henüz zamanlanmış sorgu yok</h3>
                        <p>Yukarıdaki formdan yeni bir zamanlanmış sorgu oluşturabilirsiniz</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading scheduled queries:', error);
            this.elements.scheduledQueriesList.innerHTML = '<p class="error">❌ Zamanlanmış sorgular yüklenemedi</p>';
        }
    }
    
    /**
     * Render scheduled queries list
     */
    renderScheduledQueries(queries) {
        this.elements.scheduledQueriesList.innerHTML = queries.map(query => {
            const scheduleText = this.getScheduleText(query);
            const statusBadge = query.is_active 
                ? '<span class="scheduled-query-status-badge active">✅ Aktif</span>'
                : '<span class="scheduled-query-status-badge inactive">⏸️ Pasif</span>';
            
            const lastRunInfo = query.last_run_at 
                ? `
                    <div class="scheduled-query-last-run ${query.last_run_status === 'success' ? 'last-run-success' : 'last-run-error'}">
                        <h5>Son Çalıştırma:</h5>
                        <div class="last-run-info">
                            📅 ${new Date(query.last_run_at).toLocaleString('tr-TR')}
                            <br>
                            ${query.last_run_status === 'success' ? '✅ Başarılı' : '❌ Hata'}
                            <br>
                            🔄 Toplam ${query.run_count} kez çalıştırıldı
                        </div>
                    </div>
                `
                : '<p style="font-size: 0.875rem; color: #6b7280;">Henüz çalıştırılmadı</p>';
            
            // Safely handle tables_used - it might be null, undefined, or an array
            const tablesUsed = Array.isArray(query.tables_used) ? query.tables_used : 
                               (query.tables_used ? [query.tables_used] : []);
            
            return `
                <div class="scheduled-query-card ${query.is_active ? '' : 'inactive'}">
                    <div class="scheduled-query-header">
                        <div class="scheduled-query-info">
                            <h4 class="scheduled-query-question">${this.escapeHtml(query.question)}</h4>
                            <div class="scheduled-query-schedule">
                                <span class="schedule-badge">${scheduleText}</span>
                            </div>
                            <div class="scheduled-query-meta">
                                <span>📅 ${new Date(query.created_at).toLocaleDateString('tr-TR')}</span>
                            </div>
                        </div>
                        ${statusBadge}
                    </div>
                    
                    ${tablesUsed.length > 0 ? `
                        <div class="scheduled-query-tables">
                            <h5>Kullanılan Tablolar:</h5>
                            <div class="table-tags">
                                ${tablesUsed.map(table => `<span class="table-tag">${this.escapeHtml(table)}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${lastRunInfo}
                    
                    <div class="scheduled-query-actions">
                        <button class="btn btn-primary" onclick="app.runScheduledQueryNow(${query.id})">
                            ▶️ Şimdi Çalıştır
                        </button>
                        <button class="btn btn-${query.is_active ? 'warning' : 'success'}" onclick="app.toggleScheduledQuery(${query.id}, ${!query.is_active})">
                            ${query.is_active ? '⏸️ Durdur' : '▶️ Başlat'}
                        </button>
                        <button class="btn" onclick="app.editScheduledQuery(${query.id})">
                            ✏️ Düzenle
                        </button>
                        <button class="btn btn-danger" onclick="app.deleteScheduledQuery(${query.id})">
                            🗑️ Sil
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    /**
     * Edit a scheduled query's schedule params
     */
    async editScheduledQuery(queryId) {
        try {
            // Load existing
            const res = await fetch(`${this.apiBaseUrl}/scheduled-queries/${queryId}`);
            const data = await res.json();
            if (!data.success || !data.data) {
                this.showStatus('Sorgu detayları alınamadı', 'error');
                return;
            }
            const q = data.data;

            // Ask for new values (simple prompt flow)
            const scheduleType = prompt('Zamanlama tipi (hourly/daily/weekly/monthly/custom):', q.schedule_type || 'daily');
            if (!scheduleType) return;

            let scheduleTime = q.schedule_time || '09:00';
            let scheduleDay = q.schedule_day;
            let cronExpression = q.cron_expression || '';

            if (scheduleType === 'daily' || scheduleType === 'weekly' || scheduleType === 'monthly') {
                const t = prompt('Saat (HH:MM):', scheduleTime);
                if (!t) return; 
                if (!/^\d{2}:\d{2}$/.test(t)) {
                    this.showStatus('Geçersiz saat formatı. Örn: 09:30', 'error');
                    return;
                }
                scheduleTime = t;
            }

            if (scheduleType === 'weekly') {
                const d = prompt('Gün (0=Pzt ... 6=Paz):', (scheduleDay ?? 0));
                if (d === null) return;
                const di = parseInt(d, 10);
                if (isNaN(di) || di < 0 || di > 6) {
                    this.showStatus('Geçersiz gün değeri (0-6)', 'error');
                    return;
                }
                scheduleDay = di;
            }

            if (scheduleType === 'monthly') {
                const md = prompt('Ayın günü (1-31):', (scheduleDay ?? 1));
                if (md === null) return;
                const mdi = parseInt(md, 10);
                if (isNaN(mdi) || mdi < 1 || mdi > 31) {
                    this.showStatus('Geçersiz ayın günü (1-31)', 'error');
                    return;
                }
                scheduleDay = mdi;
            }

            if (scheduleType === 'custom') {
                const ce = prompt('Cron ifadesi (min saat gün ay hafta):', cronExpression || '');
                if (ce === null || !ce.trim()) {
                    this.showStatus('Geçersiz cron ifadesi', 'error');
                    return;
                }
                cronExpression = ce.trim();
                scheduleTime = null; // not used
                scheduleDay = null;  // not used
            }

            // Build payload
            const payload = {
                question: q.question,
                tables: q.tables_used || [],
                schedule_type: scheduleType,
                schedule_time: scheduleType === 'custom' ? null : scheduleTime,
                schedule_day: scheduleType === 'weekly' || scheduleType === 'monthly' ? scheduleDay : null,
                cron_expression: scheduleType === 'custom' ? cronExpression : null,
                is_active: q.is_active
            };

            this.showStatus('Zamanlanmış sorgu güncelleniyor...', 'info');
            const putRes = await fetch(`${this.apiBaseUrl}/scheduled-queries/${queryId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const putData = await putRes.json();
            if (putData.success) {
                this.showStatus('✅ Zamanlanmış sorgu güncellendi', 'success');
                await this.loadScheduledQueries();
            } else {
                this.showStatus(`❌ Hata: ${putData.error || putData.message}`, 'error');
            }
        } catch (e) {
            console.error(e);
            this.showStatus('❌ Güncelleme sırasında bir hata oluştu', 'error');
        }
    }
    
    /**
     * Get human-readable schedule text
     */
    getScheduleText(query) {
        switch(query.schedule_type) {
            case 'hourly':
                return '🕐 Her saat başı';
            case 'daily':
                return `📅 Her gün ${query.schedule_time}`;
            case 'weekly':
                const days = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];
                return `📆 Her ${days[query.schedule_day]} ${query.schedule_time}`;
            case 'monthly':
                return `🗓️ Her ayın ${query.schedule_day}. günü ${query.schedule_time}`;
            default:
                return query.schedule_type;
        }
    }
    
    /**
     * Toggle scheduled query active status
     */
    async toggleScheduledQuery(queryId, isActive) {
        try {
            this.showStatus(`Zamanlanmış sorgu ${isActive ? 'başlatılıyor' : 'durduruluyor'}...`, 'info');
            
            const response = await fetch(`${this.apiBaseUrl}/scheduled-queries/${queryId}/toggle`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ is_active: isActive })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showStatus(`✅ Zamanlanmış sorgu ${isActive ? 'başlatıldı' : 'durduruldu'}`, 'success');
                await this.loadScheduledQueries();
            } else {
                this.showStatus(`❌ Hata: ${data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error toggling scheduled query:', error);
            this.showStatus('❌ İşlem sırasında bir hata oluştu', 'error');
        }
    }
    
    /**
     * Delete scheduled query
     */
    async deleteScheduledQuery(queryId) {
        if (!confirm('Bu zamanlanmış sorguyu silmek istediğinizden emin misiniz?')) {
            return;
        }
        
        try {
            this.showStatus('Zamanlanmış sorgu siliniyor...', 'info');
            
            const response = await fetch(`${this.apiBaseUrl}/scheduled-queries/${queryId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showStatus('✅ Zamanlanmış sorgu silindi', 'success');
                await this.loadScheduledQueries();
            } else {
                this.showStatus(`❌ Hata: ${data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error deleting scheduled query:', error);
            this.showStatus('❌ Silme işlemi sırasında bir hata oluştu', 'error');
        }
    }
    
    /**
     * Run scheduled query immediately (for testing)
     */
    async runScheduledQueryNow(queryId) {
        try {
            this.showStatus('⏳ Sorgu çalıştırılıyor...', 'info');
            
            const response = await fetch(`${this.apiBaseUrl}/scheduled-queries/${queryId}/run-now`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showStatus('✅ Sorgu başarıyla çalıştırıldı! Geçmiş sekmesinden sonuçları görebilirsiniz.', 'success');
                // Refresh the list to show updated last_run info
                await this.loadScheduledQueries();
            } else {
                this.showStatus(`❌ Hata: ${data.error || data.message}`, 'error');
            }
        } catch (error) {
            console.error('Error running scheduled query:', error);
            this.showStatus('❌ Sorgu çalıştırılırken bir hata oluştu', 'error');
        }
    }

    /**
     * Display chart information
     */
    displayChartInfo(query, chartData) {
        if (!this.elements.chartInfo || !this.elements.chartDetails) return;

        const totalDataPoints = chartData.labels.length;
        const dataset = chartData.datasets[0];
        const total = dataset.data.reduce((a, b) => a + b, 0);
        const average = (total / dataset.data.length).toFixed(2);
        const max = Math.max(...dataset.data);
        const min = Math.min(...dataset.data);

        this.elements.chartDetails.innerHTML = `
            <div class="chart-stat">
                <div class="chart-stat-label">📊 Veri Sayısı</div>
                <div class="chart-stat-value">${totalDataPoints}</div>
            </div>
            <div class="chart-stat">
                <div class="chart-stat-label">📈 Toplam</div>
                <div class="chart-stat-value">${total.toFixed(2)}</div>
            </div>
            <div class="chart-stat">
                <div class="chart-stat-label">📊 Ortalama</div>
                <div class="chart-stat-value">${average}</div>
            </div>
            <div class="chart-stat">
                <div class="chart-stat-label">⬆️ Maksimum</div>
                <div class="chart-stat-value">${max}</div>
            </div>
            <div class="chart-stat">
                <div class="chart-stat-label">⬇️ Minimum</div>
                <div class="chart-stat-value">${min}</div>
            </div>
        `;

        this.elements.chartInfo.style.display = 'block';
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // DOM tamamen yüklendikten sonra uygulamayı başlat
    setTimeout(() => {
        window.app = new SQLAgentApp();
    }, 100); // 100ms gecikme ile DOM elementlerinin hazır olduğundan emin ol
});
