import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re
import asyncio
import time

# URL з тестовим текстом
TEST_URL = "https://www.gutenberg.org/files/1342/1342-0.txt"

async def download_text(url):
    """Асинхронно завантажує текст із заданої URL-адреси."""
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    response.raise_for_status()
    return response.text

def map_reduce(text):
    """Аналізує частоту використання слів у тексті за допомогою багатопотоковості."""
    words = re.findall(r'\b\w+\b', text.lower())  # Токенізація тексту на слова
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        # Розподіл обробки по потоках
        mapped = list(executor.map(map_word, words))
    end_time = time.time()
    print(f"Час виконання Map: {end_time - start_time:.4f} секунд")
    return reduce_word_counts(mapped)

def map_word(word):
    """Функція Map: повертає слово і одиницю."""
    return (word, 1)

def reduce_word_counts(mapped):
    """Функція Reduce: об'єднує результати."""
    start_time = time.time()
    counter = Counter()
    for word, count in mapped:
        counter[word] += count
    end_time = time.time()
    print(f"Час виконання Reduce: {end_time - start_time:.4f} секунд")
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

async def main():
    print("Якщо ви не введете URL, буде використано тестовий текст.")
    url = input("Введіть URL тексту: ").strip()
    if not url:
        url = TEST_URL
        print(f"Використовується тестовий URL: {url}")

    try:
        start_time = time.time()
        text = await download_text(url)
        download_time = time.time()
        print(f"Час завантаження тексту: {download_time - start_time:.4f} секунд")

        word_counts = map_reduce(text)
        processing_time = time.time()
        print(f"Час обробки тексту (MapReduce): {processing_time - download_time:.4f} секунд")

        visualize_top_words(word_counts, top_n=10)
        end_time = time.time()
        print(f"Загальний час виконання програми: {end_time - start_time:.4f} секунд")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
