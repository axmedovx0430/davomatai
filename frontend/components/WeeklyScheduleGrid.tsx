/**
 * Weekly Schedule Grid Component
 * Displays 7-day schedule with classes
 */
'use client'

import { Plus, Edit2, Trash2, Users } from 'lucide-react'
import { Schedule } from '@/hooks/use-schedules'
import { Group } from '@/hooks/use-groups'

interface WeeklyScheduleGridProps {
    schedules: { [day: string]: Schedule[] }
    onScheduleClick: (schedule: Schedule, date: string) => void
    onAddSchedule: (dayOfWeek: number) => void
    onEditSchedule: (schedule: Schedule) => void
    onDeleteSchedule: (scheduleId: number) => void
    selectedScheduleId: number | null
    weekDates: string[]
    groups?: Group[]
}

export default function WeeklyScheduleGrid({
    schedules,
    onScheduleClick,
    onAddSchedule,
    onEditSchedule,
    onDeleteSchedule,
    selectedScheduleId,
    weekDates,
    groups
}: WeeklyScheduleGridProps) {
    const weekdays = [
        'Dushanba',
        'Seshanba',
        'Chorshanba',
        'Payshanba',
        'Juma',
        'Shanba',
        'Yakshanba'
    ]

    const getDateForDay = (dayIndex: number) => {
        return weekDates[dayIndex] || ''
    }

    const getGroupName = (groupId?: number) => {
        if (!groupId || !groups) return null
        return groups.find(g => g.id === groupId)?.name
    }

    return (
        <div className="grid grid-cols-7 gap-4">
            {weekdays.map((day, dayIndex) => {
                const daySchedules = schedules[dayIndex.toString()] || []
                const dateStr = getDateForDay(dayIndex)

                return (
                    <div key={dayIndex} className="bg-white rounded-lg shadow-sm overflow-hidden">
                        {/* Day header */}
                        <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-3">
                            <div className="font-semibold text-sm">{day}</div>
                            <div className="text-xs opacity-90">{dateStr}</div>
                        </div>

                        {/* Classes */}
                        <div className="p-2 space-y-2 min-h-[400px]">
                            {daySchedules.map((schedule) => {
                                const groupName = getGroupName(schedule.group_id)

                                return (
                                    <div
                                        key={schedule.id}
                                        onClick={() => onScheduleClick(schedule, dateStr)}
                                        className={`
                                        group relative p-3 rounded-lg cursor-pointer transition-all
                                        ${selectedScheduleId === schedule.id
                                                ? 'bg-blue-100 border-2 border-blue-500 shadow-md'
                                                : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                                            }
                                    `}
                                    >
                                        <div className="font-medium text-sm text-gray-900 mb-1">
                                            {schedule.name}
                                        </div>
                                        {groupName && (
                                            <div className="flex items-center gap-1 text-xs text-blue-600 font-medium mb-1">
                                                <Users className="w-3 h-3" />
                                                {groupName}
                                            </div>
                                        )}
                                        <div className="text-xs text-gray-600">
                                            {schedule.start_time} - {schedule.end_time}
                                        </div>

                                        {/* Edit/Delete buttons (show on hover) */}
                                        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    onEditSchedule(schedule)
                                                }}
                                                className="p-1 bg-white rounded shadow-sm hover:bg-blue-50"
                                                title="Tahrirlash"
                                            >
                                                <Edit2 className="w-3 h-3 text-blue-600" />
                                            </button>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    if (confirm(`"${schedule.name}" darsini o'chirmoqchimisiz?`)) {
                                                        onDeleteSchedule(schedule.id)
                                                    }
                                                }}
                                                className="p-1 bg-white rounded shadow-sm hover:bg-red-50"
                                                title="O'chirish"
                                            >
                                                <Trash2 className="w-3 h-3 text-red-600" />
                                            </button>
                                        </div>
                                    </div>
                                )
                            })}

                            {/* Add button */}
                            <button
                                onClick={() => onAddSchedule(dayIndex)}
                                className="w-full p-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors flex items-center justify-center gap-2 text-gray-600 hover:text-blue-600"
                            >
                                <Plus className="w-4 h-4" />
                                <span className="text-sm">Dars qo'shish</span>
                            </button>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}
