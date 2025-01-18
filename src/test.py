import requests
import sys

from bs4 import BeautifulSoup


def main(url):
    """Docstring."""
    inp = [[], [], []]

    try:
        res = requests.get(arg)

        # --- Parse the HTML Content.
        S = BeautifulSoup(res.content, "lxml")

        # --- Parse the Table.
        for tr in S.select("table")[0].select("tr")[1:]:
            for i, td in enumerate(tr.select("td")):
                try:
                    inp[i].append(int(td.p.span.text))
                except:
                    inp[i].append(td.p.span.text)

        # --- Create the default Matrix.
        matrix = [[" " for _ in range(max(inp[0]) + 1)] for _ in range(max(inp[2]) + 1)]

    except Exception as exc:
        print(f"Exception: {str(exc)}")
        return

    # --- Fill in the Grid.
    for i in range(len(inp[1])):
        matrix[inp[2][i]][inp[0][i]] = inp[1][i]

    # --- Print out the Grid.
    for j in matrix[::-1]:
        print(f'{"".join(j)}')


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(f"{arg=}")
        main(arg)
