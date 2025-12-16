/**
 * Schedule Modal Component
 * Modal for adding/editing class schedules
 */
'use client'

import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { Schedule } from '@/hooks/use-schedules'
import { useGroups } from '@/hooks/use-groups'

interface ScheduleModalProps {
    isOpen: boolean
    onClose: () => void
    onSave: (scheduleData: {
        name: string
        day_of_week: number
        start_time: string
        end_time: string
        group_id?: number
        late_threshold_minutes?: number
        duplicate_check_minutes?: number
        effective_from?: string
        effective_to?: string
        teacher?: string
        room?: string
    }) => void
    schedule?: Schedule | null
    defaultDayOfWeek?: number
    defaultEffectiveFrom?: string
    defaultEffectiveTo?: string
}

export default function ScheduleModal({
    isOpen,
    onClose,
    onSave,
    schedule,
    defaultDayOfWeek,
    defaultEffectiveFrom,
    defaultEffectiveTo
}: ScheduleModalProps) {
    const [name, setName] = useState('')
    const [dayOfWeek, setDayOfWeek] = useState(0)
    const [startTime, setStartTime] = useState('09:00')
    const [endTime, setEndTime] = useState('10:30')
    const [groupId, setGroupId] = useState<string>('')
    const [lateThreshold, setLateThreshold] = useState<string>('')
    const [duplicateCheck, setDuplicateCheck] = useState<string>('')
    const [effectiveFrom, setEffectiveFrom] = useState<string>('')
    const [effectiveTo, setEffectiveTo] = useState<string>('')
    const [teacher, setTeacher] = useState('')
    const [room, setRoom] = useState('')
    const [showSettings, setShowSettings] = useState(false)
    const [errors, setErrors] = useState<{ [key: string]: string }>({})

    const { data: groups } = useGroups()

    const weekdays = [
        'Dushanba',
        'Seshanba',
        'Chorshanba',
        'Payshanba',
        'Juma',
        'Shanba',
        'Yakshanba'
    ]

    useEffect(() => {
        if (schedule) {
            // Edit mode
            setName(schedule.name)
            setDayOfWeek(schedule.day_of_week)
            setStartTime(schedule.start_time)
            setEndTime(schedule.end_time)
            setGroupId(schedule.group_id?.toString() || '')
            setLateThreshold(schedule.late_threshold_minutes?.toString() || '')
            setDuplicateCheck(schedule.duplicate_check_minutes?.toString() || '')
            setEffectiveFrom(schedule.effective_from || '')
            setEffectiveTo(schedule.effective_to || '')
            setTeacher(schedule.teacher || '')
            setRoom(schedule.room || '')
        } else if (defaultDayOfWeek !== undefined) {
            // Add mode with default day
            setName('')
            setDayOfWeek(defaultDayOfWeek)
            setStartTime('09:00')
            setEndTime('10:30')
            setGroupId('')
            setLateThreshold('')
            setDuplicateCheck('')
            setEffectiveFrom(defaultEffectiveFrom || '')
            setEffectiveTo(defaultEffectiveTo || '')
            setTeacher('')
            setRoom('')
        } else {
            // Reset
            setName('')
            setDayOfWeek(0)
            setStartTime('09:00')
            setEndTime('10:30')
            setGroupId('')
            setLateThreshold('')
            setDuplicateCheck('')
            setEffectiveFrom(defaultEffectiveFrom || '')
            setEffectiveTo(defaultEffectiveTo || '')
            setTeacher('')
            setRoom('')
        }
        setErrors({})
        setShowSettings(false)
    }, [schedule, defaultDayOfWeek, isOpen])

    const validate = () => {
        const newErrors: { [key: string]: string } = {}

        if (!name.trim()) {
            newErrors.name = 'Dars nomini kiriting'
        }

        if (!startTime) {
            newErrors.startTime = 'Boshlanish vaqtini kiriting'
        }

        if (!endTime) {
            newErrors.endTime = 'Tugash vaqtini kiriting'
        }

        if (startTime && endTime && startTime >= endTime) {
            newErrors.endTime = 'Tugash vaqti boshlanish vaqtidan kech bo\'lishi kerak'
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()

        if (!validate()) return

        onSave({
            name: name.trim(),
            day_of_week: dayOfWeek,
            start_time: startTime,
            end_time: endTime,
            group_id: groupId ? parseInt(groupId) : undefined,
            late_threshold_minutes: lateThreshold ? parseInt(lateThreshold) : undefined,
            duplicate_check_minutes: duplicateCheck ? parseInt(duplicateCheck) : undefined,
            effective_from: effectiveFrom || undefined,
            effective_to: effectiveTo || undefined,
            teacher: teacher.trim() || undefined,
            room: room.trim() || undefined
        })

        onClose()
    }

    if (!isOpen) return null

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b">
                    <h2 className="text-xl font-bold text-gray-900">
                        {schedule ? 'Darsni tahrirlash' : 'Yangi dars qo\'shish'}
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-600" />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {/* Class name */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Dars nomi *
                        </label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.name ? 'border-red-500' : 'border-gray-300'
                                }`}
                            placeholder="Masalan: Matematika"
                        />
                        {errors.name && (
                            <p className="mt-1 text-sm text-red-600">{errors.name}</p>
                        )}
                    </div>

                    {/* Group Selector */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Guruh (Ixtiyoriy)
                        </label>
                        <select
                            value={groupId}
                            onChange={(e) => setGroupId(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Barcha guruhlar uchun</option>
                            {groups?.map((group) => (
                                <option key={group.id} value={group.id}>
                                    {group.name} ({group.code})
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Teacher and Room */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                O'qituvchi (Ixtiyoriy)
                            </label>
                            <input
                                type="text"
                                value={teacher}
                                onChange={(e) => setTeacher(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Masalan: Karimov A."
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Xona (Ixtiyoriy)
                            </label>
                            <input
                                type="text"
                                value={room}
                                onChange={(e) => setRoom(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                placeholder="Masalan: 101"
                            />
                        </div>
                    </div>

                    {/* Day of week and Settings */}
                    <div className="flex gap-4">
                        <div className="flex-1">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Kun *
                            </label>
                            <select
                                value={dayOfWeek}
                                onChange={(e) => setDayOfWeek(parseInt(e.target.value))}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                {weekdays.map((day, index) => (
                                    <option key={index} value={index}>
                                        {day}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="flex items-end">
                            <button
                                type="button"
                                onClick={() => setShowSettings(!showSettings)}
                                className={`px-4 py-2 rounded-lg transition-colors mb-[1px] ${showSettings
                                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                            >
                                Sozlamalar
                            </button>
                        </div>
                    </div>

                    {/* Time range */}
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Boshlanish *
                            </label>
                            <input
                                type="time"
                                value={startTime}
                                onChange={(e) => setStartTime(e.target.value)}
                                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.startTime ? 'border-red-500' : 'border-gray-300'
                                    }`}
                            />
                            {errors.startTime && (
                                <p className="mt-1 text-sm text-red-600">{errors.startTime}</p>
                            )}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Tugash *
                            </label>
                            <input
                                type="time"
                                value={endTime}
                                onChange={(e) => setEndTime(e.target.value)}
                                className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${errors.endTime ? 'border-red-500' : 'border-gray-300'
                                    }`}
                            />
                            {errors.endTime && (
                                <p className="mt-1 text-sm text-red-600">{errors.endTime}</p>
                            )}
                        </div>
                    </div>

                    {/* Advanced Settings */}
                    {showSettings && (
                        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-4 animate-in fade-in slide-in-from-top-2">
                            <h3 className="font-medium text-gray-900">Qo'shimcha Sozlamalar</h3>

                            {/* Date Range */}
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Boshlanish sanasi
                                    </label>
                                    <input
                                        type="date"
                                        value={effectiveFrom}
                                        onChange={(e) => setEffectiveFrom(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Tugash sanasi
                                    </label>
                                    <input
                                        type="date"
                                        value={effectiveTo}
                                        onChange={(e) => setEffectiveTo(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Kechikish chegarasi (daqiqa)
                                </label>
                                <input
                                    type="number"
                                    min="0"
                                    value={lateThreshold}
                                    onChange={(e) => setLateThreshold(e.target.value)}
                                    placeholder="Global sozlama (Default)"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Bo'sh qoldirilsa umumiy sozlama ishlatiladi
                                </p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Qayta davomat taqiqi (daqiqa)
                                </label>
                                <input
                                    type="number"
                                    min="0"
                                    value={duplicateCheck}
                                    onChange={(e) => setDuplicateCheck(e.target.value)}
                                    placeholder="Global sozlama (Default)"
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Bir xil o'quvchini qayta yozish oralig'i
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Buttons */}
                    <div className="flex gap-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            Bekor qilish
                        </button>
                        <button
                            type="submit"
                            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            {schedule ? 'Saqlash' : 'Qo\'shish'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
