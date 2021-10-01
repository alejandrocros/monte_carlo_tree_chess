def print_stats(game, results, last_score, table1, table2=None):
    explored_variables = (
        len(table1.keys()) + len(table2.keys()) if table2 else len(table1.keys())
    )

    if results.shape[0] >= 10:
        print(
            f"Game {game + 1} --> {results.mean():.3f} | Explored variants: {explored_variables} ({len(table1.keys())}) | Last result: {last_score} | 10-games mean: {results[-10:].mean()}"
        )
    else:
        print(
            f"Game {game + 1} --> {results.mean():.3f} | Explored variants: {explored_variables} ({len(table1.keys())}) | Last result: {last_score}"
        )
