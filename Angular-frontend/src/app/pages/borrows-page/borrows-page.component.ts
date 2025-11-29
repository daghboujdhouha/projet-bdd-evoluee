import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { BorrowService, Borrow } from '../../services/borrow.service';
import { BookService, Book } from '../../services/book.service';

@Component({
  selector: 'app-borrows-page',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="card">
      <h1>Mes Emprunts</h1>

      <div *ngIf="loading" style="text-align: center; padding: 20px;">
        Chargement...
      </div>

      <div *ngIf="error" class="alert alert-error">
        {{ error }}
      </div>

      <div *ngIf="message" class="alert" [ngClass]="messageType === 'success' ? 'alert-success' : 'alert-error'">
        {{ message }}
      </div>

      <table *ngIf="!loading && borrows.length > 0" class="table">
        <thead>
          <tr>
            <th>Livre</th>
            <th>Date d'emprunt</th>
            <th>Date de retour prévue</th>
            <th>Date de retour</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let borrow of borrows">
            <td>{{ getBookTitle(borrow.book_id) }}</td>
            <td>{{ formatDate(borrow.borrow_date) }}</td>
            <td>{{ formatDate(borrow.due_date) }}</td>
            <td>{{ borrow.return_date ? formatDate(borrow.return_date) : '-' }}</td>
            <td>{{ borrow.status }}</td>
            <td>
              <button 
                *ngIf="borrow.status === 'active'"
                (click)="returnBook(borrow.id)" 
                class="btn btn-primary"
                [disabled]="actionLoading">
                Retourner
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div *ngIf="!loading && borrows.length === 0" class="alert alert-info">
        Vous n'avez aucun emprunt.
      </div>
    </div>
  `,
  styles: []
})
export class BorrowsPageComponent implements OnInit {
  borrows: Borrow[] = [];
  books: Map<string, Book> = new Map();
  loading = false;
  error = '';
  message = '';
  messageType: 'success' | 'error' = 'success';
  actionLoading = false;

  constructor(
    private borrowService: BorrowService,
    private bookService: BookService
  ) {}

  ngOnInit(): void {
    this.loadBorrows();
  }

  loadBorrows(): void {
    this.loading = true;
    this.error = '';
    
    this.borrowService.getBorrows().subscribe({
      next: (borrows) => {
        this.borrows = borrows;
        this.loadBookTitles();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des emprunts';
        this.loading = false;
      }
    });
  }

  loadBookTitles(): void {
    const bookIds = [...new Set(this.borrows.map(b => b.book_id))];
    bookIds.forEach(id => {
      this.bookService.getBook(id).subscribe({
        next: (book) => {
          this.books.set(id, book);
        }
      });
    });
  }

  returnBook(id: string): void {
    this.actionLoading = true;
    this.message = '';
    
    this.borrowService.returnBook(id).subscribe({
      next: () => {
        this.message = 'Livre retourné avec succès';
        this.messageType = 'success';
        this.actionLoading = false;
        this.loadBorrows();
      },
      error: (err) => {
        this.message = err.error?.error || 'Erreur lors du retour';
        this.messageType = 'error';
        this.actionLoading = false;
      }
    });
  }

  getBookTitle(bookId: string): string {
    return this.books.get(bookId)?.title || 'Chargement...';
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('fr-FR');
  }
}

