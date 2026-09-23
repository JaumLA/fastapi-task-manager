from datetime import time

from sqlmodel import Field, SQLModel, Session, create_engine

from src.config import DATABASE_URL

# Criação das tabelas e models do banco

class User(SQLModel, table=True):
  """
  Tabela do usuário contendo \n
  Id: usando serial do postgresql\n
  email: único e com índice\n
  password: armazenada usando hash e excluída em visualização
  """
  id: int | None = Field(default=None, primary_key=True)
  email: str = Field(unique=True, index=True)
  password: str = Field(exclude=True)


class Task(SQLModel, table=True):
  """
  Tarefas que cada usuário pode criar e ter.\n
  id: serial do postgresql\n
  task_name: nome da tarefa\n
  init_time: horário que a tarefa é iniciada\n
  end_time: horário que a tarefa é finalizada\n
  user_id: id do usuário que criou a tarefa\n
  """
  id: int | None = Field(default=None, primary_key=True)
  task_name: str
  init_time: time | None
  end_time: time | None
  user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")

if not DATABASE_URL:
  exit(1)
engine = create_engine(DATABASE_URL, echo=True)

def get_engine():
   return engine

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

# Se executado direto, esse script cria as tabelas no banco conectado
if __name__ == "__main__":
    create_db_and_tables()