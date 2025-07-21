import os
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.api.core.services.webtoken_service import WebTokenService
from fastapi import HTTPException

class EmailService:
    def __init__(self):
        self.host = os.getenv("MAILER_HOST")
        self.port = int(os.getenv("MAILER_PORT", 587))
        self.user = os.getenv("MAILER_USER")
        self.password = os.getenv("MAILER_PASSWORD")

    def send(self, email_payload: dict):
        msg = MIMEMultipart()
        msg["From"] = email_payload["from"]
        msg["To"] = email_payload["to"]
        msg["Subject"] = email_payload["subject"]
        msg.attach(MIMEText(email_payload["html"], "html"))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(
                    email_payload["from"],
                    email_payload["to"],
                    msg.as_string()
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Email could not be sent")

    def handle_request(self, email: str, email_type: str, webtoken_service: WebTokenService) -> str:
        code = random.randint(100000, 999999)
        token = webtoken_service.generate_token({
            "verificationCode": code
        }, "15m")

        if email_type == "UPDATE":
            payload = self.update_email_builder(email, code)
        elif email_type == "RECOVERY":
            payload = self.account_recovery_email_builder(email, code)
        elif email_type == "NEW":
            payload = self.verification_email_builder(email, code)
        else:
            raise HTTPException(status_code=401, detail="Invalid email type")

        self.send(payload)
        return token

    def verification_email_builder(self, email: str, code: int) -> dict:
        html = self._build_verification_html(code)
        return {
            "from": "postmaster@ginrealestate.mx",
            "to": email,
            "subject": "Verificar Correo Electrónico",
            "html": html
        }

    def account_recovery_email_builder(self, email: str, code: int) -> dict:
        html = self._build_recovery_html(code)
        return {
            "from": "postmaster@ginrealestate.mx",
            "to": email,
            "subject": "Recupera tu cuenta de CXplorers con este enlace",
            "html": html
        }

    def update_email_builder(self, email: str, code: int) -> dict:
        html = self._build_update_html(code)
        return {
            "from": "postmaster@ginrealestate.mx",
            "to": email,
            "subject": "Verificar Correo Electrónico",
            "html": html
        }

    def _build_verification_html(self, code: int) -> str:
        return self._generic_template("Verificación de tu correo electrónico", code)

    def _build_recovery_html(self, code: int) -> str:
        return self._generic_template("Recuperación de Cuenta", code)

    def _build_update_html(self, code: int) -> str:
        return self._generic_template("Verificación de tu correo electrónico", code)

    def _generic_template(self, title: str, code: int) -> str:
        return f"""<!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    }}
                    .code {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #007bff;
                        padding: 10px;
                        margin-top: 10px;
                        border-radius: 5px;
                        background-color: #f4f4f4;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>{title}</h2>
                    <p>Hola,</p>
                    <p>Tu código de verificación es:</p>
                    <div class="code">{code}</div>
                    <p>Este código expirará en 15 minutos.</p>
                    <p>Saludos,<br>El equipo de Code_assistant</p>
                </div>
            </body>
            </html>
        """

