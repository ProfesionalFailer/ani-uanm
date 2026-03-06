import questionary
import typer

from .apis import AnimeUnity
from .model import Anime, Episode
from .player import MpvPlayer

app = typer.Typer(help="Anime search and player CLI")

def filter_animes(animes: list[Anime], episode: int | None = None) -> list[Anime]:
    if not episode:
        return animes
    
    if not isinstance(episode, int) or episode < 1:
        typer.echo("Episodio deve essere un numero di episodio valido")
        raise typer.Exit(code=1)
    
    return [ani for ani in animes if ani.n_ep >= episode and episode > (0 if ani.start_from_zero else 1)]

def choose_anime(animes: list[Anime]) -> Anime:    
    if len(animes) == 1:
        return animes[0]
    
    animap = {
        f"{i.title} - {i.n_ep}": i
        for i in animes
    }

    anime_name = questionary.select(
        "Quale anime vuoi vedere?",
        choices=list(animap.keys()),
    ).ask()

    return animap[anime_name]

def choose_episode(episodes: list[Episode], chosen: int) -> int | None:
    if len(episodes) == 1 and chosen is None:
        return episodes[0].num
    
    listep = [str(i.num) for i in episodes]

    if chosen and str(chosen) in listep:
        return chosen
    elif chosen:
        return None

    ep_num = questionary.select(
        "Quale episodio vuoi vedere?",
        choices=listep,
    ).ask()
    
    
    return int(ep_num)

@app.command()
def main(
    anime: str = typer.Argument(..., help="Nome dell'anime da cercare"),
    episode: int | None = typer.Option(None, help="Numero dell'episodio da vedere"),
    dub: bool = typer.Option(False, "--dub", help="Se vogliamo la versione doppiata")
):
    aniuni = AnimeUnity()
    
    filtered: list[Anime] = filter_animes(aniuni.search_animes(anime, dub), episode)
    
    if not filtered:
        typer.echo("Nessun anime trovato con i criteri specificati.")
        raise typer.Exit(code=1)
    

    choice: Anime = choose_anime(filtered) 

    choice.episodes = aniuni.get_episodes(choice)

    if not choice.episodes:
        typer.echo("Nessun episodio trovato.")
        raise typer.Exit(code=1)

    ep: int = choose_episode(choice.episodes, episode) #type: ignore
    if not ep:
        typer.echo("Episodio deve essere un numero di episodio valido")
        raise typer.Exit(code=1)

    mpv = MpvPlayer()
    mpv.load_playlist(anime=choice, episode=ep)
    mpv.player.wait_for_shutdown()

    

if __name__ == "__main__":
    app()