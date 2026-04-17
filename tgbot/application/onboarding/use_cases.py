from typing import Dict, List

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.application.onboarding.ports import OnboardingUserGateway
from tgbot.domain.onboarding import MenuAction, StartScreen


def _build_start_menu_actions() -> List[MenuAction]:
    return [
        MenuAction(key="vipinfo", label="⭐ Diventa VIP"),
        MenuAction(key="bonusgiornaliero", label="🎁 Bonus Giornaliero"),
        MenuAction(key="guadagnacrediti", label="💰 Guadagna Crediti"),
        MenuAction(key="negozio", label="🛍 Negozio"),
        MenuAction(key="recensione", label="🌟 Lascia una recensione"),
        MenuAction(key="supporto", label="🛟 Supporto"),
        MenuAction(
            key="canale_ufficiale",
            label="🆕 Canale ufficiale",
            url="https://t.me/+g_9gg5qszHNiODZk",
        ),
    ]


def build_start_screen(
    user_gateway: OnboardingUserGateway,
    update: Update,
    context: CallbackContext,
) -> StartScreen:
    snapshot = user_gateway.get_user_snapshot(update, context)
    if snapshot.is_new:
        greeting = f"Ciao {snapshot.first_name}, benvenuto!"
    else:
        greeting = f"Bentornato {snapshot.first_name}!"

    return StartScreen(
        text=(
            f"{greeting}\n\n"
            "Benvenuto in <b>Universe Account</b>!\n\n"
            "<b>Utente</b>: Normale\n"
            "<b>Crediti disponibili</b>: in aggiornamento\n\n"
            "Sfrutta al meglio i tuoi crediti e scopri tutte le funzionalita del bot."
        ),
        actions=_build_start_menu_actions(),
    )


def menu_action_message(action_key: str) -> str:
    messages: Dict[str, str] = {
        "vipinfo": "Hai scelto VIP. Collegheremo qui il flusso completo vantaggi e acquisto VIP.",
        "bonusgiornaliero": "Hai scelto Bonus Giornaliero. Collegheremo qui l'accredito bonus giornaliero.",
        "guadagnacrediti": "Hai scelto Guadagna Crediti. Collegheremo qui referral e missioni.",
        "negozio": "Hai scelto Negozio. Collegheremo qui i flussi acquisto (IPTV, account, VPN, ondemand).",
        "recensione": "Hai scelto Recensione. Collegheremo qui invio e moderazione recensioni.",
        "supporto": "Hai scelto Supporto. Collegheremo qui il flusso ticket e assistenza.",
    }
    return messages.get(action_key, "Azione non riconosciuta.")


