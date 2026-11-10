from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Nexus Omni API", version="1.0.0")

# إعداد CORS للسماح بالاتصال من أي منصة عامة وسحابية
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة قاعدة البيانات SQLite
def init_db():
    conn = sqlite3.connect("nexus_omni.db")
    cursor = conn.cursor()
    # جدول المهام
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)
    # جدول المحفظة والموارد المالية
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# نماذج البيانات (Pydantic Models)
class TaskModel(BaseModel):
    title: str

class WalletModel(BaseModel):
    title: str
    amount: float
    type: str  # income أو expense

# نقطة التحقق من حالة السيرفر
@app.get("/")
def read_root():
    return {"message": "تم الاتصال بالباك إند بنجاح يا بطل!"}

@app.get("/status")
def check_status():
    return {"status": "active", "developer": "Aaron Glamour", "system": "Nexus Omni"}

# محرك التحليل الذكي (AI Analytical Engine)
@app.get("/ai/analytics")
def get_ai_analytics():
    return {
        "twin_prediction": "استقرار نمو المهارات والفرص بنسبة 88% للـ 6 أشهر القادمة بناءً على معدل التدفقات المالية وتوزيع المهام.",
        "scenario_recommendation": "التوصية المحاكاة: السيناريو الأفضل: التوسع في مشاريع البرمجيات مع خفض المصروفات التشغيلية بنسبة 12% لتفادي ضغوط الربع القادم.",
        "shield_threat_assessment": "درجة مخاطر الاستقرار المالي والمهني: 15% [آمن جداً]",
        "eco_energy_focus": "مؤشر الطاقة والتركيز: ذروة كفاءة (94%) | مؤشر الإنتاجية: مستقر"
    }

# مسارات إدارة المهام (Tasks Endpoints)
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("nexus_omni.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "title": row["title"]} for row in rows]

@app.post("/tasks")
def add_task(task: TaskModel):
    conn = sqlite3.connect("nexus_omni.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,))
    conn.commit()
    conn.close()
    return {"message": "تم إضافة المهمة بنجاح", "title": task.title}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = sqlite3.connect("nexus_omni.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "تم حذف المهمة بنجاح"}

# مسارات المحفظة والموارد المالية (Wallet Endpoints)
@app.get("/wallet")
def get_wallet():
    conn = sqlite3.connect("nexus_omni.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wallet")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "title": row["title"], "amount": row["amount"], "type": row["type"]} for row in rows]

@app.post("/wallet")
def add_transaction(item: WalletModel):
    conn = sqlite3.connect("nexus_omni.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wallet (title, amount, type) VALUES (?, ?, ?)", (item.title, item.amount, item.type))
    conn.commit()
    conn.close()
    return {"message": "تم تسجيل المعاملة بنجاح"}