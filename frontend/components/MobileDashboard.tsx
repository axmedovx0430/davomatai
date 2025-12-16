'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api-client'
import { User, Calendar, Clock, CheckCircle, XCircle, LogOut } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface MobileDashboardProps {
    onSwitchToAdmin: () => void
}

interface UserData {
    id: number
    name: string
    email: string
    role: 'employee' | 'admin'
}

interface AttendanceRecord {
    id: number
    check_in_time: string
    status: 'present' | 'late'
    schedule?: {
        name: string
    }
}

interface MonthlyStats {
    present_count: number
    late_count: number
    absent_count: number
}

export default function MobileDashboard({ onSwitchToAdmin }: MobileDashboardProps) {
    const [employeeId, setEmployeeId] = useState('')
    const [user, setUser] = useState<UserData | null>(null)
    const [todayAttendance, setTodayAttendance] = useState<AttendanceRecord[]>([])
    const [stats, setStats] = useState<MonthlyStats | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const router = useRouter()

    useEffect(() => {
        const storedEmployeeId = localStorage.getItem('employeeId')
        if (storedEmployeeId) {
            setEmployeeId(storedEmployeeId)
            fetchDashboardData(storedEmployeeId)
        } else {
            router.push('/login')
        }
    }, [router])

    const fetchDashboardData = async (id: string) => {
        setLoading(true)
        setError(null)
        try {
            const userRes = await api.getUserByEmployeeId(id)
            const userData = userRes.data.user
            setUser(userData)

            const [attendanceRes, statsRes] = await Promise.all([
                api.getUserAttendance(userData.id, { date: new Date().toISOString().split('T')[0] }),
                api.getUserStats(userData.id)
            ])

            setTodayAttendance(attendanceRes.data.attendance)
            setStats(statsRes.data)
        } catch (err) {
            console.error('Failed to fetch dashboard data:', err)
            setError('Maʼlumotlarni yuklashda xatolik yuz berdi.')
            // If user data fails, redirect to login
            // router.push('/login') // Don't redirect immediately to avoid loops if API is down
        } finally {
            setLoading(false)
        }
    }

    const handleLogout = () => {
        localStorage.removeItem('employeeId')
        router.push('/login')
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
                <p className="mt-4 text-gray-600">Yuklanmoqda...</p>
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
                <XCircle className="text-red-500" size={48} />
                <p className="mt-4 text-red-600">{error}</p>
                <button
                    onClick={() => router.push('/login')}
                    className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition-colors"
                >
                    Qayta urinish
                </button>
            </div>
        )
    }

    if (!user) {
        return null // Should ideally not happen if error handling and redirect work
    }

    return (
        <div className="min-h-screen bg-gray-50 p-4">
            <div className="max-w-md mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                        <User className="text-gray-700" size={24} />
                        <div>
                            <p className="text-lg font-semibold text-gray-900">{user.name}</p>
                            <p className="text-sm text-gray-500">{user.role === 'admin' ? 'Administrator' : 'Xodim'}</p>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        {user.role === 'admin' && (
                            <button
                                onClick={onSwitchToAdmin}
                                className="p-2 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 transition-colors"
                                aria-label="Switch to Admin Dashboard"
                            >
                                Admin Panel
                            </button>
                        )}
                        <button onClick={handleLogout} className="text-gray-400 hover:text-red-500">
                            <LogOut size={20} />
                        </button>
                    </div>
                </div>

                {/* Today's Attendance */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 mb-6">
                    <div className="flex items-center justify-between mb-3">
                        <h2 className="text-sm font-medium text-gray-500">Bugungi davomat</h2>
                        <span className="text-xs text-gray-400">{new Date().toLocaleDateString('uz-UZ', { weekday: 'short', day: 'numeric', month: 'short' })}</span>
                    </div>
                    {todayAttendance.length > 0 ? (
                        <div className="space-y-3">
                            {todayAttendance.map((record: any) => (
                                <div key={record.id} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                                    <div className="flex items-center space-x-3">
                                        {record.status === 'present' ? (
                                            <CheckCircle className="text-green-500" size={20} />
                                        ) : (
                                            <Clock className="text-yellow-500" size={20} />
                                        )}
                                        <div>
                                            <p className="font-medium text-gray-900">
                                                {record.schedule ? record.schedule.name : 'Dars'}
                                            </p>
                                            <p className="text-xs text-gray-500">
                                                {new Date(record.check_in_time).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })}
                                            </p>
                                        </div>
                                    </div>
                                    <span className={`px-2 py-1 rounded text-xs font-medium ${record.status === 'present' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                                        }`}>
                                        {record.status === 'present' ? 'Keldi' : 'Kechikdi'}
                                    </span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-4 text-gray-400 text-sm">
                            Bugun hali davomat qilinmadi
                        </div>
                    )}
                </div>

                {/* Monthly Stats */}
                {stats && (
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                            <div className="flex items-center space-x-2 mb-2">
                                <CheckCircle className="text-green-500" size={16} />
                                <span className="text-xs text-gray-500">Kelgan</span>
                            </div>
                            <p className="text-2xl font-bold text-gray-900">{stats.present_count}</p>
                            <p className="text-xs text-gray-400">Bu oy</p>
                        </div>
                        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
                            <div className="flex items-center space-x-2 mb-2">
                                <Clock className="text-yellow-500" size={16} />
                                <span className="text-xs text-gray-500">Kechikkan</span>
                            </div>
                            <p className="text-2xl font-bold text-gray-900">{stats.late_count}</p>
                            <p className="text-xs text-gray-400">Bu oy</p>
                        </div>
                    </div>
                )}

                {/* Schedule Preview (Placeholder) */}
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between mb-3">
                        <h2 className="text-sm font-medium text-gray-500">Dars jadvali</h2>
                        <span className="text-xs text-blue-600">Bugun</span>
                    </div>
                    {/* Logic to show today's schedule would go here */}
                    <div className="text-center py-4 text-gray-400 text-sm">
                        Jadval yuklanmoqda...
                    </div>
                </div>
            </div>
        </div>
    )
}
