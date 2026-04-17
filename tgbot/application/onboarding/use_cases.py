from typing import Dict, List

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.application.onboarding.ports import OnboardingUserGateway
from tgbot.domain.onboarding import MenuAction, StartScreen


def _build_start_menu_actions() -> List[MenuAction]:
    return [
        MenuAction(key="shop", label="🛍 Negozio"),
        MenuAction(key="support", label="🛟 Supporto"),
        MenuAction(key="profile", label="👤 Profilo"),
        MenuAction(key="credits", label="💳 Crediti"),
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
        text=f"{greeting}\n\nSeleziona una voce dal menu qui sotto.",
        actions=_build_start_menu_actions(),
    )


def menu_action_message(action_key: str) -> str:
    messages: Dict[str, str] = {
        "shop": "Hai scelto Negozio. Qui potremo agganciare il flusso acquisti (IPTV, account, VPN).",
        "support": "Hai scelto Supporto. Qui potremo agganciare il flusso assistenza e ticket.",
        "profile": "Hai scelto Profilo. Qui potremo mostrare stato utente, piano e referral.",
        "credits": "Hai scelto Crediti. Qui potremo agganciare ricarica e storico movimenti.",
    }
    return messages.get(action_key, "Azione non riconosciuta.")


