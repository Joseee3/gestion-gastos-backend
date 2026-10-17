
import os
from functools import lru_cache

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging


SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")

ISSUER = f"{SUPABASE_URL}/auth/v1"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

security = HTTPBearer()


@lru_cache
def obtener_cliente_claves():
    if not SUPABASE_URL:
        raise RuntimeError("Falta configurar SUPABASE_URL")

    return PyJWKClient(JWKS_URL)


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
):
    token = credenciales.credentials

    try:
        # Diagnóstico: registra solo metadatos del encabezado, nunca el token.
        header = jwt.get_unverified_header(token)
        logging.warning(
            "JWT recibido: alg=%s kid=%s",
            header.get("alg"),
            header.get("kid"),
        )

        cliente = obtener_cliente_claves()
        clave = cliente.get_signing_key_from_jwt(token).key

        payload = jwt.decode(
            token,
            clave,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=ISSUER,
            options={
                "require": ["exp", "sub", "iss", "aud"],
            },
        )

        usuario_id = payload.get("sub")

        if not usuario_id:
            raise HTTPException(
                status_code=401,
                detail="Token sin identificador de usuario",
            )

        return {
            "id": usuario_id,
            "email": payload.get("email"),
        }

    except HTTPException:
        raise
    except Exception as error:
        # Registra el tipo de error, sin incluir el token ni el secreto.
        logging.warning(
            "Falló la validación JWT: %s",
            type(error).__name__,
        )
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )