/**
 * Week Selector Component
 * Allows navigation between weeks
 */
'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'

interface WeekSelectorProps {
    year: number
    week: number
    onWeekChange: (year: number, week: number) => void
}

export default function WeekSelector({ year, week, onWeekChange }: WeekSelectorProps) {
    const getWeekDateRange = (year: number, week: number) => {
        // Get first day of the week (Monday)
        const jan4 = new Date(year, 0, 4)
        const daysToMonday = (jan4.getDay() + 6) % 7
        const firstMonday = new Date(year, 0, 4 - daysToMonday)
        const weekStart = new Date(firstMonday.getTime() + (week - 1) * 7 * 24 * 60 * 60 * 1000)
        const weekEnd = new Date(weekStart.getTime() + 6 * 24 * 60 * 60 * 1000)

        const months = [
            'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
            'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr'
        ]

        const startDay = weekStart.getDate()
        const startMonth = months[weekStart.getMonth()]
        const endDay = weekEnd.getDate()
        const endMonth = months[weekEnd.getMonth()]
        const endYear = weekEnd.getFullYear()

        if (startMonth === endMonth) {
            return `${startDay}-${endDay} ${startMonth}, ${endYear}-yil`
        } else {
            return `${startDay} ${startMonth} - ${endDay} ${endMonth}, ${endYear}-yil`
        }
    }

    const handlePrevWeek = () => {
        if (week === 1) {
            // Go to last week of previous year
            const lastWeek = getWeeksInYear(year - 1)
            onWeekChange(year - 1, lastWeek)
        } else {
            onWeekChange(year, week - 1)
        }
    }

    const handleNextWeek = () => {
        const weeksInYear = getWeeksInYear(year)
        if (week === weeksInYear) {
            // Go to first week of next year
            onWeekChange(year + 1, 1)
        } else {
            onWeekChange(year, week + 1)
        }
    }

    const getWeeksInYear = (year: number) => {
        const dec31 = new Date(year, 11, 31)
        const jan1 = new Date(year, 0, 1)
        const day = dec31.getDay()

        if (day === 4 || (day === 3 && isLeapYear(year))) {
            return 53
        }
        return 52
    }

    const isLeapYear = (year: number) => {
        return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0)
    }

    const goToCurrentWeek = () => {
        const now = new Date()
        const currentYear = now.getFullYear()
        const currentWeek = getISOWeek(now)
        onWeekChange(currentYear, currentWeek)
    }

    const getISOWeek = (date: Date) => {
        const target = new Date(date.valueOf())
        const dayNr = (date.getDay() + 6) % 7
        target.setDate(target.getDate() - dayNr + 3)
        const jan4 = new Date(target.getFullYear(), 0, 4)
        const dayDiff = (target.getTime() - jan4.getTime()) / 86400000
        return 1 + Math.ceil(dayDiff / 7)
    }

    const isCurrentWeek = () => {
        const now = new Date()
        const currentYear = now.getFullYear()
        const currentWeek = getISOWeek(now)
        return year === currentYear && week === currentWeek
    }

    return (
        <div className="flex items-center justify-between bg-white rounded-lg shadow-sm p-4 mb-6">
            <button
                onClick={handlePrevWeek}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Oldingi hafta"
            >
                <ChevronLeft className="w-5 h-5 text-gray-600" />
            </button>

            <div className="flex items-center gap-4">
                <div className="text-center">
                    <div className="text-sm text-gray-500">Hafta</div>
                    <div className="text-lg font-semibold text-gray-900">
                        {getWeekDateRange(year, week)}
                    </div>
                </div>

                {!isCurrentWeek() && (
                    <button
                        onClick={goToCurrentWeek}
                        className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
                    >
                        Bugun
                    </button>
                )}
            </div>

            <button
                onClick={handleNextWeek}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Keyingi hafta"
            >
                <ChevronRight className="w-5 h-5 text-gray-600" />
            </button>
        </div>
    )
}
