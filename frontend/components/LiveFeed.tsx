'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api-client'
import { Clock, User, AlertCircle, CheckCircle } from 'lucide-react'

interface AttendanceRecord {
    id: number
    user_id: number
    user_name: string
    employee_id: string
    check_in_time: string
    confidence: number
    image_path?: string
    status: 'present' | 'late'
    schedule_name?: string
}

export default function LiveFeed() {
    const [records, setRecords] = useState<AttendanceRecord[]>([])
    const [loading, setLoading] = useState(true)
    const [lastUpdate, setLastUpdate] = useState<Date | null>(null)

    const fetchAttendance = async () => {
        try {
            const response = await api.getTodayAttendance()
            if (response.data.success) {
                // Sort by time descending (newest first)
                const sorted = response.data.attendance.sort((a: AttendanceRecord, b: AttendanceRecord) =>
                    new Date(b.check_in_time).getTime() - new Date(a.check_in_time).getTime()
                )
                setRecords(sorted.slice(0, 5)) // Keep only latest 5
                setLastUpdate(new Date())
            }
        } catch (error) {
            console.error('Error fetching live feed:', error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchAttendance()
        const interval = setInterval(fetchAttendance, 5000) // Poll every 5 seconds
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-blue-50 to-white">
                <div className="flex items-center gap-2">
                    <div className="relative">
                        <span className="absolute -top-1 -right-1 flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                        </span>
                        <Clock className="w-5 h-5 text-blue-600" />
                    </div>
                    <h3 className="font-bold text-gray-900">Jonli Davomat</h3>
                </div>
                <span className="text-xs text-gray-500">
                    Yangilandi: {lastUpdate ? lastUpdate.toLocaleTimeString() : ''}
                </span>
            </div>

            <div className="divide-y divide-gray-100">
                {loading && records.length === 0 ? (
                    <div className="p-8 text-center text-gray-500">
                        <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mb-2"></div>
                        <p className="text-sm">Yuklanmoqda...</p>
                    </div>
                ) : records.length === 0 ? (
                    <div className="p-8 text-center text-gray-500">
                        <User className="w-10 h-10 mx-auto mb-2 text-gray-300" />
                        <p className="text-sm">Bugun hali hech kim kelmadi</p>
                    </div>
                ) : (
                    records.map((record) => (
                        <div key={record.id} className="p-4 hover:bg-gray-50 transition-colors animate-in slide-in-from-left-2 duration-300">
                            <div className="flex items-start gap-3">
                                {/* User Avatar */}
                                <div className="relative flex-shrink-0">
                                    {record.image_path ? (
                                        <img
                                            src={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/${record.image_path}`}
                                            alt={record.user_name}
                                            className="w-12 h-12 rounded-full object-cover border-2 border-white shadow-sm"
                                        />
                                    ) : (
                                        <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center border-2 border-white shadow-sm">
                                            <User className="w-6 h-6 text-gray-400" />
                                        </div>
                                    )}
                                    <div className={`absolute -bottom-1 -right-1 rounded-full p-1 border-2 border-white ${record.status === 'present' ? 'bg-green-100' : 'bg-yellow-100'
                                        }`}>
                                        {record.status === 'present' ? (
                                            <CheckCircle className={`w-3 h-3 ${record.status === 'present' ? 'text-green-600' : 'text-yellow-600'}`} />
                                        ) : (
                                            <AlertCircle className="w-3 h-3 text-yellow-600" />
                                        )}
                                    </div>
                                </div>

                                {/* Info */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-start">
                                        <h4 className="font-semibold text-gray-900 truncate">
                                            {record.user_name}
                                        </h4>
                                        <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                                            {new Date(record.check_in_time).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                    <p className="text-xs text-gray-500 truncate mb-1">
                                        ID: {record.employee_id}
                                    </p>
                                    <div className="flex items-center gap-2">
                                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${record.status === 'present'
                                            ? 'bg-green-100 text-green-800'
                                            : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                            {record.status === 'present' ? 'O\'z vaqtida' : 'Kechikdi'}
                                        </span>
                                        {record.schedule_name && (
                                            <span className="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded truncate max-w-[120px]">
                                                {record.schedule_name}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {
                records.length > 0 && (
                    <div className="p-3 bg-gray-50 border-t border-gray-100 text-center">
                        <a href="/attendance" className="text-xs font-medium text-blue-600 hover:text-blue-800 hover:underline">
                            Barcha davomatni ko'rish &rarr;
                        </a>
                    </div>
                )
            }
        </div >
    )
}
