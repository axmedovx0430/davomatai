'use client'

import { useAttendanceStats } from '@/hooks/use-api'
import { useWeekSchedules, useScheduleStats, useScheduleAttendance, useCreateSchedule, useUpdateSchedule, useDeleteSchedule, Schedule } from '@/hooks/use-schedules'
import { useGroups } from '@/hooks/use-groups'
import { Users, UserCheck, Clock, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import ImageModal from '@/components/ImageModal'
import WeekSelector from '@/components/WeekSelector'
import WeeklyScheduleGrid from '@/components/WeeklyScheduleGrid'
import ScheduleModal from '@/components/ScheduleModal'
import LiveFeed from '@/components/LiveFeed'
import ProtectedRoute from '@/components/ProtectedRoute'

// Type definitions
interface AttendanceRecord {
    id: number
    user_id: number
    user_name: string
    employee_id: string
    check_in_time: string
    confidence: number
    image_path?: string
    status: 'present' | 'late'
    device_id?: number
    device_name?: string
    schedule_id?: number
    schedule_name?: string
}

export default function HomePage() {
    const router = useRouter()
    const [currentYear, setCurrentYear] = useState(0)
    const [currentWeek, setCurrentWeek] = useState(0)
    const [selectedSchedule, setSelectedSchedule] = useState<Schedule | null>(null)
    const [selectedDate, setSelectedDate] = useState('')
    const [weekDates, setWeekDates] = useState<string[]>([])
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [editingSchedule, setEditingSchedule] = useState<Schedule | null>(null)
    const [defaultDayOfWeek, setDefaultDayOfWeek] = useState<number | undefined>(undefined)
    const [selectedImage, setSelectedImage] = useState<string | null>(null)
    const [selectedRecord, setSelectedRecord] = useState<AttendanceRecord | null>(null)
    const [selectedGroupId, setSelectedGroupId] = useState<string>('')

    // Initialize current week
    useEffect(() => {
        const now = new Date()
        const year = now.getFullYear()
        const week = getISOWeek(now)
        setCurrentYear(year)
        setCurrentWeek(week)

        // Calculate week dates
        const dates = getWeekDates(year, week)
        setWeekDates(dates)
        setSelectedDate(dates[0]) // Default to Monday
    }, [])

    // Update week dates when week changes
    useEffect(() => {
        if (currentYear && currentWeek) {
            const dates = getWeekDates(currentYear, currentWeek)
            setWeekDates(dates)
            if (!selectedDate || !dates.includes(selectedDate)) {
                setSelectedDate(dates[0])
            }
        }
    }, [currentYear, currentWeek])

    const getISOWeek = (date: Date) => {
        const target = new Date(date.valueOf())
        const dayNr = (date.getDay() + 6) % 7
        target.setDate(target.getDate() - dayNr + 3)
        const jan4 = new Date(target.getFullYear(), 0, 4)
        const dayDiff = (target.getTime() - jan4.getTime()) / 86400000
        return 1 + Math.ceil(dayDiff / 7)
    }

    const getWeekDates = (year: number, week: number): string[] => {
        const jan4 = new Date(year, 0, 4)
        const daysToMonday = (jan4.getDay() + 6) % 7
        const firstMonday = new Date(year, 0, 4 - daysToMonday)
        const weekStart = new Date(firstMonday.getTime() + (week - 1) * 7 * 24 * 60 * 60 * 1000)

        const dates: string[] = []
        for (let i = 0; i < 7; i++) {
            const date = new Date(weekStart.getTime() + i * 24 * 60 * 60 * 1000)
            const year = date.getFullYear()
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const day = String(date.getDate()).padStart(2, '0')
            dates.push(`${year}-${month}-${day}`)
        }
        return dates
    }

    // Fetch data
    const { data: weeklyStats, isLoading: statsLoading } = useAttendanceStats()
    const { data: schedules, isLoading: schedulesLoading, refetch: refetchSchedules } = useWeekSchedules(weekDates[0], weekDates[6])
    const { data: scheduleStats } = useScheduleStats(selectedSchedule?.id || null, selectedDate)
    const { data: scheduleAttendance } = useScheduleAttendance(selectedSchedule?.id || null, selectedDate)
    const { data: groups } = useGroups()

    // Mutations
    const createSchedule = useCreateSchedule()
    const updateSchedule = useUpdateSchedule()
    const deleteSchedule = useDeleteSchedule()

    // Determine which stats to show
    const stats = selectedSchedule && scheduleStats ? scheduleStats : (weeklyStats?.stats || {})

    // Filter schedules by group
    const filteredSchedules = (() => {
        if (!schedules) return {}
        if (!selectedGroupId) return schedules

        const filtered: { [key: string]: Schedule[] } = {}
        Object.keys(schedules).forEach(day => {
            filtered[day] = schedules[day].filter((s: Schedule) =>
                !s.group_id || s.group_id.toString() === selectedGroupId
            )
        })
        return filtered
    })()

    const handleWeekChange = (year: number, week: number) => {
        setCurrentYear(year)
        setCurrentWeek(week)
        setSelectedSchedule(null)
    }

    const handleScheduleClick = (schedule: Schedule, date: string) => {
        setSelectedSchedule(schedule)
        setSelectedDate(date)
        // Set group filter based on selected schedule
        if (schedule.group_id) {
            setSelectedGroupId(schedule.group_id.toString())
        }
    }

    const handleAddSchedule = (dayOfWeek: number) => {
        setEditingSchedule(null)
        setDefaultDayOfWeek(dayOfWeek)
        setIsModalOpen(true)
    }

    const handleEditSchedule = (schedule: Schedule) => {
        setEditingSchedule(schedule)
        setDefaultDayOfWeek(undefined)
        setIsModalOpen(true)
    }

    const handleSaveSchedule = async (scheduleData: any) => {
        try {
            if (editingSchedule) {
                const updatedSchedule = await updateSchedule.mutateAsync({ id: editingSchedule.id, ...scheduleData })
                // Update selected schedule if it's the one being edited
                if (selectedSchedule?.id === editingSchedule.id) {
                    setSelectedSchedule(updatedSchedule.schedule)
                }
            } else {
                await createSchedule.mutateAsync(scheduleData)
            }
            refetchSchedules()
        } catch (error: any) {
            console.error('Failed to save schedule:', error)
            const errorMessage = error?.response?.data?.detail || error?.message || 'Xatolik yuz berdi!'
            alert(`Xatolik: ${errorMessage}`)
        }
    }

    const handleDeleteSchedule = async (scheduleId: number) => {
        try {
            await deleteSchedule.mutateAsync(scheduleId)
            if (selectedSchedule?.id === scheduleId) {
                setSelectedSchedule(null)
            }
            refetchSchedules()
        } catch (error) {
            console.error('Failed to delete schedule:', error)
            alert('Xatolik yuz berdi!')
        }
    }

    const attendance = scheduleAttendance || []

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
                {/* Header */}
                <header className="bg-white shadow-sm border-b">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <h1 className="text-3xl font-bold text-gray-900">Davomat Tizimi</h1>
                                <p className="text-gray-600 mt-1">ESP32-CAM yuz tanish asosida</p>
                            </div>
                            <nav className="flex gap-4">
                                <Link
                                    href="/"
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                                >
                                    Dashboard
                                </Link>
                                <Link
                                    href="/users"
                                    className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                                >
                                    Foydalanuvchilar
                                </Link>
                                <Link
                                    href="/attendance"
                                    className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                                >
                                    Davomat
                                </Link>
                                <Link
                                    href="/devices"
                                    className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                                >
                                    Qurilmalar
                                </Link>
                                <Link
                                    href="/groups"
                                    className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                                >
                                    Guruhlar
                                </Link>
                            </nav>
                        </div>
                    </div>
                </header>

                {/* Main Content */}
                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {/* Stats Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        <StatCard
                            title="Jami Xodimlar"
                            value={stats.total_users || 0}
                            icon={<Users className="w-8 h-8" />}
                            color="bg-blue-500"
                            loading={statsLoading}
                            onClick={() => router.push(selectedGroupId ? `/users?group_id=${selectedGroupId}` : '/users')}
                        />
                        <StatCard
                            title="Kelganlar"
                            value={stats.present || 0}
                            icon={<UserCheck className="w-8 h-8" />}
                            color="bg-green-500"
                            loading={statsLoading}
                            onClick={() => router.push(selectedGroupId ? `/attendance?status=present&group_id=${selectedGroupId}` : '/attendance?status=present')}
                        />
                        <StatCard
                            title="Kechikkanlar"
                            value={stats.late || 0}
                            icon={<Clock className="w-8 h-8" />}
                            color="bg-yellow-500"
                            loading={statsLoading}
                            onClick={() => router.push(selectedGroupId ? `/attendance?status=late&group_id=${selectedGroupId}` : '/attendance?status=late')}
                        />
                        <StatCard
                            title="Kelmaganlar"
                            value={stats.absent || 0}
                            icon={<AlertCircle className="w-8 h-8" />}
                            color="bg-red-500"
                            loading={statsLoading}
                            onClick={() => router.push(selectedGroupId ? `/attendance?status=absent&group_id=${selectedGroupId}` : '/attendance?status=absent')}
                        />
                    </div>

                    {/* Main Grid Layout */}
                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                        {/* Left Column (Main Content) */}
                        <div className="lg:col-span-3 space-y-8">
                            {/* Selected Schedule Info */}
                            {selectedSchedule && (
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <span className="text-sm text-blue-600 font-medium">Tanlangan dars:</span>
                                            <span className="ml-2 text-lg font-bold text-blue-900">
                                                {selectedSchedule.name}
                                            </span>
                                            <span className="ml-2 text-sm text-blue-600">
                                                ({selectedSchedule.start_time} - {selectedSchedule.end_time})
                                            </span>
                                        </div>
                                        <button
                                            onClick={() => setSelectedSchedule(null)}
                                            className="px-3 py-1 text-sm bg-white text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                                        >
                                            Barcha darslar
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Week Selector */}
                            {currentYear > 0 && currentWeek > 0 && (
                                <div className="space-y-4">
                                    <WeekSelector
                                        year={currentYear}
                                        week={currentWeek}
                                        onWeekChange={handleWeekChange}
                                    />

                                    {/* Group Filter */}
                                    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Guruh bo'yicha filtrlash
                                        </label>
                                        <select
                                            value={selectedGroupId}
                                            onChange={(e) => setSelectedGroupId(e.target.value)}
                                            className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        >
                                            <option value="">Barcha guruhlar</option>
                                            {groups?.map((group: any) => (
                                                <option key={group.id} value={group.id}>
                                                    {group.name} ({group.code})
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                </div>
                            )}

                            {/* Weekly Schedule Grid */}
                            <div className="card">
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-2xl font-bold text-gray-900">Bu hafta</h2>
                                </div>

                                {schedulesLoading ? (
                                    <div className="text-center py-12">
                                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                                        <p className="mt-4 text-gray-600">Yuklanmoqda...</p>
                                    </div>
                                ) : (
                                    <WeeklyScheduleGrid
                                        schedules={filteredSchedules}
                                        onScheduleClick={handleScheduleClick}
                                        onAddSchedule={handleAddSchedule}
                                        onEditSchedule={handleEditSchedule}
                                        onDeleteSchedule={handleDeleteSchedule}
                                        selectedScheduleId={selectedSchedule?.id || null}
                                        weekDates={weekDates}
                                        groups={groups}
                                    />
                                )}
                            </div>
                        </div>

                        {/* Attendance Table */}
                        {selectedSchedule && (
                            <div className="card">
                                <h3 className="text-xl font-bold text-gray-900 mb-4">
                                    {selectedSchedule.name} - Davomat
                                </h3>

                                {attendance.length === 0 ? (
                                    <div className="text-center py-12">
                                        <AlertCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                                        <p className="text-gray-600">Bu darsda hozircha davomat yo'q</p>
                                    </div>
                                ) : (
                                    <div className="overflow-x-auto">
                                        <table className="w-full">
                                            <thead className="bg-gray-50 border-b">
                                                <tr>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                        Xodim
                                                    </th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                        ID
                                                    </th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                        Vaqt
                                                    </th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                        Ishonch
                                                    </th>
                                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                                        Status
                                                    </th>
                                                </tr>
                                            </thead>
                                            <tbody className="bg-white divide-y divide-gray-200">
                                                {attendance.map((record: AttendanceRecord) => (
                                                    <tr key={record.id} className="hover:bg-gray-50">
                                                        <td className="px-6 py-4 whitespace-nowrap">
                                                            <div className="font-medium text-gray-900">{record.user_name}</div>
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                            {record.employee_id}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                            {new Date(record.check_in_time).toLocaleTimeString('uz-UZ')}
                                                        </td>
                                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                            <button
                                                                onClick={() => {
                                                                    if (record.image_path) {
                                                                        const imageUrl = `${process.env.NEXT_PUBLIC_API_URL || ''}/${record.image_path}`
                                                                        setSelectedImage(imageUrl)
                                                                        setSelectedRecord(record)
                                                                    } else {
                                                                        alert('Rasm mavjud emas')
                                                                    }
                                                                }}
                                                                className={`text-blue-600 hover:text-blue-800 font-medium ${record.image_path ? 'cursor-pointer underline' : 'cursor-not-allowed text-gray-400'}`}
                                                                disabled={!record.image_path}
                                                            >
                                                                {(record.confidence * 100).toFixed(1)}%
                                                            </button>
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
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Groups Section */}
                        <div className="pt-4">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-xl font-bold text-gray-900">Guruhlar</h2>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {groups?.map((group: any) => (
                                    <div key={group.id} className="bg-white rounded-lg shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow">
                                        <div className="flex justify-between items-start mb-4">
                                            <div>
                                                <h3 className="font-bold text-lg text-gray-900">{group.name}</h3>
                                                <p className="text-sm text-gray-500">{group.code}</p>
                                            </div>
                                            <div className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                                                {group.student_count} talaba
                                            </div>
                                        </div>
                                        <div className="text-sm text-gray-600">
                                            <p>{group.faculty || 'Fakultet ko\'rsatilmagan'}</p>
                                            <p>{group.course}-kurs, {group.semester}-semestr</p>
                                        </div>
                                    </div>
                                ))}
                                {(!groups || groups.length === 0) && (
                                    <div className="col-span-full text-center py-8 text-gray-500 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                                        Hozircha guruhlar yo'q
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Right Column (Live Feed) */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-8">
                            <LiveFeed />
                        </div>
                    </div>
                </main>

                {/* Schedule Modal */}
                <ScheduleModal
                    isOpen={isModalOpen}
                    onClose={() => {
                        setIsModalOpen(false)
                        setEditingSchedule(null)
                        setDefaultDayOfWeek(undefined)
                    }}
                    onSave={handleSaveSchedule}
                    schedule={editingSchedule}
                    defaultDayOfWeek={defaultDayOfWeek}
                    defaultEffectiveFrom={weekDates[0]}
                    defaultEffectiveTo={weekDates[6]}
                />

                {/* Image Modal */}
                <ImageModal
                    imageUrl={selectedImage}
                    onClose={() => {
                        setSelectedImage(null)
                        setSelectedRecord(null)
                    }}
                    userName={selectedRecord?.user_name}
                    confidence={selectedRecord?.confidence}
                />
            </div>
        </ProtectedRoute>
    )
}

function StatCard({ title, value, icon, color, loading, onClick }: any) {
    return (
        <div
            onClick={onClick}
            className="card cursor-pointer hover:shadow-lg transition-all transform hover:-translate-y-1 active:scale-95"
        >
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm text-gray-600 mb-1">{title}</p>
                    {loading ? (
                        <div className="h-8 w-16 bg-gray-200 animate-pulse rounded"></div>
                    ) : (
                        <p className="text-3xl font-bold text-gray-900">{value}</p>
                    )}
                </div>
                <div className={`${color} text-white p-3 rounded-lg shadow-md`}>
                    {icon}
                </div>
            </div>
        </div>
    )
}
