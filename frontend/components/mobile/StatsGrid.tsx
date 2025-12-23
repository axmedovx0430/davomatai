import { Card, CardContent } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

interface Stats {
    present: number;
    late: number;
    absent: number;
    total: number;
    attendance_rate: number;
}

interface StatsGridProps {
    stats: Stats | null;
    t: (key: any) => string;
}

export function StatsGrid({ stats, t }: StatsGridProps) {
    if (!stats) return null;

    const data = [
        { name: 'Present', value: stats.present, color: '#22c55e' },
        { name: 'Late', value: stats.late, color: '#eab308' },
        { name: 'Absent', value: stats.absent, color: '#ef4444' },
    ];

    return (
        <div className="space-y-4">
            {/* Attendance Rate Chart */}
            <Card className="overflow-hidden shadow-sm border">
                <CardContent className="p-4 flex items-center justify-between">
                    <div className="w-1/2 h-32">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={data}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={35}
                                    outerRadius={50}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="w-1/2 text-center">
                        <div className="text-3xl font-extrabold text-blue-600">{Math.round(stats.attendance_rate)}%</div>
                        <div className="text-[10px] font-medium text-gray-500 uppercase tracking-widest mt-1">{t('attendance_rate')}</div>
                    </div>
                </CardContent>
            </Card>

            {/* Stats Cards */}
            <div className="grid grid-cols-3 gap-3">
                <Card className="border-green-100 bg-green-50/50 shadow-sm">
                    <CardContent className="p-3 text-center">
                        <div className="text-2xl font-bold text-green-600">{stats.present}</div>
                        <div className="text-[10px] font-medium text-green-700 mt-1 uppercase tracking-wider">{t('present')}</div>
                    </CardContent>
                </Card>
                <Card className="border-yellow-100 bg-yellow-50/50 shadow-sm">
                    <CardContent className="p-3 text-center">
                        <div className="text-2xl font-bold text-yellow-600">{stats.late}</div>
                        <div className="text-[10px] font-medium text-yellow-700 mt-1 uppercase tracking-wider">{t('late')}</div>
                    </CardContent>
                </Card>
                <Card className="border-red-100 bg-red-50/50 shadow-sm">
                    <CardContent className="p-3 text-center">
                        <div className="text-2xl font-bold text-red-600">{stats.absent}</div>
                        <div className="text-[10px] font-medium text-red-700 mt-1 uppercase tracking-wider">{t('absent')}</div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
