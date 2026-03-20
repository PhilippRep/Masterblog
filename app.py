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

@app.route('/delete/<int:post_id>',  methods=["POST"])
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    with open("static/blog.json", "r", encoding="utf-8") as f:
        blog_posts = json.load(f)
    updated_blog = [post for post in blog_posts if post.get('id') != post_id]
    with open("static/blog.json", "w", encoding="utf-8") as f:
        json.dump(updated_blog, f, ensure_ascii=False, indent=4)
    # Redirect back to the home page
        return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
    # Update the post in the JSON file
    # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)