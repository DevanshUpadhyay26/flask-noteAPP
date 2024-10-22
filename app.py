# backend code


from flask import Flask, render_template, request, redirect, url_for

import sqlite3

app = Flask(__name__)



def init_db():
    con = sqlite3.connect('notes.db')
    c = con.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT,
              content TEXT NOT NULL)''')
    con.commit()
    con.close()


@app.route('/', methods=['GET','POST'])
def index():
    con = sqlite3.connect('notes.db')
    c = con.cursor()


    if request.method == 'POST':
        note_content = request.form['content']
        if note_content:
            c.execute(''' INSERT INTO notes(content) VALUES(?)''',(note_content,))
            con.commit()
            return redirect(url_for('index'))
    

    c.execute(''' SELECT * FROM notes ''')
    notes = c.fetchall()
    con.close()

    return render_template('index.html', notes = notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    con = sqlite3.connect('notes.db')
    c = con.cursor()
    c.execute(''' DELETE FROM notes WHERE id = ?''', (note_id,))
    con.commit()
    con.close()
    return redirect(url_for('index'))




if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0",port=int("3000") ,debug=True)


