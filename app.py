import argparse,json,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY,title TEXT NOT NULL,project TEXT NOT NULL,assignee TEXT NOT NULL,due_date TEXT NOT NULL,status TEXT NOT NULL)');return c
def add(title,project,assignee,due_date,status,path=DB):
 if status not in ('todo','in_progress','done'):raise ValueError('status must be todo, in_progress or done')
 with connect(path) as c:cur=c.execute('INSERT INTO tasks(title,project,assignee,due_date,status) VALUES(?,?,?,?,?)',(title,project,assignee,due_date,status));return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM tasks ORDER BY due_date')]
def report(path=DB):
 rows=listing(path);return {'tasks':len(rows),'by_status':{s:sum(r['status']==s for r in rows) for s in ('todo','in_progress','done')}}
def main():
 p=argparse.ArgumentParser(description='Project task tracker');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('add');a.add_argument('--title',required=True);a.add_argument('--project',required=True);a.add_argument('--assignee',required=True);a.add_argument('--due-date',required=True);a.add_argument('--status',choices=['todo','in_progress','done'],default='todo');s.add_parser('list');s.add_parser('report');x=p.parse_args()
 if x.cmd=='add':print(json.dumps({'id':add(x.title,x.project,x.assignee,x.due_date,x.status)}))
 elif x.cmd=='list':print(json.dumps(listing(),indent=2))
 else:print(json.dumps(report(),indent=2))
if __name__=='__main__':main()
