module.exports = {
    apps: [{
        name: 'attendance-backend',
        script: 'main.py',
        interpreter: 'python',
        cwd: './backend',
        env: {
            NODE_ENV: 'production'
        },
        error_file: './logs/backend-error.log',
        out_file: './logs/backend-out.log',
        log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
    }]
}
