'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api-client'

export function useAttendance(params?: any) {
    return useQuery({
        queryKey: ['attendance', params],
        queryFn: async () => {
            const response = await api.getAttendance(params)
            return response.data
        },
    })
}

export function useTodayAttendance() {
    return useQuery({
        queryKey: ['attendance', 'today'],
        queryFn: async () => {
            const response = await api.getTodayAttendance()
            return response.data
        },
        refetchInterval: 30000, // Refetch every 30 seconds
    })
}

export function useAttendanceStats() {
    return useQuery({
        queryKey: ['attendance', 'stats'],
        queryFn: async () => {
            const response = await api.getAttendanceStats()
            return response.data
        },
        refetchInterval: 60000, // Refetch every minute
    })
}

export function useUsers(params?: any) {
    return useQuery({
        queryKey: ['users', params],
        queryFn: async () => {
            const response = await api.getUsers(params)
            return response.data
        },
    })
}

export function useCreateUser() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (data: any) => api.createUser(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] })
        },
    })
}

export function useUpdateUser() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) => api.updateUser(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] })
        },
    })
}

export function useDeleteUser() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (id: number) => api.deleteUser(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] })
        },
    })
}

export function useRegisterFace() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: ({ userId, file }: { userId: number; file: File }) =>
            api.registerFace(userId, file),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] })
        },
    })
}

export function useDevices() {
    return useQuery({
        queryKey: ['devices'],
        queryFn: async () => {
            const response = await api.getDevices()
            return response.data
        },
    })
}

export function useTimeSettings() {
    return useQuery({
        queryKey: ['time-settings'],
        queryFn: async () => {
            const response = await api.getTimeSettings()
            return response.data
        },
    })
}

export function useUpdateTimeSettings() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (data: any) => api.updateTimeSettings(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['time-settings'] })
        },
    })
}
