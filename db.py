import sqlite3

def save_link(links, link_count):
    conn = sqlite3.connect(r'C:\Users\TheNa\PycharmProjects\playwrite-test\yt-links.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL UNIQUE
    )
    ''')
    cursor.executemany("INSERT OR IGNORE INTO links (content) VALUES (?)", [(s,) for s in links])
    conn.commit()
    conn.close()
    print(f"{link_count}" + " links saved to database.")

def grab_link():
    conn = sqlite3.connect('yt-links.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM links ORDER BY RANDOM() LIMIT 1;")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


