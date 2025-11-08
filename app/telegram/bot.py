import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from app.telegram.handlers import (
    start_handler,
    help_handler,
    programas_sociales_handler,
    button_handler,
    notificaciones_handler,
    ask_vehicle_name,
    save_vehicle_info,
    cancel_handler,
    message_handler,
    error_handler,
    ASK_PLATE,
    ASK_VEHICLE_NAME
)

load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")

        if not self.token:
            raise ValueError("No se encontró TELEGRAM_TOKEN en el archivo .env")

        # Crear aplicación de Telegram
        self.app = Application.builder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self):
        """Registrar todos los comandos y handlers del bot."""
        logger.info("Registrando handlers...")

        # Comandos básicos
        self.app.add_handler(CommandHandler("start", start_handler))
        self.app.add_handler(CommandHandler("ayuda", help_handler))
        logger.info("✓ Comandos básicos registrados")

        # Programas sociales con botones
        self.app.add_handler(CommandHandler("programas_sociales", programas_sociales_handler))
        self.app.add_handler(CallbackQueryHandler(button_handler))
        logger.info("✓ Programas sociales registrados")

        # Conversación de notificaciones
        self.app.add_handler(self._notification_conversation_handler())
        logger.info("✓ Conversación de notificaciones registrada")

        # Mensajes generales (debe ir al final)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        logger.info("✓ Handler de mensajes generales registrado")

        # Error handler (global)
        self.app.add_error_handler(error_handler)
        logger.info("✓ Error handler registrado")

        logger.info("Todos los handlers registrados correctamente")

    def _notification_conversation_handler(self):
        """Crear el handler de conversación para notificaciones."""
        return ConversationHandler(
            entry_points=[CommandHandler("notificaciones", notificaciones_handler)],
            states={
                ASK_PLATE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, ask_vehicle_name)
                ],
                ASK_VEHICLE_NAME: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, save_vehicle_info)
                ],
            },
            fallbacks=[
                CommandHandler("cancelar", cancel_handler),
                CommandHandler("ayuda", help_handler)
            ],
        )

    def run(self):
        """Inicializa y ejecuta el bot."""
        logger.info("🤖 Bot ciudadano ejecutándose...")
        print("🤖 Bot ciudadano ejecutándose... Presiona Ctrl + C para detenerlo.")

        # Ejecutar con manejo de errores
        try:
            self.app.run_polling(
                allowed_updates=[Update.MESSAGE, Update.CALLBACK_QUERY],
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"Error al ejecutar el bot: {e}", exc_info=True)