# app/telegram/handlers.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

# Configurar logger
logger = logging.getLogger(__name__)

# Estados para /notificaciones
ASK_PLATE, ASK_VEHICLE_NAME = range(2)


# ========== COMANDOS BÁSICOS ==========

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para el comando /start"""
    logger.info(f"Comando /start recibido de {update.effective_user.id}")
    user = update.effective_user
    await update.message.reply_text(
        f"👋 ¡Hola {user.first_name}! Soy tu asistente ciudadano 24/7.\n\n"
        "Puedo ayudarte con:\n"
        "• Guía de trámites\n"
        "• PQRSD (Peticiones, Quejas, Reclamos, Sugerencias, Denuncias)\n"
        "• Programas sociales y subsidios\n"
        "• Notificaciones de pico y placa, eventos y cierres viales\n\n"
        "📋 Comandos disponibles:\n"
        "/programas_sociales - Ver programas disponibles\n"
        "/notificaciones - Configurar alertas de movilidad\n"
        "/ayuda - Ver esta ayuda\n\n"
        "¡También puedes escribirme en lenguaje natural! 🚀"
    )
    logger.info("Respuesta enviada correctamente")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para el comando /ayuda"""
    logger.info(f"Comando /ayuda recibido de {update.effective_user.id}")
    await update.message.reply_text(
        "ℹ️ <b>Comandos disponibles:</b>\n\n"
        "/programas_sociales → Ver programas como Medellín Te Quiere, Buen Comienzo 365, etc.\n"
        "/notificaciones → Configurar alertas de pico y placa, eventos, cierres viales\n"
        "/cancelar → Cancelar operación actual\n\n"
        "💬 <b>Uso natural:</b>\n"
        "También puedes escribirme directamente:\n"
        "• 'Quiero saber sobre subsidios'\n"
        "• '¿Cómo hago un trámite?'\n"
        "• 'Necesito presentar una queja'",
        parse_mode='HTML'
    )
    logger.info("Respuesta enviada correctamente")


# ========== PROGRAMAS SOCIALES ==========

async def programas_sociales_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los programas sociales disponibles con botones"""
    keyboard = [
        [InlineKeyboardButton("💙 Medellín Te Quiere", callback_data="prog_medellin_te_quiere")],
        [InlineKeyboardButton("👶 Buen Comienzo 365", callback_data="prog_buen_comienzo")],
        [InlineKeyboardButton("🎓 Oportunidades para Crecer", callback_data="prog_oportunidades")],
        [InlineKeyboardButton("🏠 Subsidios de Vivienda", callback_data="prog_subsidios")],
        [InlineKeyboardButton("🍲 Alimentación Escolar", callback_data="prog_alimentacion")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📋 <b>Programas Sociales Disponibles</b>\n\n"
        "Selecciona el programa que deseas consultar:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para los botones inline (callback queries)"""
    query = update.callback_query
    await query.answer()  # Responder al callback para quitar el reloj de carga

    # Diccionario con información de programas
    programas_info = {
        "prog_medellin_te_quiere": {
            "titulo": "💙 Medellín Te Quiere",
            "descripcion": (
                "Programa de apoyo económico para familias vulnerables.\n\n"
                "<b>📌 Requisitos:</b>\n"
                "• Estar en nivel SISBEN I o II\n"
                "• Residir en Medellín\n"
                "• Tener hijos menores de edad\n\n"
                "<b>💰 Beneficio:</b> Hasta $150.000 mensuales\n\n"
                "<b>📞 Contacto:</b> 123-456-7890\n"
                "<b>🌐 Web:</b> www.medellin.gov.co/medellin-te-quiere"
            )
        },
        "prog_buen_comienzo": {
            "titulo": "👶 Buen Comienzo 365",
            "descripcion": (
                "Atención integral a la primera infancia.\n\n"
                "<b>📌 Beneficiarios:</b>\n"
                "• Niños de 0 a 5 años\n"
                "• Familias de estratos 1, 2 y 3\n\n"
                "<b>🎁 Incluye:</b>\n"
                "• Nutrición\n"
                "• Educación inicial\n"
                "• Valoraciones médicas\n\n"
                "<b>📞 Contacto:</b> 123-456-7891\n"
                "<b>🌐 Web:</b> www.medellin.gov.co/buen-comienzo"
            )
        },
        "prog_oportunidades": {
            "titulo": "🎓 Oportunidades para Crecer",
            "descripcion": (
                "Becas y apoyo educativo para jóvenes.\n\n"
                "<b>📌 Para quién:</b>\n"
                "• Estudiantes de secundaria y universidad\n"
                "• Estratos 1, 2 y 3\n\n"
                "<b>💰 Beneficios:</b>\n"
                "• Becas parciales o completas\n"
                "• Apoyo para útiles escolares\n\n"
                "<b>📞 Contacto:</b> 123-456-7892"
            )
        },
        "prog_subsidios": {
            "titulo": "🏠 Subsidios de Vivienda",
            "descripcion": (
                "Apoyo para compra de vivienda nueva o usada.\n\n"
                "<b>📌 Requisitos:</b>\n"
                "• No tener vivienda propia\n"
                "• Ingresos hasta 4 SMMLV\n\n"
                "<b>💰 Subsidio:</b> Hasta $30 millones\n\n"
                "<b>📞 Contacto:</b> 123-456-7893\n"
                "<b>🌐 Web:</b> www.medellin.gov.co/vivienda"
            )
        },
        "prog_alimentacion": {
            "titulo": "🍲 Alimentación Escolar",
            "descripcion": (
                "Programa de alimentación en instituciones educativas.\n\n"
                "<b>📌 Cobertura:</b>\n"
                "• Desayuno y almuerzo\n"
                "• Estudiantes de colegios públicos\n\n"
                "<b>📞 Contacto:</b> 123-456-7894"
            )
        }
    }

    # Obtener la información del programa seleccionado
    info = programas_info.get(query.data)

    if info:
        # Crear botón para volver
        keyboard = [[InlineKeyboardButton("⬅️ Volver", callback_data="volver_programas")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"{info['titulo']}\n\n{info['descripcion']}",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif query.data == "volver_programas":
        # Recrear el menú de programas
        keyboard = [
            [InlineKeyboardButton("💙 Medellín Te Quiere", callback_data="prog_medellin_te_quiere")],
            [InlineKeyboardButton("👶 Buen Comienzo 365", callback_data="prog_buen_comienzo")],
            [InlineKeyboardButton("🎓 Oportunidades para Crecer", callback_data="prog_oportunidades")],
            [InlineKeyboardButton("🏠 Subsidios de Vivienda", callback_data="prog_subsidios")],
            [InlineKeyboardButton("🍲 Alimentación Escolar", callback_data="prog_alimentacion")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="📋 <b>Programas Sociales Disponibles</b>\n\nSelecciona el programa que deseas consultar:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )


# ========== CONVERSACIÓN DE NOTIFICACIONES ==========

async def notificaciones_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia el flujo de configuración de notificaciones"""
    await update.message.reply_text(
        "🚗 <b>Configuración de Notificaciones de Movilidad</b>\n\n"
        "Vamos a configurar alertas para tu vehículo.\n"
        "Recibirás notificaciones sobre:\n"
        "• 🚦 Pico y placa\n"
        "• 🚧 Cierres viales\n"
        "• 📢 Eventos importantes\n\n"
        "Por favor, escribe la <b>placa de tu vehículo</b> (ej: ABC123):\n\n"
        "<i>Puedes usar /cancelar en cualquier momento</i>",
        parse_mode='HTML'
    )
    return ASK_PLATE


async def ask_vehicle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Solicita el nombre del vehículo (segundo paso)"""
    plate = update.message.text.strip().upper()

    # Validación básica de placa
    if len(plate) < 5 or len(plate) > 7:
        await update.message.reply_text(
            "❌ Placa inválida. Por favor ingresa una placa válida (ej: ABC123):"
        )
        return ASK_PLATE

    context.user_data["plate"] = plate
    await update.message.reply_text(
        f"✅ Placa registrada: <b>{plate}</b>\n\n"
        "Ahora dime el <b>nombre del vehículo</b> para identificarlo fácilmente\n"
        "(ej: Mi carro, Moto trabajo, etc.):",
        parse_mode='HTML'
    )
    return ASK_VEHICLE_NAME


async def save_vehicle_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guarda la información del vehículo (paso final)"""
    name = update.message.text.strip()
    plate = context.user_data.get("plate", "N/A")
    user_id = update.effective_user.id

    # TODO: Aquí guardarás en Firestore
    # firestore_service.save_vehicle(user_id, plate, name)

    await update.message.reply_text(
        f"✅ <b>¡Configuración completa!</b>\n\n"
        f"📝 <b>Vehículo:</b> {name}\n"
        f"🚗 <b>Placa:</b> {plate}\n\n"
        f"Te notificaré sobre:\n"
        f"• Cambios en pico y placa\n"
        f"• Cierres viales en tu zona\n"
        f"• Eventos que afecten la movilidad\n\n"
        f"Usa /notificaciones para agregar más vehículos.",
        parse_mode='HTML'
    )

    # Limpiar datos temporales
    context.user_data.clear()

    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la conversación actual"""
    await update.message.reply_text(
        "❌ Operación cancelada.\n\n"
        "Usa /ayuda para ver los comandos disponibles."
    )
    context.user_data.clear()
    return ConversationHandler.END


# ========== MENSAJE GENERAL (IA) ==========

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para mensajes de texto libres (procesados con IA)"""
    logger.info(f"Mensaje recibido de {update.effective_user.id}: {update.message.text}")
    user_message = update.message.text.strip()
    user_name = update.effective_user.first_name

    # TODO: Aquí integrarás LangChain/OpenAI para procesar el mensaje
    # response = ai_service.process_message(user_message)

    response = (
        f"💬 Hola {user_name}, recibí tu mensaje:\n"
        f"<i>{user_message}</i>\n\n"
        f"🤖 Próximamente procesaré esto con IA para darte una respuesta inteligente.\n\n"
        f"Por ahora, usa /ayuda para ver los comandos disponibles."
    )

    await update.message.reply_text(response, parse_mode='HTML')
    logger.info("Respuesta enviada correctamente")


# ========== ERROR HANDLER ==========

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handler global de errores"""
    logger.error(f"Error: {context.error}", exc_info=context.error)

    # Si hay un update disponible, informar al usuario
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Ocurrió un error al procesar tu mensaje.\n"
                "Por favor intenta de nuevo o usa /ayuda para ver los comandos disponibles."
            )
        except Exception as e:
            logger.error(f"No se pudo enviar mensaje de error al usuario: {e}")