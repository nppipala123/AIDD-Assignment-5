import sqlite3
import os
from typing import Optional, List, Dict


DB_FILE = os.path.join(os.path.dirname(__file__), 'projects.db')


def ensure_db() -> None:
    """Create database and table if they don't exist. Seed initial rows if empty."""
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS projects ('
            '    Id INTEGER PRIMARY KEY AUTOINCREMENT,'
            '    Title TEXT NOT NULL,'
            '    Description TEXT NOT NULL,'
            '    ImageFileName TEXT'
            ');'
        )
        conn.commit()

        cur.execute('SELECT COUNT(*) FROM projects;')
        count = cur.fetchone()[0]
        if count == 0:
            # Seed with the two requested images if present in images folder
            default_rows = [
                (
                    'Workday Reporting Automation',
                    'Automated custom Workday reports and APIs to streamline HR data exchanges.',
                    'Workday Studio.jpg'
                ),
                (
                    'Power BI Quality Dashboards',
                    'Dashboards built on SQL Server to track shop floor quality and trends.',
                    'PowerBI Dashboard.jpg'
                ),
            ]
            cur.executemany(
                'INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?);',
                default_rows
            )
            conn.commit()
    finally:
        conn.close()


def saveProjectDB(title: str, description: str, image_file_name: Optional[str]) -> None:
    """Insert a new project row."""
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO projects (Title, Description, ImageFileName) VALUES (?,?,?);',
            (title, description, image_file_name or '')
        )
        conn.commit()
    finally:
        conn.close()


def getAllProjects() -> List[Dict]:
    """Return all projects as list of dictionaries suitable for templates."""
    conn = sqlite3.connect(DB_FILE)
    try:
        cur = conn.cursor()
        cur.execute('SELECT Title, Description, ImageFileName FROM projects ORDER BY Id DESC;')
        rows = cur.fetchall()
        results: List[Dict] = []
        for row in rows:
            title = row[0]
            description = row[1]
            image = row[2] if row[2] else ''
            results.append({
                'Title': title,
                'Description': description,
                'Image': image if image else ''
            })
        return results
    finally:
        conn.close()


# Ensure DB and table exist on import
ensure_db()


