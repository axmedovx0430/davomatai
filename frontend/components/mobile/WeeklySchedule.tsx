import { useState, useMemo } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, CalendarDays, MapPin, User as UserIcon } from "lucide-react";

interface Schedule {
    id: number;
    name: string;
    day_of_week: number;
    start_time: string;
    end_time: string;
    room?: string;
    teacher?: string;
}

interface Attendance {
    id: number;
    status: string;
    check_in_time: string;
    schedule_id?: number;
    date: string;
}

interface WeeklyScheduleProps {
    schedules: Schedule[];
    todayAttendance: Attendance[];
    t: (key: any) => string;
    lang: string;
}

export function WeeklySchedule({ schedules, todayAttendance, t, lang }: WeeklyScheduleProps) {
    const today = new Date().getDay(); // 0=Sunday, 1=Monday...
    const initialDay = today === 0 ? 6 : today - 1; // Convert to 0=Monday, 6=Sunday
    const [selectedDay, setSelectedDay] = useState(initialDay);

    const days = [
        { id: 0, label: t('mon') },
        { id: 1, label: t('tue') },
        { id: 2, label: t('wed') },
        { id: 3, label: t('thu') },
        { id: 4, label: t('fri') },
        { id: 5, label: t('sat') },
        { id: 6, label: t('sun') },
    ];

    const filteredSchedules = useMemo(() => {
        return schedules.filter(s => s.day_of_week === selectedDay);
    }, [schedules, selectedDay]);

    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between px-1">
                <h2 className="text-md font-semibold text-gray-900 flex items-center gap-2">
                    <CalendarDays className="h-4 w-4 text-blue-500" />
                    {t('weekly_schedule')}
                </h2>
            </div>

            {/* Day Selector */}
            <div className="flex justify-between bg-white p-1 rounded-xl border shadow-sm overflow-x-auto no-scrollbar">
                {days.map((day) => (
                    <button
                        key={day.id}
                        onClick={() => setSelectedDay(day.id)}
                        className={`flex-1 min-w-[40px] py-2 rounded-lg text-xs font-bold transition-all ${selectedDay === day.id
                                ? 'bg-blue-600 text-white shadow-md'
                                : 'text-gray-400 hover:bg-gray-50'
                            }`}
                    >
                        {day.label}
                    </button>
                ))}
            </div>

            {/* Schedule List */}
            <div className="space-y-3">
                {filteredSchedules.length > 0 ? (
                    filteredSchedules.map((item) => {
                        // Check if this schedule has attendance today
                        const isToday = selectedDay === initialDay;
                        const attendance = isToday ? todayAttendance.find(a => a.schedule_id === item.id) : null;

                        return (
                            <Card key={item.id} className="overflow-hidden border-l-4 border-l-blue-500 shadow-sm">
                                <CardContent className="p-4 flex justify-between items-center">
                                    <div className="space-y-1.5 flex-1">
                                        <h3 className="font-bold text-gray-900 text-md leading-tight">
                                            {item.name}
                                        </h3>
                                        <div className="flex flex-wrap gap-2">
                                            <span className="flex items-center gap-1 bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded text-[10px] font-medium">
                                                <Clock className="h-3 w-3" />
                                                {item.start_time.substring(0, 5)} - {item.end_time.substring(0, 5)}
                                            </span>
                                            {item.room && (
                                                <span className="flex items-center gap-1 bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded text-[10px] font-medium">
                                                    <MapPin className="h-3 w-3" />
                                                    {item.room}
                                                </span>
                                            )}
                                            {item.teacher && (
                                                <span className="flex items-center gap-1 bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded text-[10px] font-medium">
                                                    <UserIcon className="h-3 w-3" />
                                                    {item.teacher}
                                                </span>
                                            )}
                                        </div>
                                    </div>

                                    {attendance && (
                                        <div className="flex flex-col items-end gap-1.5 ml-2">
                                            <Badge
                                                variant={
                                                    attendance.status === 'present' ? 'default' :
                                                        attendance.status === 'late' ? 'secondary' : 'destructive'
                                                }
                                                className={`text-[10px] px-2 py-0 ${attendance.status === 'present' ? 'bg-green-500' :
                                                    attendance.status === 'late' ? 'bg-yellow-500' : 'bg-red-500'
                                                    }`}
                                            >
                                                {attendance.status === 'present' ? t('present') :
                                                    attendance.status === 'late' ? t('late') : t('absent')}
                                            </Badge>
                                            <span className="text-[10px] font-mono text-gray-400">
                                                {attendance.check_in_time.substring(0, 5)}
                                            </span>
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        );
                    })
                ) : (
                    <div className="bg-gray-50 border-dashed border-2 rounded-xl p-8 text-center text-gray-400">
                        <Clock className="h-8 w-8 mx-auto mb-2 opacity-20" />
                        <p className="text-sm">{t('no_data_today')}</p>
                    </div>
                )}
            </div>
        </div>
    );
}
