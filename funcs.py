import os
import sys
import time

from rich import print as pprint


def clear_screen():
    os.system("cls")


def set_title(title: str):
    os.system(f"title {title}")


def exit():
    sys.exit()


def pause():
    os.system("pause")


def pause_and_exit():
    pause()
    exit()


def success(message: str):
    pprint(f"[bold green]{message}[/bold green]")


def warning(message: str):
    pprint(f"[bold yellow]{message}[/bold yellow]")


def error(message: str):
    pprint(f"[bold red]{message}[/bold red]")


def pinput(message: str):
    pprint(f"[bold yellow]{message}[/bold yellow] ", end="")
    return input("")


def wait(t=3):
    time.sleep(t)
