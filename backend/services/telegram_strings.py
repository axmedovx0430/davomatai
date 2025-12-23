"""
Localization strings for the Telegram bot
"""

STRINGS = {
    "uz": {
        "welcome_registered": "👋 Xush kelibsiz, <b>{name}</b>!\n\nSiz allaqachon ro'yxatdan o'tgansiz.",
        "welcome_new": "👋 <b>Xush kelibsiz!</b>\n\nESP32-CAM davomat tizimi botiga xush kelibsiz.\n\nRo'yxatdan o'tish uchun <b>Employee ID</b> ingizni yuboring.\nMasalan: <code>EMP001</code>",
        "commands_list": "\n\n<b>Mavjud buyruqlar:</b>\n/mystats - Mening statistikam\n/today - Bugungi davomatim\n/week - Haftalik hisobot\n/profile - Profilim\n/schedule - Bugungi jadval\n/notify - Xabarlar sozlamasi\n/language - Tilni o'zgartirish\n/help - Yordam",
        "open_app": "📱 Ilovani ochish",
        "reg_success": "✅ <b>Muvaffaqiyatli ro'yxatdan o'tdingiz!</b>\n\n👤 Ism: <b>{name}</b>\n🆔 ID: <code>{id}</code>",
        "user_not_found": "❌ <b>Foydalanuvchi topilmadi!</b>\n\nEmployee ID: <code>{id}</code> tizimda mavjud emas.\n\nIltimos, to'g'ri ID ni kiriting yoki admin bilan bog'laning.",
        "error_occurred": "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "unknown_cmd": "Tushunarsiz buyruq. Iltimos, /help buyrug'idan foydalaning.",
        "not_registered": "❌ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini bosing.",
        "stats_title": "📊 <b>Sizning statistikangiz</b>\n\n📅 <b>{month}</b>\n✅ Kelgan: {present}\n⏰ Kechikkan: {late}\n📈 Davomat: {rate:.1f}%\n\n<b>Umumiy ({year}-yil):</b>\n📊 Jami: {total} ta davomat",
        "today_title": "📅 <b>Bugungi davomat ({date})</b>\n\n",
        "no_attendance_today": "📅 <b>Bugungi davomat ({date})</b>\n\nHali davomat yo'q.",
        "profile_title": "👤 <b>Profil</b>\n\n<b>Ism:</b> {name}\n🆔 <b>ID:</b> <code>{id}</code>\n📱 <b>Telefon:</b> {phone}\n📧 <b>Email:</b> {email}\n👥 <b>Guruh:</b> {groups}\n\n📊 <b>Umumiy statistika:</b>\nDavomat: {rate:.0f}%\nJami: {total}\n✅ Kelgan: {present}\n⏰ Kechikkan: {late}",
        "notify_on": "🔔 <b>Xabarlar yoqildi</b>\n\nEndi davomat xabarlari olasiz.",
        "notify_off": "🔕 <b>Xabarlar o'chirildi</b>\n\nDavomat xabarlari kelmaydi.",
        "lang_select": "🌐 <b>Tilni tanlang / Выберите язык / Select language</b>",
        "lang_updated": "✅ Til muvaffaqiyatli o'zgartirildi!",
        "help_text": "ℹ️ <b>Yordam</b>\n\n<b>Mavjud buyruqlar:</b>\n\n/start - Ro'yxatdan o'tish\n/mystats - Mening statistikam\n/today - Bugungi davomatim\n/week - Haftalik hisobot\n/profile - Profilim\n/schedule - Bugungi jadval\n/notify - Xabarlarni yoqish/o'chirish\n/language - Tilni tanlash\n/help - Bu yordam xabari\n\nSavollar uchun admin bilan bog'laning."
    },
    "ru": {
        "welcome_registered": "👋 Добро пожаловать, <b>{name}</b>!\n\nВы уже зарегистрированы.",
        "welcome_new": "👋 <b>Добро пожаловать!</b>\n\nДобро пожаловать в бот системы посещаемости ESP32-CAM.\n\nДля регистрации отправьте свой <b>Employee ID</b>.\nНапример: <code>EMP001</code>",
        "commands_list": "\n\n<b>Доступные команды:</b>\n/mystats - Моя статистика\n/today - Моя посещаемость сегодня\n/week - Еженедельный отчет\n/profile - Мой профиль\n/schedule - Расписание на сегодня\n/notify - Настройка уведомлений\n/language - Сменить язык\n/help - Помощь",
        "open_app": "📱 Открыть приложение",
        "reg_success": "✅ <b>Вы успешно зарегистрированы!</b>\n\n👤 Имя: <b>{name}</b>\n🆔 ID: <code>{id}</code>",
        "user_not_found": "❌ <b>Пользователь не найден!</b>\n\nEmployee ID: <code>{id}</code> не существует в системе.\n\nПожалуйста, введите правильный ID или свяжитесь с админом.",
        "error_occurred": "❌ Произошла ошибка. Пожалуйста, попробуйте еще раз.",
        "unknown_cmd": "Непонятная команда. Пожалуйста, используйте /help.",
        "not_registered": "❌ Вы не зарегистрированы. Нажмите /start.",
        "stats_title": "📊 <b>Ваша статистика</b>\n\n📅 <b>{month}</b>\n✅ Пришел: {present}\n⏰ Опоздал: {late}\n📈 Посещаемость: {rate:.1f}%\n\n<b>Общая ({year} год):</b>\n📊 Всего: {total} посещений",
        "today_title": "📅 <b>Посещаемость сегодня ({date})</b>\n\n",
        "no_attendance_today": "📅 <b>Посещаемость сегодня ({date})</b>\n\nПосещений пока нет.",
        "profile_title": "👤 <b>Профиль</b>\n\n<b>Имя:</b> {name}\n🆔 <b>ID:</b> <code>{id}</code>\n📱 <b>Телефон:</b> {phone}\n📧 <b>Email:</b> {email}\n👥 <b>Группа:</b> {groups}\n\n📊 <b>Общая статистика:</b>\nПосещаемость: {rate:.0f}%\nВсего: {total}\n✅ Пришел: {present}\n⏰ Опоздал: {late}",
        "notify_on": "🔔 <b>Уведомления включены</b>\n\nТеперь вы будете получать сообщения о посещаемости.",
        "notify_off": "🔕 <b>Уведомления выключены</b>\n\nСообщения о посещаемости приходить не будут.",
        "lang_select": "🌐 <b>Выберите язык / Tanlang tilni / Select language</b>",
        "lang_updated": "✅ Язык успешно изменен!",
        "help_text": "ℹ️ <b>Помощь</b>\n\n<b>Доступные команды:</b>\n\n/start - Регистрация\n/mystats - Моя статистика\n/today - Посещаемость сегодня\n/week - Еженедельный отчет\n/profile - Профиль\n/schedule - Расписание\n/notify - Вкл/выкл уведомления\n/language - Выбор языка\n/help - Это сообщение помощи\n\nПо вопросам обращайтесь к админу."
    },
    "en": {
        "welcome_registered": "👋 Welcome, <b>{name}</b>!\n\nYou are already registered.",
        "welcome_new": "👋 <b>Welcome!</b>\n\nWelcome to the ESP32-CAM attendance system bot.\n\nTo register, please send your <b>Employee ID</b>.\nExample: <code>EMP001</code>",
        "commands_list": "\n\n<b>Available commands:</b>\n/mystats - My statistics\n/today - Today's attendance\n/week - Weekly report\n/profile - My profile\n/schedule - Today's schedule\n/notify - Notification settings\n/language - Change language\n/help - Help",
        "open_app": "📱 Open App",
        "reg_success": "✅ <b>Successfully registered!</b>\n\n👤 Name: <b>{name}</b>\n🆔 ID: <code>{id}</code>",
        "user_not_found": "❌ <b>User not found!</b>\n\nEmployee ID: <code>{id}</code> does not exist in the system.\n\nPlease enter the correct ID or contact the admin.",
        "error_occurred": "❌ An error occurred. Please try again.",
        "unknown_cmd": "Unknown command. Please use /help.",
        "not_registered": "❌ You are not registered. Please press /start.",
        "stats_title": "📊 <b>Your Statistics</b>\n\n📅 <b>{month}</b>\n✅ Present: {present}\n⏰ Late: {late}\n📈 Rate: {rate:.1f}%\n\n<b>Total ({year}):</b>\n📊 Total: {total} attendances",
        "today_title": "📅 <b>Today's Attendance ({date})</b>\n\n",
        "no_attendance_today": "📅 <b>Today's Attendance ({date})</b>\n\nNo attendance records yet.",
        "profile_title": "👤 <b>Profile</b>\n\n<b>Name:</b> {name}\n🆔 <b>ID:</b> <code>{id}</code>\n📱 <b>Phone:</b> {phone}\n📧 <b>Email:</b> {email}\n👥 <b>Group:</b> {groups}\n\n📊 <b>Overall Statistics:</b>\nRate: {rate:.0f}%\nTotal: {total}\n✅ Present: {present}\n⏰ Late: {late}",
        "notify_on": "🔔 <b>Notifications enabled</b>\n\nYou will now receive attendance messages.",
        "notify_off": "🔕 <b>Notifications disabled</b>\n\nYou will no longer receive attendance messages.",
        "lang_select": "🌐 <b>Select language / Tanlang tilni / Выберите язык</b>",
        "lang_updated": "✅ Language successfully updated!",
        "help_text": "ℹ️ <b>Help</b>\n\n<b>Available commands:</b>\n\n/start - Registration\n/mystats - My statistics\n/today - Today's attendance\n/week - Weekly report\n/profile - Profile\n/schedule - Schedule\n/notify - Toggle notifications\n/language - Select language\n/help - This help message\n\nFor questions, contact the admin."
    }
}
