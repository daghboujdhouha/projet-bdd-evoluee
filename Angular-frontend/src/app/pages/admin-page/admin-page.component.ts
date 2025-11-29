import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService, Book } from '../../services/book.service';

@Component({
  selector: 'app-admin-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="card">
      <h1>Administration - Gestion des Livres</h1>

      <div *ngIf="message" class="alert" [ngClass]="messageType === 'success' ? 'alert-success' : 'alert-error'">
        {{ message }}
      </div>

      <h2>Ajouter un nouveau livre</h2>
      <form (ngSubmit)="createBook()" style="margin-bottom: 30px;">
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
          <div class="form-group">
            <label>Titre *</label>
            <input type="text" [(ngModel)]="newBook.title" name="title" required>
          </div>
          <div class="form-group">
            <label>Auteur *</label>
            <input type="text" [(ngModel)]="newBook.author" name="author" required>
          </div>
          <div class="form-group">
            <label>Genre *</label>
            <input type="text" [(ngModel)]="newBook.genre" name="genre" required>
          </div>
          <div class="form-group">
            <label>Année *</label>
            <input type="number" [(ngModel)]="newBook.year" name="year" required>
          </div>
          <div class="form-group">
            <label>ISBN *</label>
            <input type="text" [(ngModel)]="newBook.isbn" name="isbn" required>
          </div>
          <div class="form-group">
            <label>Statut</label>
            <select [(ngModel)]="newBook.status" name="status">
              <option value="disponible">Disponible</option>
              <option value="réservé">Réservé</option>
              <option value="emprunté">Emprunté</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Description *</label>
          <textarea [(ngModel)]="newBook.description" name="description" rows="4" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary" [disabled]="actionLoading">
          {{ actionLoading ? 'Création...' : 'Créer le livre' }}
        </button>
      </form>

      <h2>Liste des livres</h2>
      <div *ngIf="loading" style="text-align: center; padding: 20px;">
        Chargement...
      </div>

      <table *ngIf="!loading && books.length > 0" class="table">
        <thead>
          <tr>
            <th>Titre</th>
            <th>Auteur</th>
            <th>Genre</th>
            <th>Année</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let book of books">
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.genre }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.status }}</td>
            <td>
              <button (click)="editBook(book)" class="btn btn-secondary" style="margin-right: 5px;">
                Modifier
              </button>
              <button (click)="deleteBook(book.id)" class="btn btn-danger">
                Supprimer
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div *ngIf="editingBook" class="card" style="margin-top: 20px;">
        <h3>Modifier le livre</h3>
        <form (ngSubmit)="updateBook()">
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
            <div class="form-group">
              <label>Titre</label>
              <input type="text" [(ngModel)]="editingBook.title" name="editTitle" required>
            </div>
            <div class="form-group">
              <label>Auteur</label>
              <input type="text" [(ngModel)]="editingBook.author" name="editAuthor" required>
            </div>
            <div class="form-group">
              <label>Genre</label>
              <input type="text" [(ngModel)]="editingBook.genre" name="editGenre" required>
            </div>
            <div class="form-group">
              <label>Année</label>
              <input type="number" [(ngModel)]="editingBook.year" name="editYear" required>
            </div>
            <div class="form-group">
              <label>ISBN</label>
              <input type="text" [(ngModel)]="editingBook.isbn" name="editIsbn" required>
            </div>
            <div class="form-group">
              <label>Statut</label>
              <select [(ngModel)]="editingBook.status" name="editStatus">
                <option value="disponible">Disponible</option>
                <option value="réservé">Réservé</option>
                <option value="emprunté">Emprunté</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea [(ngModel)]="editingBook.description" name="editDescription" rows="4" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary" [disabled]="actionLoading">
            {{ actionLoading ? 'Mise à jour...' : 'Mettre à jour' }}
          </button>
          <button type="button" (click)="cancelEdit()" class="btn btn-secondary">
            Annuler
          </button>
        </form>
      </div>
    </div>
  `,
  styles: []
})
export class AdminPageComponent implements OnInit {
  books: Book[] = [];
  loading = false;
  message = '';
  messageType: 'success' | 'error' = 'success';
  actionLoading = false;
  editingBook: Book | null = null;
  
  newBook: Partial<Book> = {
    title: '',
    author: '',
    genre: '',
    year: new Date().getFullYear(),
    description: '',
    isbn: '',
    status: 'disponible'
  };

  constructor(private bookService: BookService) {}

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.loading = true;
    this.bookService.getBooks().subscribe({
      next: (books) => {
        this.books = books;
        this.loading = false;
      },
      error: (err) => {
        this.message = 'Erreur lors du chargement des livres';
        this.messageType = 'error';
        this.loading = false;
      }
    });
  }

  createBook(): void {
    this.actionLoading = true;
    this.message = '';
    
    this.bookService.createBook(this.newBook).subscribe({
      next: () => {
        this.message = 'Livre créé avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.resetForm();
        this.loadBooks();
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de la création';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  editBook(book: Book): void {
    this.editingBook = { ...book };
  }

  updateBook(): void {
    if (!this.editingBook) return;
    
    this.actionLoading = true;
    this.message = '';
    
    this.bookService.updateBook(this.editingBook.id, this.editingBook).subscribe({
      next: () => {
        this.message = 'Livre mis à jour avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.editingBook = null;
        this.loadBooks();
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de la mise à jour';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  deleteBook(id: string): void {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce livre ?')) {
      return;
    }
    
    this.actionLoading = true;
    this.message = '';
    
    this.bookService.deleteBook(id).subscribe({
      next: () => {
        this.message = 'Livre supprimé avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.loadBooks();
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors de la suppression';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  cancelEdit(): void {
    this.editingBook = null;
  }

  resetForm(): void {
    this.newBook = {
      title: '',
      author: '',
      genre: '',
      year: new Date().getFullYear(),
      description: '',
      isbn: '',
      status: 'disponible'
    };
  }
}

