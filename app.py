import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных (пока используем простую SQLite, файл появится сам)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knotseedbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель раздачи (как она хранится в базе)
class Torrent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    seeds = db.Column(db.Integer, default=0)
    peers = db.Column(db.Integer, default=0)
    date_added = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(10), default='📁')

# Главная страница
@app.route('/')
def index():
    # Берем все раздачи из базы данных
    torrents = Torrent.query.order_by(Torrent.id.desc()).all()
    return render_template('index.html', torrents=torrents)

# Команда для первичного заполнения базы (сработает при первом запуске)
with app.app_context():
    db.create_all()
    if Torrent.query.count() == 0:
        # Добавляем тестовые данные, если база пустая
        initial_data = [
            Torrent(title="Дюна: Часть вторая (2024) [4K UHD]", category="Фильмы", size="45 GB", seeds=1240, peers=340, date_added="2 мин назад", icon="🎬"),
            Torrent(title="Cyberpunk 2077: Phantom Liberty (v2.1)", category="Игры (PC)", size="65 GB", seeds=2100, peers=450, date_added="15 мин назад", icon="🎮"),
            Torrent(title="Daft Punk - Random Access Memories (2013) [FLAC]", category="Lossless", size="1.2 GB", seeds=430, peers=15, date_added="1 час назад", icon="🎵"),
            Torrent(title="Оппенгеймер (2023) [1080p BDRip]", category="Фильмы", size="32 GB", seeds=850, peers=120, date_added="3 часа назад", icon="🎬"),
            Torrent(title="Чистый код (Роберт Мартин) [PDF, EPUB]", category="Учебники", size="15 MB", seeds=120, peers=5, date_added="1 день назад", icon="📚")
        ]
        db.session.bulk_save_objects(initial_data)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)