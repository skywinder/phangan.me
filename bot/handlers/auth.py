import base64
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from bot.cache import flush_users_cache, cached_telegram_users
from users.models.user import User


def command_auth(update: Update, context: CallbackContext) -> None:
    if not update.message or not update.message.text or " " not in update.message.text:
        update.effective_chat.send_message(
            "☝️ Нужно прислать мне секретный код. "
            "Напиши /auth и код из <a href=\"https://phangan.me/user/me/edit/bot/\">профиля в Клубе</a> "
            "через пробел. Только не публикуй его в публичных чатах!",
            parse_mode=ParseMode.HTML
        )
        return None

    secret_code = update.message.text.split(" ", 1)[1].strip()
    secret_code = base64.urlsafe_b64decode(secret_code).decode('utf-8')
    user = User.objects.filter(secret_hash=secret_code).first()

    if not user:
        update.effective_chat.send_message("Пользователь с таким кодом не найден")
        return None

    user.telegram_id = update.effective_user.id
    user.telegram_data = {
        "id": update.effective_user.id,
        "username": update.effective_user.username,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name,
        "language_code": update.effective_user.language_code,
    }
    user.save()

    update.effective_chat.send_message(f"Приятно познакомиться, {user.slug}! Добро пожаловать в Панган🏝Клуб!")
    update.message.delete()

    # Refresh the cache by deleting and requesting it again
    flush_users_cache()
    cached_telegram_users()

    return None
