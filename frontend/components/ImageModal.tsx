'use client'

import { useState } from 'react'
import { X } from 'lucide-react'

interface ImageModalProps {
    imageUrl: string | null
    onClose: () => void
    userName?: string
    confidence?: number
}

export default function ImageModal({ imageUrl, onClose, userName, confidence }: ImageModalProps) {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    if (!imageUrl) return null

    return (
        <div
            className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
            onClick={onClose}
        >
            <div
                className="relative bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-hidden"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b">
                    <div>
                        <h3 className="text-lg font-bold text-gray-900">
                            {userName || 'Davomat Rasmi'}
                        </h3>
                        {confidence && (
                            <p className="text-sm text-gray-600">
                                Ishonch darajasi: {(confidence * 100).toFixed(1)}%
                            </p>
                        )}
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-100"
                    >
                        <X className="w-6 h-6" />
                    </button>
                </div>

                {/* Image */}
                <div className="p-4 flex items-center justify-center bg-gray-50">
                    {loading && !error && (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                            <p className="mt-4 text-gray-600">Yuklanmoqda...</p>
                        </div>
                    )}

                    {error && (
                        <div className="text-center py-12">
                            <p className="text-red-600">Rasmni yuklab bo'lmadi</p>
                            <p className="text-sm text-gray-500 mt-2">Rasm topilmadi yoki o'chirilgan</p>
                        </div>
                    )}

                    <img
                        src={imageUrl}
                        alt={userName || 'Attendance image'}
                        className={`max-w-full max-h-[70vh] object-contain rounded ${loading ? 'hidden' : 'block'}`}
                        onLoad={() => setLoading(false)}
                        onError={() => {
                            setLoading(false)
                            setError(true)
                        }}
                    />
                </div>

                {/* Footer */}
                <div className="p-4 border-t bg-gray-50">
                    <button
                        onClick={onClose}
                        className="btn btn-secondary w-full"
                    >
                        Yopish
                    </button>
                </div>
            </div>
        </div>
    )
}
