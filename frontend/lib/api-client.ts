import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor for API key
apiClient.interceptors.request.use((config) => {
    const apiKey = localStorage.getItem('api_key')
    if (apiKey) {
        config.headers['X-API-Key'] = apiKey
    }
    return config
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Redirect to login or show error
            console.error('Unauthorized access')
        }
        return Promise.reject(error)
    }
)

// API functions
export const api = {
    // Users
    getUsers: (params?: any) => apiClient.get('/api/users', { params }),
    getUser: (id: number) => apiClient.get(`/api/users/${id}`),
    getUserByEmployeeId: (employeeId: string) => apiClient.get(`/api/users/employee/${employeeId}`),
    createUser: (data: any) => apiClient.post('/api/users', data),
    updateUser: (id: number, data: any) => apiClient.put(`/api/users/${id}`, data),
    deleteUser: (id: number) => apiClient.delete(`/api/users/${id}`),

    // Faces
    registerFace: (userId: number, file: File) => {
        const formData = new FormData()
        formData.append('file', file)
        return apiClient.post(`/api/face/register?user_id=${userId}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
    },
    getUserFaces: (userId: number) => apiClient.get(`/api/face/user/${userId}`),
    deleteFace: (faceId: number) => apiClient.delete(`/api/face/${faceId}`),

    // Attendance
    getAttendance: (params?: any) => apiClient.get('/api/attendance', { params }),
    getTodayAttendance: () => apiClient.get('/api/attendance/today'),
    getAttendanceStats: () => apiClient.get('/api/attendance/stats'),
    getUserAttendance: (userId: number, params?: any) =>
        apiClient.get(`/api/attendance/user/${userId}`, { params }),
    getUserStats: (userId: number, days: number = 30) =>
        apiClient.get(`/api/attendance/user/${userId}/stats?days=${days}`),

    // Devices
    getDevices: () => apiClient.get('/api/devices'),
    getDevice: (id: number) => apiClient.get(`/api/devices/${id}`),
    createDevice: (data: any) => apiClient.post('/api/devices', data),
    updateDevice: (id: number, data: any) => apiClient.put(`/api/devices/${id}`, data),
    deleteDevice: (id: number) => apiClient.delete(`/api/devices/${id}`),
    regenerateApiKey: (id: number) => apiClient.post(`/api/devices/${id}/regenerate-key`),

    // Time Settings
    getTimeSettings: () => apiClient.get('/api/settings/time'),
    updateTimeSettings: (data: any) => apiClient.post('/api/settings/time', data),
    getTimeSettingsHistory: () => apiClient.get('/api/settings/time/history'),
}

export default apiClient
