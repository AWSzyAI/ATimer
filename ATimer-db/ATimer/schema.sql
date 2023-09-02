--schema.sql

-- 创建 users 表
CREATE TABLE IF NOT EXISTS User (
  id INTEGER PRIMARY KEY,
  username VARCHAR(64) NOT NULL UNIQUE,
  password_hash VARCHAR(128) NOT NULL
);

-- 创建 projects 表
CREATE TABLE IF NOT EXISTS Project (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'In Planning', // 项目状态 InPlanning, InProgress, Completed, Abandoned, Paused
  --all_time TIME DEFAULT '00:00:00',
  all_time TEXT,
  daily_time JSON, -- 日时间,TEXT类型存储JSON
  weekly_time JSON,  
  monthly_time JSON,
  yearly_time JSON,
  FOREIGN KEY (user_id) REFERENCES User (id)
);

-- 创建 records 表
CREATE TABLE IF NOT EXISTS Record (
  id INTEGER PRIMARY KEY,
  project_id INTEGER NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  duration INTERVAL NOT NULL,
  FOREIGN KEY (project_id) REFERENCES Project (id)
);



