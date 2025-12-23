import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock } from "lucide-react";
import { useState } from "react";
import { ImagePreviewModal } from "./ImagePreviewModal";

interface Schedule {
    id: number;
    name: string;
    start_time: string;
    end_time: string;
    room?: string;
}

interface Attendance {
    id: number;
    status: string;
    check_in_time: string;
    schedule?: Schedule;
    date: string;
    image_path?: string;
}

interface AttendanceCardProps {
    item: Attendance;
    t: (key: any) => string;
}

export function AttendanceCard({ item, t }: AttendanceCardProps) {
    const [isImagePreviewOpen, setIsImagePreviewOpen] = useState(false);
    const imageUrl = item.image_path ? `${process.env.NEXT_PUBLIC_API_URL || ''}/${item.image_path}` : null;

    return (
        <>
            <Card className="overflow-hidden border-l-4 border-l-blue-500 shadow-sm hover:shadow-md transition-shadow">
                <CardContent className="p-4 flex justify-between items-center gap-3">
                    {/* Image Thumbnail */}
                    {imageUrl && (
                        <div
                            className="flex-shrink-0 w-12 h-12 rounded-lg overflow-hidden cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                            onClick={() => setIsImagePreviewOpen(true)}
                        >
                            <img
                                src={imageUrl}
                                alt="Attendance"
                                className="w-full h-full object-cover"
                            />
                        </div>
                    )}

                    <div className="flex-1 space-y-1">
                        <h3 className="font-bold text-gray-900 text-md leading-tight">
                            {item.schedule?.name || t('unknown_lesson')}
                        </h3>
                        <div className="flex items-center text-[10px] text-gray-500 space-x-2">
                            <span className="flex items-center gap-1 bg-gray-100 px-1.5 py-0.5 rounded">
                                <Clock className="h-3 w-3" />
                                {item.schedule?.start_time} - {item.schedule?.end_time}
                            </span>
                            {item.schedule?.room && (
                                <span className="text-gray-400">{t('room')}: {item.schedule.room}</span>
                            )}
                        </div>
                    </div>
                    <div className="flex flex-col items-end gap-1.5">
                        <Badge
                            variant={
                                item.status === 'present' ? 'default' :
                                    item.status === 'late' ? 'secondary' : 'destructive'
                            }
                            className={`text-[10px] px-2 py-0 ${item.status === 'present' ? 'bg-green-500' :
                                item.status === 'late' ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                        >
                            {item.status === 'present' ? t('present') :
                                item.status === 'late' ? t('late') : t('absent')}
                        </Badge>
                        <span className="text-[10px] font-mono text-gray-400">
                            {item.check_in_time.substring(0, 5)}
                        </span>
                    </div>
                </CardContent>
            </Card>

            {imageUrl && (
                <ImagePreviewModal
                    imageUrl={imageUrl}
                    isOpen={isImagePreviewOpen}
                    onClose={() => setIsImagePreviewOpen(false)}
                />
            )}
        </>
    );
}
