def print_stats(game, results, last_score, table):
    if results.shape[0] >= 10:
        print(f'Game {game + 1} --> {results.mean():.3f} | Table size: {len(table.keys())} | Last result: {last_score} | 10-games mean: {results[-10:].mean()}')
    else:
        print(f'Game {game + 1} --> {results.mean():.3f} | Table size: {len(table.keys())} | Last result: {last_score}')
