"""Common handlers for bot commands."""
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.models.user import User
from bot.models.settings import SettingsRepository
from bot.utils.texts import get_text
from bot.keyboards.inline import get_main_menu, get_language_menu, get_info_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user: User, state: FSMContext):
    """Handle /start command."""
    await state.clear()

    text = get_text(user.language, "main_menu")
    keyboard = get_main_menu(user.language)

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery, user: User, state: FSMContext):
    """Show main menu."""
    await state.clear()

    text = get_text(user.language, "main_menu")
    keyboard = get_main_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "language")
async def show_language_menu(callback: CallbackQuery, user: User):
    """Show language selection menu."""
    text = get_text(user.language, "select_language")
    keyboard = get_language_menu()

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("set_language:"))
async def set_language(callback: CallbackQuery, user: User, user_repo):
    """Set user language."""
    language = callback.data.split(":")[1]

    # Update user language
    await user_repo.update_language(user.telegram_id, language)
    user.language = language

    text = get_text(language, "language_changed")
    await callback.answer(text, show_alert=True)

    # Show main menu
    menu_text = get_text(language, "main_menu")
    keyboard = get_main_menu(language)
    await callback.message.edit_text(menu_text, reply_markup=keyboard)


@router.callback_query(F.data == "info")
async def show_info(callback: CallbackQuery, user: User, settings_repo: SettingsRepository):
    """Show info menu."""
    settings = await settings_repo.get_all_settings()

    text = get_text(user.language, "info_message")
    keyboard = get_info_menu(user.language, settings)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
