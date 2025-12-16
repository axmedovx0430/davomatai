'use client'

import { useAttendance, useUsers } from '@/hooks/use-api'
import { useState, useMemo } from 'react'
import { ArrowLeft, Download } from 'lucide-react'
import Link from 'next/link'

import { useSearchParams } from 'next/navigation'

export default function AttendancePage() {
    const searchParams = useSearchParams()
    const groupId = searchParams.get('group_id')
    const status = searchParams.get('status')

    const [startDate, setStartDate] = useState(
        new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    )
    const [endDate, setEndDate] = useState(new Date().toISOString().split('T')[0])

    const { data, isLoading } = useAttendance({
        start_date: startDate,
        end_date: endDate,
        group_id: groupId,
    })

    // Get users for absent calculation
    const userParams: any = { is_active: true }
    if (groupId) {
        userParams.group_id = groupId
    }
    const { data: usersData, isLoading: usersLoading } = useUsers(userParams)

    // Filter by status if provided
    let attendance = data?.attendance || []
    if (status && status !== 'absent') {
        attendance = attendance.filter((record: any) => record.status === status)
    }

    // Calculate absent users
    const absentUsers = useMemo(() => {
        if (status !== 'absent' || !usersData?.users) return []

        const attendedUserIds = new Set(attendance.map((r: any) => r.user_id))
        return usersData.users.filter((user: any) => !attendedUserIds.has(user.id))
    }, [status, usersData, attendance])

    const exportToCSV = () => {
        const headers = ['Ism', 'ID', 'Vaqt', 'Ishonch', 'Status']
        const rows = attendance.map((r: any) => [
            r.user_name,
            r.employee_id,
            new Date(r.check_in_time).toLocaleString('uz-UZ'),
            `${(r.confidence * 100).toFixed(1)}%`,
            r.status === 'present' ? 'Keldi' : 'Kechikdi'
        ])

        const csv = [headers, ...rows].map(row => row.join(',')).join('\n')
        const blob = new Blob([csv], { type: 'text/csv' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `davomat_${startDate}_${endDate}.csv`
        a.click()
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Link href="/" className="text-gray-600 hover:text-gray-900">
                                <ArrowLeft className="w-6 h-6" />
                            </Link>
                            <h1 className="text-3xl font-bold text-gray-900">Davomat Tarixi</h1>
                        </div>
                        <button onClick={exportToCSV} className="btn btn-primary flex items-center gap-2">
                            <Download className="w-5 h-5" />
                            CSV Export
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Filters */}
                <div className="card mb-6">
                    <h2 className="text-xl font-bold mb-4">Filtr</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Boshlanish Sanasi
                            </label>
                            <input
                                type="date"
                                className="input"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Tugash Sanasi
                            </label>
                            <input
                                type="date"
                                className="input"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                {/* Attendance Table */}
                <div className="card">
                    <h2 className="text-xl font-bold mb-4">
                        Davomat Yozuvlari ({status === 'absent' ? absentUsers.length : attendance.length})
                        {status && status !== 'absent' && (
                            <span className="ml-2 text-sm font-normal text-gray-600">
                                - {status === 'present' ? 'Kelganlar' : status === 'late' ? 'Kechikkanlar' : ''}
                            </span>
                        )}
                        {status === 'absent' && (
                            <span className="ml-2 text-sm font-normal text-gray-600">
                                - Kelmaganlar
                            </span>
                        )}
                    </h2>

                    {isLoading || usersLoading ? (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                        </div>
                    ) : status === 'absent' ? (
                        absentUsers.length === 0 ? (
                            <div className="text-center py-12">
                                <div className="text-gray-600">
                                    <p className="mb-4">Barcha foydalanuvchilar davomat bergan!</p>
                                </div>
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50 border-b">
                                        <tr>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Xodim</th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Telefon</th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white divide-y divide-gray-200">
                                        {absentUsers.map((user: any) => (
                                            <tr key={user.id} className="hover:bg-gray-50">
                                                <td className="px-6 py-4 whitespace-nowrap font-medium">{user.full_name}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.employee_id}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.phone || '-'}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.email || '-'}</td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                                        Kelmagan
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50 border-b">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Xodim</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sana</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vaqt</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ishonch</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {attendance.map((record: any) => {
                                        const date = new Date(record.check_in_time)
                                        return (
                                            <tr key={record.id} className="hover:bg-gray-50">
                                                <td className="px-6 py-4 whitespace-nowrap font-medium">{record.user_name}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{record.employee_id}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {date.toLocaleDateString('uz-UZ')}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {date.toLocaleTimeString('uz-UZ')}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {(record.confidence * 100).toFixed(1)}%
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${record.status === 'present'
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-yellow-100 text-yellow-800'
                                                        }`}>
                                                        {record.status === 'present' ? 'Keldi' : 'Kechikdi'}
                                                    </span>
                                                </td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </main>
        </div>
    )
}
