import os
import random
from datetime import datetime, timedelta
word_list = ["apple", "banana", "cat", "dog", "elephant", "fish", "giraffe", "house", "ice", "jungle",
             "kite", "lemon", "monkey", "night", "orange", "pencil", "queen", "rain", "sun", "tree",
             "umbrella", "vase", "whale", "xray", "yacht", "zebra", "ball", "car", "drum", "eagle",
             "frog", "goat", "hat", "ink", "jam", "key", "lion", "milk", "net", "owl",
             "pen", "quiz", "rope", "snake", "train", "van", "wolf", "yak", "zoo", "ant"]

start_date = datetime.strptime("2025-04-20T23:50:21+05:30", "%Y-%m-%dT%H:%M:%S%z")

def f():
    for i in range(2000):
        file_name = f"post_{i}.md"
        f = open(file_name, 'w+')
        current_date = start_date + timedelta(days=i)
        header = f"""+++
date = '{current_date.strftime('%Y-%m-%dT%H:%M:%S%z')}'
draft = false
title = '{random.choice(word_list)} {random.choice(word_list)}'
+++\n\n\n"""
        random_words = random.choices(word_list, k=50)
        f.write(header)
        f.write(' '.join(random_words + ["\n"]))
        f.close()
        print(f"{file_name} has been created!")
        
f()