import requests
from collections import Counter
from multiprocessing import Pool
import matplotlib.pyplot as plt
import re

# URL с тестовым текстом
TEST_URL = "https://www.gutenberg.org/files/1342/1342-0.txt"

def download_text(url):
    """Завантажує текст із заданої URL-адреси."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def map_reduce(text):
    """Аналізує частоту використання слів у тексті за допомогою MapReduce."""
    words = re.findall(r'\b\w+\b', text.lower())  # Токенізація тексту на слова
    with Pool() as pool:
        # Розподіл обробки по потоках
        mapped = pool.map(map_word, words)
    return reduce_word_counts(mapped)

def map_word(word):
    """Функція Map: повертає слово і одиницю."""
    return (word, 1)

def reduce_word_counts(mapped):
    """Функція Reduce: об'єднує результати."""
    counter = Counter()
    for word, count in mapped:
        counter[word] += count
    return counter

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ N слів за частотою використання."""
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title(f"Топ {top_n} найчастіше вживаних слів")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    print("Якщо ви не введете URL, буде використано тестовий текст.")
    url = input("Введіть URL тексту: ").strip()
    if not url:
        url = TEST_URL
        print(f"Використовується тестовий URL: {url}")

    try:
        text = download_text(url)
        word_counts = map_reduce(text)
        visualize_top_words(word_counts, top_n=10)
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
