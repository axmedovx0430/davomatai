/**
 * Schedule-related API hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Types
export interface Schedule {
    id: number
    name: string
    day_of_week: number
    start_time: string
    end_time: string
    group_id?: number
    is_active: boolean
    late_threshold_minutes?: number
    duplicate_check_minutes?: number
    effective_from?: string
    effective_to?: string
    teacher?: string
    room?: string
    created_at: string
    updated_at: string
}

export interface ScheduleStats {
    total_users: number
    present: number
    late: number
    absent: number
    attendance_rate: number
}

export interface WeekSchedules {
    [day: string]: Schedule[]
}

// Get week schedules (recurring weekly pattern)
export function useWeekSchedules(startDate?: string, endDate?: string) {
    return useQuery({
        queryKey: ['schedules', 'week', startDate, endDate],
        queryFn: async () => {
            let url = `${API_URL}/api/schedules/week`
            if (startDate && endDate) {
                url += `?start_date=${startDate}&end_date=${endDate}`
            }
            const response = await fetch(url)
            if (!response.ok) throw new Error('Failed to fetch week schedules')
            const data = await response.json()
            return data.schedules as WeekSchedules
        }
    })
}

// Get schedule stats
export function useScheduleStats(scheduleId: number | null, date: string) {
    return useQuery({
        queryKey: ['schedules', scheduleId, 'stats', date],
        queryFn: async () => {
            if (!scheduleId) return null
            const response = await fetch(`${API_URL}/api/schedules/${scheduleId}/stats?date=${date}`)
            if (!response.ok) throw new Error('Failed to fetch schedule stats')
            const data = await response.json()
            return data.stats as ScheduleStats
        },
        enabled: !!scheduleId,
        refetchInterval: 30000, // Refetch every 30 seconds
    })
}

// Get schedule attendance
export function useScheduleAttendance(scheduleId: number | null, date: string) {
    return useQuery({
        queryKey: ['schedules', scheduleId, 'attendance', date],
        queryFn: async () => {
            if (!scheduleId) return []
            const response = await fetch(`${API_URL}/api/schedules/${scheduleId}/attendance?date=${date}`)
            if (!response.ok) throw new Error('Failed to fetch schedule attendance')
            const data = await response.json()
            return data.attendance
        },
        enabled: !!scheduleId,
        refetchInterval: 10000, // Refetch every 10 seconds
    })
}

// Create schedule
export function useCreateSchedule() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (scheduleData: {
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
        }) => {
            const response = await fetch(`${API_URL}/api/schedules`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scheduleData)
            })
            if (!response.ok) throw new Error('Failed to create schedule')
            return response.json()
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['schedules'] })
        }
    })
}

// Update schedule
export function useUpdateSchedule() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async ({ id, ...scheduleData }: {
            id: number
            name?: string
            day_of_week?: number
            start_time?: string
            end_time?: string
            group_id?: number
            is_active?: boolean
            late_threshold_minutes?: number
            duplicate_check_minutes?: number
            effective_from?: string
            effective_to?: string
            teacher?: string
            room?: string
        }) => {
            const response = await fetch(`${API_URL}/api/schedules/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scheduleData)
            })
            if (!response.ok) throw new Error('Failed to update schedule')
            return response.json()
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['schedules'] })
        }
    })
}

// Delete schedule
export function useDeleteSchedule() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (id: number) => {
            const response = await fetch(`${API_URL}/api/schedules/${id}`, {
                method: 'DELETE'
            })
            if (!response.ok) throw new Error('Failed to delete schedule')
            return response.json()
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['schedules'] })
        }
    })
}
