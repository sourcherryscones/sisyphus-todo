from flask import Flask, render_template, redirect, url_for, request
from datetime import date
import os
from supabase import create_client, Client

app = Flask(__name__)

# supabase stuff
url : str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')

if not url or not key:
    raise ValueError('one of the env vars isnt there!')

supabase: Client = create_client(url,key)

@app.route('/', methods=['GET'])
def index():
    current_data = supabase.table("tasks").select('*').order("due_date",desc=False).execute()
    return render_template('index.html', todos_list=current_data.data)

@app.route('/newtodo', methods=['POST'])
def add_todo():
    tname = request.form.get('task_name')
    plevel = request.form.get('priority_level')
    dd = request.form.get('due_date')
    resp = supabase.table("tasks").insert({'task':tname,'priority_level':int(plevel),'due_date':dd}).execute()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def complete_todo(task_id):
    resp = supabase.table("tasks").update({"done":True}).eq("id",task_id).execute()
    return redirect(url_for('index'))

@app.template_filter('fmtdate')
def date_format(value, fmt='%b %d'):
    dt = date.fromisoformat(value)
    return dt.strftime(fmt)
