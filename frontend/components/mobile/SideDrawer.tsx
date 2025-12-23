import React, { useEffect, useState } from 'react';
import { User as UserIcon, GraduationCap, BookOpen, Building2, Phone, Mail, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface User {
    id: number;
    full_name: string;
    employee_id: string;
    phone?: string;
    email?: string;
    course?: number;
    major?: string;
    faculty?: string;
    groups?: { id: number; name: string; code: string }[];
}

interface SideDrawerProps {
    user: User | null;
    isOpen: boolean;
    onClose: () => void;
    t: (key: any) => string;
}

export function SideDrawer({ user, isOpen, onClose, t }: SideDrawerProps) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (isOpen) {
            setIsVisible(true);
            document.body.style.overflow = 'hidden';
        } else {
            const timer = setTimeout(() => setIsVisible(false), 300); // Match transition duration
            document.body.style.overflow = 'unset';
            return () => clearTimeout(timer);
        }
    }, [isOpen]);

    if (!isVisible && !isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex justify-start">
            {/* Backdrop */}
            <div
                className={`fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity duration-300 ${isOpen ? 'opacity-100' : 'opacity-0'}`}
                onClick={onClose}
            />

            {/* Drawer */}
            <div
                className={`relative w-[70%] max-w-sm bg-white h-full shadow-2xl transition-transform duration-300 ease-in-out transform ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}
            >
                {/* Close Button */}
                <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-4 right-4 z-10 rounded-full hover:bg-gray-100"
                    onClick={onClose}
                >
                    <X className="h-6 w-6 text-gray-500" />
                </Button>

                <div className="h-full overflow-y-auto p-6">
                    {user && (
                        <div className="space-y-8 mt-8">
                            {/* Header */}
                            <div className="flex flex-col items-center space-y-4">
                                <div className="h-28 w-28 rounded-3xl bg-blue-600 flex items-center justify-center text-white shadow-xl rotate-3 hover:rotate-0 transition-transform duration-300">
                                    <UserIcon className="h-14 w-14" />
                                </div>
                                <div className="text-center">
                                    <h2 className="text-2xl font-black text-gray-900 tracking-tight">
                                        {user.full_name}
                                    </h2>
                                    <Badge variant="secondary" className="mt-2 bg-blue-50 text-blue-600 border-blue-100 font-mono text-sm px-3 py-1">
                                        {user.employee_id}
                                    </Badge>
                                </div>
                            </div>

                            {/* Academic Info */}
                            <div className="space-y-4">
                                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">{t('academic_info') || 'Academic Info'}</h3>
                                <div className="grid grid-cols-1 gap-3">
                                    <InfoCard
                                        icon={<GraduationCap className="h-5 w-5 text-blue-500" />}
                                        label={t('course')}
                                        value={user.course ? `${user.course}-${t('course').toLowerCase()}` : "N/A"}
                                    />
                                    <InfoCard
                                        icon={<BookOpen className="h-5 w-5 text-purple-500" />}
                                        label={t('major')}
                                        value={user.major || "N/A"}
                                    />
                                    <InfoCard
                                        icon={<Building2 className="h-5 w-5 text-orange-500" />}
                                        label={t('faculty')}
                                        value={user.faculty || "N/A"}
                                    />
                                </div>
                            </div>

                            {/* Contact Info */}
                            <div className="space-y-4">
                                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">{t('contact_info') || 'Contact Info'}</h3>
                                <div className="space-y-3">
                                    {user.phone ? (
                                        <div className="flex items-center gap-4 p-4 rounded-2xl bg-gray-50 border border-gray-100">
                                            <div className="h-10 w-10 rounded-xl bg-white flex items-center justify-center shadow-sm">
                                                <Phone className="h-5 w-5 text-green-500" />
                                            </div>
                                            <span className="text-sm font-bold text-gray-700">{user.phone}</span>
                                        </div>
                                    ) : (
                                        <div className="text-sm text-gray-400 italic pl-2">No phone number</div>
                                    )}

                                    {user.email ? (
                                        <div className="flex items-center gap-4 p-4 rounded-2xl bg-gray-50 border border-gray-100">
                                            <div className="h-10 w-10 rounded-xl bg-white flex items-center justify-center shadow-sm">
                                                <Mail className="h-5 w-5 text-red-500" />
                                            </div>
                                            <span className="text-sm font-bold text-gray-700">{user.email}</span>
                                        </div>
                                    ) : (
                                        <div className="text-sm text-gray-400 italic pl-2">No email address</div>
                                    )}
                                </div>
                            </div>

                            {/* Groups */}
                            {user.groups && user.groups.length > 0 && (
                                <div className="space-y-4">
                                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">{t('groups') || 'Groups'}</h3>
                                    <div className="flex flex-wrap gap-2">
                                        {user.groups.map(group => (
                                            <Badge key={group.id} variant="outline" className="px-4 py-2 rounded-xl border-gray-200 text-gray-600 bg-white shadow-sm">
                                                {group.name} <span className="text-gray-400 ml-1">({group.code})</span>
                                            </Badge>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

function InfoCard({ icon, label, value }: { icon: React.ReactNode, label: string, value: string }) {
    return (
        <div className="flex items-center gap-4 p-4 rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="h-10 w-10 rounded-xl bg-gray-50 flex items-center justify-center">
                {icon}
            </div>
            <div>
                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{label}</p>
                <p className="text-sm font-bold text-gray-900">{value}</p>
            </div>
        </div>
    );
}
