def load_popular_hashtags(file_path):
    with open(file_path, 'r' ,encoding='utf-8') as f:
        return set(line.strip().lower() for line in f)

POPULAR_HASHTAGS = load_popular_hashtags('popular_hashtags.txt')