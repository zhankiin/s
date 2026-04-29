import psycopg2

# =========================
# DATABASE CONNECTION
# =========================

conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


# =========================
# PLAYER FUNCTIONS
# =========================

def get_or_create_player(username):
    # Проверка игрока в базе
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()

    # Если есть → вернуть id
    if res:
        return res[0]

    # Если нет → создать нового игрока
    cur.execute(
        "INSERT INTO players(username) VALUES(%s) RETURNING id",
        (username,)
    )
    conn.commit()

    return cur.fetchone()[0]


# =========================
# GAME SAVE
# =========================

def save_game(player_id, score, level):
    # Сохраняем результат игры
    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
        (player_id, score, level)
    )
    conn.commit()


def get_top10():
    # Топ 10 игроков
    cur.execute("""
        SELECT username, score FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        ORDER BY score DESC LIMIT 10
    """)
    return cur.fetchall()


def get_best(player_id):
    # Лучший результат игрока
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s", (player_id,))
    res = cur.fetchone()[0]
    return res if res else 0