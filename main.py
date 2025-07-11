from fastapi import FastAPI
app = FastAPI()
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, HTTPException


def setup_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sowjanya@6",
            database="task_manager"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), completed BOOLEAN)")
            cursor.close()
            connection.close()
            print("Table 'tasks' created successfully!")
    except Error as e:
        print("Error connecting to MySQL:", e)

setup_database()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sowjanya@6",
            database="task_manager"
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None
    
@app.get("/tasks/")
async def get_tasks():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="datavase connection failed")
    cursor = connection.cursor()
    cursor.execute("Select * From tasks ")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks

@app.post("/tasks/")
async def create_task(title: str):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = connection.cursor()
    sql = "INSERT INTO tasks (title, completed) VALUES (%s, %s)"
    values = (title, False)
    cursor.execute(sql, values)
    connection.commit()
    task_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {"id": task_id, "title": title, "completed": False}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, completed: bool):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = connection.cursor()
    sql = "UPDATE tasks SET completed = %s WHERE id = %s"
    values = (completed, task_id)
    cursor.execute(sql, values)
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.close()
    connection.close()
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = connection.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    values = (task_id,)
    cursor.execute(sql, values)
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")
    cursor.close()
    connection.close()
    return {"message": "Task deleted"}


@app.get("/")
async def read_root():
    return {"message": "Task Manager API is running!"}