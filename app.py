from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# -------------------------
#   BOOK MODEL
# -------------------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Book {self.book_name}>"

    def to_json(self):
        return {
            "id": self.id,
            "book_name": self.book_name,
            "author": self.author,
            "publisher": self.publisher
        }

# -------------------------
#   ROUTES (CRUD)
# -------------------------

# CREATE a book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_json()), 201


# READ all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_json() for book in books])


# READ one book
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_json())


# UPDATE a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()

    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)

    db.session.commit()

    return jsonify(book.to_json())


# DELETE a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted"})


# Run server
if __name__ == '__main__':
    app.run(debug=True)


