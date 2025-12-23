'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const router = useRouter()

    useEffect(() => {
        const token = localStorage.getItem('access_token')

        if (!token) {
            router.push('/login')
            return
        }

        // Verify token is still valid
        const verifyToken = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/verify`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })

                if (!response.ok) {
                    // Token invalid, redirect to login
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('user')
                    router.push('/login')
                }
            } catch (error) {
                console.error('Token verification failed:', error)
                router.push('/login')
            }
        }

        verifyToken()
    }, [router])

    return <>{children}</>
}
