import sqlite3
import database 

def exibir_menu():
    print("\n" + "="*30)
    print("      SISTEMA BIBLIOTECA      ")
    print("="*30)
    print("1. Cadastrar Livro")
    print("2. Listar Todos os Livros")
    print("3. Buscar Livro por ID")
    print("4. Atualizar Livro")
    print("5. Deletar Livro")
    print("---")
    print("6. Cadastrar Leitor")
    print("7. Listar Todos os Leitores")
    print("8. Atualizar Leitor")
    print("9. Deletar Leitor")
    print("---")
    print("10. Realizar Empréstimo")
    print("11. Realizar Devolução")
    print("12. Histórico de Empréstimos por Leitor")
    print("13. Relatório de Livros Atrasados (+30 dias)")
    print("0. Sair")
    print("="*30)

def main():
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n[NOVO LIVRO]")
            database.create_book(cur, con)

        elif opcao == "2":
            print("\n[TODOS OS LIVROS]")
            books = database.get_all_books(cur)
            if not books:
                print("Nenhum livro cadastrado.")
            else:
                for b in books:
                    print(f"ID: {b[0]} | Título: {b[1]} | Autor: {b[2]}")

        elif opcao == "3":
            print("\n[BUSCAR LIVRO POR ID]")
            try:
                id_livro = int(input("Digite o ID do livro que deseja buscar: "))
                book = database.get_book_by_id(id_livro, cur)
                
                if not book:
                    print("Livro não encontrado com o ID informado.")
                else:
                    print("-" * 40)
                    print(f"ID: {book[0]}")
                    print(f"Título: {book[1]}")
                    print(f"Autor: {book[2]}")
                    print("-" * 40)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "4":
            print("\n[ATUALIZAR LIVRO]")
            try:
                id_livro = int(input("Digite o ID do livro que deseja atualizar: "))
                database.update_book(id_livro, cur, con)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "5":
            print("\n[DELETAR LIVRO]")
            try:
                id_livro = int(input("Digite o ID do livro que deseja deletar: "))
                database.delete_book(id_livro, cur, con)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "6":
            print("\n[NOVO LEITOR]")
            database.create_reader(cur, con)

        elif opcao == "7":
            print("\n[TODOS OS LEITORES]")
            readers = database.get_all_users(cur)
            if not readers:
                print("Nenhum leitor cadastrado.")
            else:
                for reader in readers:
                    print(f"ID: {reader[0]} | Nome: {reader[1]}")

        elif opcao == "8":
            print("\n[ATUALIZAR LEITOR]")
            try:
                id_leitor = int(input("Digite o ID do leitor que deseja atualizar: "))
                database.update_reader(id_leitor, cur, con)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "9":
            print("\n[DELETAR LEITOR]")
            try:
                id_leitor = int(input("Digite o ID do leitor que deseja deletar: "))
                database.delete_reader(id_leitor, cur, con)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "10":
            print("\n[NOVO EMPRÉSTIMO]")
            try:
                id_livro = int(input("Digite o ID do livro: "))
                id_leitor = int(input("Digite o ID do leitor: "))
                
                sucesso = database.loan(id_livro, id_leitor, cur, con)
                if sucesso:
                    print("Empréstimo realizado com sucesso!")

            except ValueError:
                print("IDs precisam ser números inteiros.")

        elif opcao == "11":
            print("\n[DEVOLUÇÃO DE LIVRO]")
            try:
                id_livro = int(input("Digite o ID do livro sendo devolvido: "))
                database.return_book(id_livro, cur, con)
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "12":
            print("\n[EMPRÉSTIMOS ATIVOS DO LEITOR]")
            try:
                id_leitor = int(input("Digite o ID do leitor para buscar os empréstimos: "))
                ativos = database.get_books_by_reader(id_leitor, cur)
                
                if not ativos:
                    print("O leitor não possui nenhum empréstimo ATIVO no momento.")
                else:
                    print(f"\n--- Livros atualmente com o Leitor (ID: {id_leitor}) ---")
                    for item in ativos:
                        print(f"ID Livro: {item[0]} | Livro: {item[1]} ({item[2]}) | Retirado em: {item[3]}")
                        
            except ValueError:
                print("Por favor, digite um ID numérico válido.")

        elif opcao == "13":
            print("\n[RELATÓRIO DE ATRASOS]")
            overdue = database.get_overdue_books(cur)
            if not overdue:
                print("Nenhum livro atrasado! Todos os prazos estão em dia.")
            else:
                print(f"Alerta: {len(overdue)} empréstimos com mais de 30 dias de atraso!")
                print("-" * 60)
                for o in overdue:
                    print(f"Livro ID: {o[0]} | '{o[1]}' ({o[2]})")
                    print(f"Leitor: {o[3]} | Retirado em: {o[4]} ({o[5]} dias de atraso)")
                    print("-" * 60)

        elif opcao == "0":
            print("\nEncerrando o sistema da biblioteca. Até mais!")
            break
        else:
            print("Opção inválida! Tente novamente.")

    cur.close()
    con.close()

if __name__ == "__main__":
    main()