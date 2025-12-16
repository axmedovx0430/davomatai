'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api-client'
import { User, LogIn } from 'lucide-react'

export default function LoginPage() {
    const [employeeId, setEmployeeId] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const router = useRouter()

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            // Verify user exists
            const response = await api.getUserByEmployeeId(employeeId)

            if (response.data.user) {
                // Save to localStorage
                localStorage.setItem('employeeId', employeeId)

                // Redirect to home
                router.push('/')
            }
        } catch (err: any) {
            console.error('Login error:', err)
            setError(err.response?.data?.detail || 'Foydalanuvchi topilmadi')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                        <User className="text-blue-600" size={32} />
                    </div>
                    <h1 className="text-2xl font-bold text-gray-900">Davomat Tizimi</h1>
                    <p className="text-gray-600 mt-2">Xodim ID raqamingizni kiriting</p>
                </div>

                {/* Login Form */}
                <form onSubmit={handleLogin} className="space-y-6">
                    <div>
                        <label htmlFor="employeeId" className="block text-sm font-medium text-gray-700 mb-2">
                            Xodim ID
                        </label>
                        <input
                            id="employeeId"
                            type="text"
                            value={employeeId}
                            onChange={(e) => setEmployeeId(e.target.value)}
                            placeholder="Masalan: ADMIN001"
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            required
                            disabled={loading}
                        />
                    </div>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading || !employeeId}
                        className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                                Yuklanmoqda...
                            </>
                        ) : (
                            <>
                                <LogIn size={20} />
                                Kirish
                            </>
                        )}
                    </button>
                </form>

                {/* Help Text */}
                <div className="mt-6 text-center text-sm text-gray-500">
                    <p>Xodim ID raqamingizni bilmaysizmi?</p>
                    <p className="mt-1">Administrator bilan bog'laning</p>
                </div>
            </div>
        </div>
    )
}
