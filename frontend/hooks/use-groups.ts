import { useQuery } from '@tanstack/react-query'
import apiClient from '@/lib/api-client'

export interface Group {
    id: number
    name: string
    code: string
    description?: string
    faculty?: string
    course?: number
    semester?: number
    academic_year?: string
    is_active: boolean
    student_count: number
    created_at: string
    updated_at: string
}

export function useGroups() {
    return useQuery({
        queryKey: ['groups'],
        queryFn: async () => {
            const response = await apiClient.get('/api/groups')
            return response.data.groups as Group[]
        }
    })
}
