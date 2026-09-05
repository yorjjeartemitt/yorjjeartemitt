import random
import re
from pathlib import Path

ASSETS_DIR=Path("assets")
README_PATH=Path("README.md")
START_MARKER="<!--GIF_START-->"
END_MARKER="<!--GIF_END-->"
def get_gif_list() -> list[str]:
    gifs = sorted(ASSETS_DIR.glob("*.gif"))
    if not gifs:
        raise FileNotFoundError(f"Немає .gif файлів у {ASSETS_DIR}/")
    return [g.name for g in gifs]
 
 
def pick_random_gif(gifs: list[str]) -> str:
    return random.choice(gifs)

def update_readme(gif_name: str) -> bool:
    content = README_PATH.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )

    new_block = f"{START_MARKER}\n![video](assets/{gif_name})\n{END_MARKER}"

    if not pattern.search(content):
        raise ValueError(
            f"Маркери {START_MARKER} / {END_MARKER} не знайдені в README.md"
        )

    new_content = pattern.sub(new_block, content)

    if new_content == content:
        return False

    README_PATH.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    gifs = get_gif_list()
    chosen = pick_random_gif(gifs)
    changed = update_readme(chosen)

    if changed:
        print(f"README.md оновлено: {chosen}")
    else:
        print(f"Без змін (випав той самий gif: {chosen})")
if __name__ == "__main__":
    main()
