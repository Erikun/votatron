import subprocess


COLUMNS = [
    "tconst",
    "titleType",
    "primaryTitle",
    "originalTitle",
    "isAdult",
    "startYear",
    "endYear",
    "runtimeMinutes",
    "genres"
]


def find_movie(imdb_file, title_regex):

    """
    Find movies with matching 'primary title' in the given IMDB database file
    (title.basics.tsv downloaded from https://datasets.imdbws.com/).
    """

    process = subprocess.run([
        "grep",
        "-i",  # Case insensitive
        f'movie\t[^\t]*{title_regex}',  # Only match movies
        imdb_file
    ], stdout=subprocess.PIPE)
    hits = [dict(zip(COLUMNS, hit.decode("utf-8").split("\t")))
            for hit in process.stdout.split(b"\n")[:-1]]
    # Try to filter out irrelevant hits, e.g. that don't yet exist or are porn
    legitimate_hits = [hit for hit in hits
                       if hit["startYear"] != "\\N" and
                       hit["isAdult"] == "0"]
    return legitimate_hits


if __name__ == "__main__":

    import sys

    print(find_movie("title.basics.tsv", " ".join(sys.argv[1:])))
