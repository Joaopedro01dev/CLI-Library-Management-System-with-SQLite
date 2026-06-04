import sqlite3

# Books
def create_book(cur, con):
    
    while True:
        title = input("Digite o título do livro: ").strip().title()
        if title:
            break
        print("O campo não pode ser vazio!")

    while True:
        author = input("Digite o nome do autor do livro: ").strip().title()
        if author:
            break
        print("O campo não pode ser vazio!")

    try:
        cur.execute("""
            INSERT INTO book (title, author)
            VALUES(?, ?);
        """, (title, author))
        
        con.commit()
        print(f"Sucesso! O livro '{title}' foi adicionado com sucesso!")

    except sqlite3.Error as e:

        con.rollback()
        print(f"Erro ao salvar no banco de dados: {e}")


def update_book(book_id, cur, con):

    try:
        cur.execute("SELECT title, author FROM book WHERE id = ?", (book_id,))
        current_book = cur.fetchone()
        
        if not current_book:
            print("Erro: Livro não encontrado!")
            return
            
        current_title, current_author = current_book

    except sqlite3.Error as e:
        print(f"Erro ao buscar dados do livro: {e}")
        return

    new_title = input("Digite o novo título ou pressione ENTER para manter: ").strip().title()
    if not new_title:
        new_title = current_title

    new_author = input("Digite o novo autor ou pressione ENTER para manter: ").strip().title()
    if not new_author:
        new_author = current_author

    try:
        cur.execute("""
            UPDATE book
            SET title = ?, author = ?
            WHERE id = ?
        """, (new_title, new_author, book_id))

        con.commit()
        print(f"Sucesso! O livro foi atualizado para '{new_title}'.")

    except sqlite3.Error as e:
        con.rollback()
        print(f"Falha ao atualizar no banco de dados: {e}")


def delete_book(book_id, cur, con):
    try:
        cur.execute("""
            SELECT book_id FROM loan
            WHERE book_id = ? AND return_date IS NULL; 
        """, (book_id,))

        if cur.fetchone():
            print("Erro: O livro está emprestado no momento!")
            return
        
        cur.execute("""
            DELETE FROM book
            WHERE id = ?;
        """, (book_id,))

        if cur.rowcount == 0:
            print("Erro! Livro não encontrado no banco de dados!")
            return

        con.commit()
        print("Livro deletado com sucesso!")

    except sqlite3.Error as e:

        con.rollback()
        print(f"Erro ao deletar no banco de dados: {e}")


def get_all_books(cur):
    try:
        cur.execute("""
            SELECT id, title, author FROM book;
        """)

        books = cur.fetchall()
        return books
    
    except sqlite3.Error as e:
        print(f"Erro ao buscar todos os livros: {e}")
        return []
    
def get_book_by_id(book_id, cur):
    try:
        cur.execute("""
            SELECT id, title, author FROM book
            WHERE id = ?;
        """, (book_id,))

        book = cur.fetchone()
        return book
    
    except sqlite3.Error as e:
        print(f"Erro ao ler o livro {book_id}: {e}")
        return None

# Readers
def create_reader(cur, con):
    while True:
        name = input("Digite o nome do leitor: ").strip().title()
        if name:
            break
    
        print("O campo não pode ser vazio!")

    try:
        cur.execute("""
            INSERT INTO reader (name)
            VALUES (?);
        """, (name,))

        con.commit()
        print(f"Sucesso! Leitor '{name}' criado!")

    except sqlite3.Error as e:

        print(f"Erro ao criar o leitor: {e}")


def update_reader(reader_id, cur, con):
    try:
        cur.execute("SELECT name FROM reader WHERE id = ?;", (reader_id,))
        current_reader = cur.fetchone()

        if not current_reader:
            print("Leitor não encontrado!")
            return
        
    except sqlite3.Error as e:
        print(f"Erro ao procurar o leitor: {e}")
        return
    
    new_name = input("Digite um novo nome ou pressione ENTER para manter: ").strip().title()
    if not new_name:
        new_name = current_reader[0]

    try:
        cur.execute("""
            UPDATE reader
            SET name = ?
            WHERE id = ?;
        """, (new_name, reader_id,))

        con.commit()
        print(f"Sucesso! Leitor atualizado para '{new_name}'")

    except sqlite3.Error as e:
        con.rollback()
        print(f"Erro ao atualizar o leitor: {e}")

def delete_reader(reader_id, cur, con):
    try:
        cur.execute("""
            SELECT id FROM reader
            WHERE id = ?;
        """, (reader_id,))

        if not cur.fetchone():
            print("Leitor não encontrado!")
            return
        
        cur.execute("""
            DELETE FROM loan
            WHERE reader_id = ?;
        """, (reader_id,))

        cur.execute("""
            DELETE FROM reader
            WHERE id = ?;
        """, (reader_id,))

        con.commit()

    except sqlite3.Error as e:
        con.rollback()
        print(f"Erro ao deletar o leitor: {e}")

def get_all_users(cur):
    try:
        cur.execute("""
            SELECT id, name FROM reader;
        """)

        readers = cur.fetchall()
        return readers
    
    except sqlite3.Error as e:
        print(f"Erro ao selecionar os leitores: {e}")
        return []
    
def get_reader_by_id(reader_id, cur):
    try:
        cur.execute("""
            SELECT name FROM reader
            WHERE id = ?;
        """, (reader_id,))

        reader = cur.fetchone()
        return reader
    
    except sqlite3.Error as e:
        print(f"Erro ao pegar o leitor '{reader_id}: {e}'")
        return None

# Loan
def loan(book_id, reader_id, cur, con):
    try:
        cur.execute("SELECT id FROM book WHERE id = ?;", (book_id,))
        if not cur.fetchone():
            print("Erro: O ID do livro informado não existe!")
            return

        cur.execute("SELECT id FROM reader WHERE id = ?;", (reader_id,))
        if not cur.fetchone():
            print("Erro: O ID do leitor informado não existe!")
            return

        cur.execute("""
            SELECT id FROM loan
            WHERE book_id = ? AND return_date IS NULL;
        """, (book_id,))

        if cur.fetchone():
            print("Erro: Livro não disponível, pois já está emprestado!")
            return
            
        cur.execute("""
            INSERT INTO loan (reader_id, book_id, loan_date)
            VALUES (?, ?, DATE('now'));
        """, (reader_id, book_id))

        con.commit()
        print("Empréstimo realizado com sucesso!")

    except sqlite3.Error as e:
        con.rollback()
        print(f"Erro no banco de dados: {e}")

def return_book(book_id, cur, con):
    try:
        cur.execute("""
            SELECT id FROM loan
            WHERE book_id = ? AND return_date IS NULL;
        """, (book_id,))
        
        loan_record = cur.fetchone()
        
        if not loan_record:
            print("Erro: Este livro não possui nenhum empréstimo ativo no momento!")
            return
            
        loan_id = loan_record[0]

        cur.execute("""
            UPDATE loan
            SET return_date = DATE('now')
            WHERE id = ?;
        """, (loan_id,))

        con.commit()
        print("Sucesso! Livro devolvido e disponível para novos empréstimos.")

    except sqlite3.Error as e:
        con.rollback()
        print(f"Erro ao processar devolução no banco de dados: {e}")

def get_books_by_reader(reader_id, cur):
    try:
        cur.execute("""
            SELECT id FROM loan
            WHERE reader_id = ?;
        """, (reader_id,))

        if not cur.fetchone():
            print("Erro! Leitor sem histórico de livros emprestados!")
            return

        cur.execute("""
            SELECT book.title, book.author, loan.loan_date, loan.return_date
            FROM loan
            JOIN book ON book.id = loan.book_id
            WHERE loan.reader_id = ? AND loan.return_date IS NULL;
        """, (reader_id,))

        loans = cur.fetchall()
        print(f"\n--- Histórico de Empréstimos do Leitor (ID: {reader_id}) ---")
        
        for row in loans:
            title = row[0]
            author = row[1]
            loan_date = row[2]
            return_date = row[3]
            
            if return_date is None:
                status = "EM ANDAMENTO"
            else:
                status = f"DEVOLVIDO em {return_date}"
                
            print(f"Livro: {title} ({author}) | Retirado em: {loan_date} | Status: {status}")

    except sqlite3.Error as e:
        print(f"Erro ao buscar histórico do leitor: {e}")

def get_overdue_books(cur):
    try:
        cur.execute("""
            SELECT book.id AS book_id, book.title, book.author, reader.name AS reader_name, loan.loan_date, CAST(JULIANDAY('now') - JULIANDAY(loan.loan_date) AS INTEGER) AS days_overdue
            FROM loan
            JOIN book ON book.id = loan.book_id
            JOIN reader ON reader.id = loan.reader_id
            WHERE loan.return_date IS NULL AND loan.loan_date < DATE('now', '-30 days');
        """)

        overdue_books = cur.fetchall()
        return overdue_books

    except sqlite3.Error as e:
        print(f"Erro ao buscar livros atrasados: {e}")
        return []