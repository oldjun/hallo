# -*- coding: utf-8 -*-

from app.console.base import BaseCommand
import secrets


class SecretCommand(BaseCommand):

    @staticmethod
    def refresh():
        print(secrets.token_hex())
