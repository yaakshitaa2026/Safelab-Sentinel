import sqlite3
from datetime import datetime
from pathlib import Path


# ============================================================
# DATABASE LOCATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATABASE_PATH = PROJECT_ROOT / "safelab.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def initialize_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            device_id TEXT,

            temperature REAL,

            humidity REAL,

            voltage REAL,

            current REAL,

            vibration REAL,

            device_verified INTEGER,

            signature_valid INTEGER,

            security_status TEXT,

            security_risk TEXT,

            security_risk_score INTEGER,

            ai_status TEXT,

            ai_risk TEXT,

            ai_risk_score INTEGER,

            ai_prediction INTEGER,

            final_status TEXT,

            action TEXT

        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# SAVE EVENT
# ============================================================

def save_event(sensor_data, pipeline_result):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events (

            timestamp,
            device_id,

            temperature,
            humidity,
            voltage,
            current,
            vibration,

            device_verified,
            signature_valid,

            security_status,
            security_risk,
            security_risk_score,

            ai_status,
            ai_risk,
            ai_risk_score,
            ai_prediction,

            final_status,
            action

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        sensor_data.get(
            "timestamp",
            datetime.now().isoformat()
        ),

        sensor_data.get(
            "device_id",
            "UNKNOWN"
        ),

        sensor_data.get(
            "temperature",
            0
        ),

        sensor_data.get(
            "humidity",
            0
        ),

        sensor_data.get(
            "voltage",
            0
        ),

        sensor_data.get(
            "current",
            0
        ),

        sensor_data.get(
            "vibration",
            0
        ),

        int(
            pipeline_result.get(
                "device_verified",
                False
            )
        ),

        int(
            pipeline_result.get(
                "signature_valid",
                False
            )
        ),

        pipeline_result.get(
            "security_status",
            "UNKNOWN"
        ),

        pipeline_result.get(
            "security_risk",
            "UNKNOWN"
        ),

        pipeline_result.get(
            "security_risk_score",
            0
        ),

        pipeline_result.get(
            "ai_status",
            "UNKNOWN"
        ),

        pipeline_result.get(
            "ai_risk",
            "UNKNOWN"
        ),

        pipeline_result.get(
            "ai_risk_score",
            0
        ),

        pipeline_result.get(
            "ai_prediction",
            0
        ),

        pipeline_result.get(
            "final_status",
            "UNKNOWN"
        ),

        pipeline_result.get(
            "action",
            "UNKNOWN"
        )
    ))

    connection.commit()

    connection.close()


# ============================================================
# GET RECENT EVENTS
# ============================================================

def get_recent_events(limit=20):

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# INITIALIZE DATABASE WHEN MODULE LOADS
# ============================================================

initialize_database()