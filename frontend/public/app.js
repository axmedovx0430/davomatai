// Telegram Mini App Logic (Vanilla JS)

// Configuration
const CONFIG = {
    API_BASE_URL: '/api', // Relative path to use Next.js proxy
    DEFAULT_USER: {
        id: 999,
        first_name: 'Guest User',
        username: 'guest'
    }
};

// Logger
const Logger = {
    log: (msg, data) => console.log(`[App] ${msg}`, data || ''),
    error: (msg, err) => console.error(`[App Error] ${msg}`, err || '')
};

// Telegram Environment Detection
const TelegramEnv = {
    isTelegram: () => !!window.Telegram?.WebApp,
    init: () => {
        if (TelegramEnv.isTelegram()) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
            Logger.log('Telegram WebApp initialized');
            return true;
        }
        Logger.log('Not running in Telegram');
        return false;
    },
    getUser: () => {
        if (TelegramEnv.isTelegram() && window.Telegram.WebApp.initDataUnsafe?.user) {
            return window.Telegram.WebApp.initDataUnsafe.user;
        }
        return CONFIG.DEFAULT_USER;
    }
};

// Safe Fetch Wrapper
const SafeFetch = async (endpoint, options = {}) => {
    try {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        Logger.log(`Fetching: ${url}`);

        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        Logger.error('Fetch failed', error);
        throw error;
    }
};

// UI Rendering
const UI = {
    renderUser: (user) => {
        const container = document.getElementById('user-info');
        if (container) {
            container.innerHTML = `
                <div class="user-card">
                    <h3>👋 Hello, ${user.first_name}</h3>
                    <p>ID: ${user.id}</p>
                    <p>Username: @${user.username || 'N/A'}</p>
                </div>
            `;
        }
    },
    renderStats: (stats) => {
        const container = document.getElementById('stats-content');
        if (container && stats) {
            container.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${stats.present_days || 0}</div>
                        <div class="stat-label">Present</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.late_days || 0}</div>
                        <div class="stat-label">Late</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.absent_days || 0}</div>
                        <div class="stat-label">Absent</div>
                    </div>
                </div>
            `;
        }
    },
    renderHistory: (records) => {
        const container = document.getElementById('history-content');
        if (container && records) {
            if (records.length === 0) {
                container.innerHTML = '<p class="no-data">No attendance records found.</p>';
                return;
            }

            const html = records.map(r => {
                const date = new Date(r.timestamp).toLocaleDateString();
                const time = new Date(r.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                const statusClass = r.status.toLowerCase();
                return `
                    <div class="history-item">
                        <div class="history-date">
                            <div>${date}</div>
                            <div class="history-time">${time}</div>
                        </div>
                        <div class="history-status status-${statusClass}">
                            ${r.status}
                        </div>
                    </div>
                `;
            }).join('');

            container.innerHTML = `<div class="history-list">${html}</div>`;
        }
    },
    renderError: (msg) => {
        const container = document.getElementById('app-content');
        if (container) {
            container.innerHTML = `<div class="error-card">❌ ${msg}</div>`;
        }
    },
    renderLoading: () => {
        const container = document.getElementById('app-content');
        if (container) {
            container.innerHTML = '<div class="loading">Loading data...</div>';
        }
    }
};

// Main Application
const App = {
    init: async () => {
        try {
            TelegramEnv.init();
            const user = TelegramEnv.getUser();
            UI.renderUser(user);
            UI.renderLoading();

            // Fetch Stats
            try {
                const statsData = await SafeFetch(`/attendance/user/${user.id}/stats`);
                if (statsData.success) {
                    UI.renderStats(statsData.stats);
                }
            } catch (e) {
                console.error("Failed to fetch stats", e);
            }

            // Fetch History
            try {
                const historyData = await SafeFetch(`/attendance/user/${user.id}`);
                if (historyData.success) {
                    UI.renderHistory(historyData.attendance);
                }
            } catch (e) {
                console.error("Failed to fetch history", e);
            }

            // Clear loading if it's still there (replaced by stats/history)
            const loading = document.querySelector('.loading');
            if (loading) loading.remove();

        } catch (error) {
            UI.renderError(error.message);
        }
    }
};

// Start App
document.addEventListener('DOMContentLoaded', App.init);
