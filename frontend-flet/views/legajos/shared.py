import asyncio
import flet as ft
import httpx
from core.config import settings

class CatalogosService:

    bancos = []

    categorias = []

    modalidades_liquidacion = []

    @classmethod
    async def cargar_bancos(cls, token:str):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{settings.URL_BACKEND}/bancos",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code == 200:

            cls.bancos = response.json()

    @classmethod
    async def cargar_categorias(cls, token):


        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{settings.URL_BACKEND}/categorias",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code == 200:

            cls.categorias = response.json()

    @classmethod
    async def cargar_modalidades_liquidacion(cls, token:str):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{settings.URL_BACKEND}/modalidades",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code == 200:

            cls.modalidades_liquidacion = response.json()

    @classmethod
    async def refresh(cls, token):

        await asyncio.gather(
            cls.cargar_bancos(token),
            cls.cargar_categorias(token),
            cls.cargar_modalidades_liquidacion(token)
        )