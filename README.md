# SMTP Form Service

A minimal Flask-based email gateway for verification codes, tryout credentials delivery, and install instruction emails.  
It uses SMTP with TLS for sending messages, Redis for short-lived verification codes, and PostgreSQL for persistence.

> This repository contains a single Python service file (`smtp_form.py`) plus configuration samples and minimal SQL schema.

## Features
- **Endpoints**:
  - `POST /send-code` — issue a 6-digit verification code and email it to the user
  - `POST /verify-code` — verify email/code against Redis and persist verification to PostgreSQL
  - `POST /tryout` — generate username/password, email tryout credentials, and persist state
  - `POST /send-install-commands` — email “how to install” commands to the user
- **Email**: HTML + plaintext via SMTP (STARTTLS)
- **Rate limiting**: `50 per minute` per IP (Flask-Limiter)
- **Storage**:
  - **Redis** — temporary verification codes (TTL=300s)
  - **PostgreSQL** — `email_addresses`, `tryout_sessions`, simple proc to check existence
- **Logging**: file logging for delivery and server errors

> All of the above is implemented in `smtp_form.py`. See the file for details. 

## Requirements

- Python 3.10+
- PostgreSQL 13+ (or compatible)
- Redis 6+
- An SMTP account capable of STARTTLS
