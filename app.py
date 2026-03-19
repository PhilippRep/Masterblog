from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("static/blog.json", "r", encoding="utf-8") as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        with open("static/blog.json", "r", encoding="utf-8") as f:
            blog_posts = json.load(f)
        if blog_posts:
            new_id = max(post["id"] for post in blog_posts) + 1
        else:
            new_id = 1
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)
        with open("static/blog.json", "w", encoding="utf-8") as f:
           json.dump(blog_posts, f, ensure_ascii=False, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)