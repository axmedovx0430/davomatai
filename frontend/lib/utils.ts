export const cn = (...classes: (string | undefined | null | false)[]) => {
    return classes.filter(Boolean).join(' ')
}

export const formatDate = (date: string | Date) => {
    return new Date(date).toLocaleDateString('uz-UZ', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    })
}

export const formatTime = (date: string | Date) => {
    return new Date(date).toLocaleTimeString('uz-UZ', {
        hour: '2-digit',
        minute: '2-digit',
    })
}

export const formatDateTime = (date: string | Date) => {
    return new Date(date).toLocaleString('uz-UZ', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    })
}

export const getStatusColor = (status: string) => {
    switch (status) {
        case 'present':
            return 'bg-green-100 text-green-800'
        case 'late':
            return 'bg-yellow-100 text-yellow-800'
        case 'absent':
            return 'bg-red-100 text-red-800'
        default:
            return 'bg-gray-100 text-gray-800'
    }
}

export const getStatusText = (status: string) => {
    switch (status) {
        case 'present':
            return 'Keldi'
        case 'late':
            return 'Kechikdi'
        case 'absent':
            return 'Kelmadi'
        default:
            return status
    }
}
