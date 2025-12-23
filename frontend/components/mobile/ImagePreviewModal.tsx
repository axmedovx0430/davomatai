import React, { useState, useRef, useEffect } from 'react';
import { X, ZoomIn, ZoomOut } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ImagePreviewModalProps {
    imageUrl: string;
    isOpen: boolean;
    onClose: () => void;
}

export function ImagePreviewModal({ imageUrl, isOpen, onClose }: ImagePreviewModalProps) {
    const [scale, setScale] = useState(1);
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    const imageRef = useRef<HTMLImageElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!isOpen) {
            setScale(1);
            setPosition({ x: 0, y: 0 });
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const handleZoomIn = () => {
        setScale(prev => Math.min(prev + 0.5, 4));
    };

    const handleZoomOut = () => {
        setScale(prev => Math.max(prev - 0.5, 1));
        if (scale <= 1.5) {
            setPosition({ x: 0, y: 0 });
        }
    };

    const handleDoubleClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (scale > 1) {
            setScale(1);
            setPosition({ x: 0, y: 0 });
        } else {
            setScale(2);
        }
    };

    const handleMouseDown = (e: React.MouseEvent) => {
        if (scale > 1) {
            setIsDragging(true);
            setDragStart({
                x: e.clientX - position.x,
                y: e.clientY - position.y
            });
        }
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        if (isDragging && scale > 1) {
            setPosition({
                x: e.clientX - dragStart.x,
                y: e.clientY - dragStart.y
            });
        }
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    const handleTouchStart = (e: React.TouchEvent) => {
        if (e.touches.length === 1 && scale > 1) {
            setIsDragging(true);
            setDragStart({
                x: e.touches[0].clientX - position.x,
                y: e.touches[0].clientY - position.y
            });
        }
    };

    const handleTouchMove = (e: React.TouchEvent) => {
        if (isDragging && e.touches.length === 1 && scale > 1) {
            setPosition({
                x: e.touches[0].clientX - dragStart.x,
                y: e.touches[0].clientY - dragStart.y
            });
        }
    };

    const handleTouchEnd = () => {
        setIsDragging(false);
    };

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm"
            onClick={onClose}
        >
            <div className="relative w-full h-full flex items-center justify-center p-4">
                {/* Close Button */}
                <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-4 right-4 z-20 rounded-full bg-white/90 hover:bg-white"
                    onClick={onClose}
                >
                    <X className="h-6 w-6 text-gray-900" />
                </Button>

                {/* Zoom Controls */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-20 flex gap-2 bg-white/90 rounded-full p-2">
                    <Button
                        variant="ghost"
                        size="icon"
                        className="rounded-full"
                        onClick={(e) => {
                            e.stopPropagation();
                            handleZoomOut();
                        }}
                        disabled={scale <= 1}
                    >
                        <ZoomOut className="h-5 w-5 text-gray-900" />
                    </Button>
                    <span className="px-3 py-2 text-sm font-medium text-gray-900">
                        {Math.round(scale * 100)}%
                    </span>
                    <Button
                        variant="ghost"
                        size="icon"
                        className="rounded-full"
                        onClick={(e) => {
                            e.stopPropagation();
                            handleZoomIn();
                        }}
                        disabled={scale >= 4}
                    >
                        <ZoomIn className="h-5 w-5 text-gray-900" />
                    </Button>
                </div>

                {/* Image Container */}
                <div
                    ref={containerRef}
                    className="relative overflow-hidden max-w-full max-h-full"
                    onClick={(e) => e.stopPropagation()}
                >
                    <img
                        ref={imageRef}
                        src={imageUrl}
                        alt="Attendance"
                        className="max-w-full max-h-[85vh] rounded-lg shadow-2xl object-contain select-none"
                        style={{
                            transform: `scale(${scale}) translate(${position.x / scale}px, ${position.y / scale}px)`,
                            transition: isDragging ? 'none' : 'transform 0.3s ease-out',
                            cursor: scale > 1 ? (isDragging ? 'grabbing' : 'grab') : 'pointer'
                        }}
                        onDoubleClick={handleDoubleClick}
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}
                        onTouchStart={handleTouchStart}
                        onTouchMove={handleTouchMove}
                        onTouchEnd={handleTouchEnd}
                        draggable={false}
                    />
                </div>

                {/* Hint Text */}
                {scale === 1 && (
                    <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 text-white/70 text-sm">
                        Rasmni kattalashtirish uchun ikki marta bosing
                    </div>
                )}
            </div>
        </div>
    );
}
