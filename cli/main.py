import os
import shutil
import subprocess
import questionary
from rich.console import Console

console = Console()

PROJECTS_BASE = "/var/www/html"


def run(cmd: str):
    subprocess.run(cmd, shell=True)


def get_containers():
    result = subprocess.getoutput("docker ps -a --format '{{.Names}}'")
    return result.splitlines() if result else []


def get_images():
    result = subprocess.getoutput("docker images --format '{{.Repository}}:{{.Tag}}'")
    return result.splitlines() if result else []


def get_volumes():
    result = subprocess.getoutput("docker volume ls --format '{{.Name}}'")
    return result.splitlines() if result else []


def find_local_volume_dirs():
    dirs = []
    if not os.path.isdir(PROJECTS_BASE):
        return []

    for proj in os.listdir(PROJECTS_BASE):
        vol_dir = os.path.join(PROJECTS_BASE, proj, ".docker", ".volumes")
        if os.path.isdir(vol_dir):
            dirs.append(vol_dir)

    return dirs


def remove_local_volume_dirs():
    dirs = find_local_volume_dirs()

    if not dirs:
        console.print("[yellow]Nenhum diretório .volumes encontrado.[/yellow]")
        return

    selected = questionary.checkbox(
        "Selecione as pastas .volumes que deseja apagar:",
        choices=dirs
    ).ask()

    if not selected:
        return

    if questionary.confirm("Tem certeza que deseja remover TODAS essas pastas?").ask():
        for d in selected:
            console.print(f"[red]Removendo:[/] {d}")
            run(f"sudo rm -rf '{d}'")  

        console.print("[green]Pastas .volumes removidas.[/green]")


def remove_containers():
    containers = get_containers()
    if not containers:
        return console.print("[yellow]Nenhum container encontrado.[/yellow]")

    selected = questionary.checkbox("Selecione containers para remover:", choices=containers).ask()

    if selected and questionary.confirm("Confirmar remoção?").ask():
        for c in selected:
            run(f"docker rm -f {c}")


def remove_images():
    images = get_images()
    if not images:
        return console.print("[yellow]Nenhuma imagem encontrada.[/yellow]")

    selected = questionary.checkbox("Selecione imagens para remover:", choices=images).ask()

    if selected and questionary.confirm("Confirmar remoção?").ask():
        for img in selected:
            run(f"docker rmi -f {img}")


def remove_docker_volumes():
    volumes = get_volumes()
    if not volumes:
        return console.print("[yellow]Nenhum volume Docker encontrado.[/yellow]")

    selected = questionary.checkbox("Selecione volumes Docker:", choices=volumes).ask()

    if selected and questionary.confirm("Confirmar remoção?").ask():
        for v in selected:
            run(f"docker volume rm {v}")


def prune_all():
    if questionary.confirm("Isso vai apagar tudo (containers, imagens, volumes). Continuar?").ask():
        run("docker system prune -a --volumes -f")


def main_menu():
    while True:
        choice = questionary.select(
            "🐳 Docker Cleaner",
            choices=[
                "Remover Containers",
                "Remover Imagens",
                "Remover Volumes Docker",
                "Remover Volumes Locais (.docker/.volumes)",
                "Limpar Tudo (prune)",
                "Sair"
            ]
        ).ask()

        if choice == "Remover Containers":
            remove_containers()

        elif choice == "Remover Imagens":
            remove_images()

        elif choice == "Remover Volumes Docker":
            remove_docker_volumes()

        elif choice == "Remover Volumes Locais (.docker/.volumes)":
            remove_local_volume_dirs()

        elif choice == "Limpar Tudo (prune)":
            prune_all()

        elif choice == "Sair":
            break


if __name__ == "__main__":
    main_menu()